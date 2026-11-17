
import pytest


@pytest.fixture(scope="module")
def spark():
    from pyspark.sql import SparkSession

    session = (
        SparkSession.builder
        .master("local[2]")
        .appName("RetailSparkTests")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    yield session
    session.stop()


def test_order_revenue_aggregation(spark):
    from pyspark.sql.functions import (
        count,
        round as spark_round,
        sum as spark_sum,
    )

    orders = spark.createDataFrame(
        [
            ("order_1", "delivered"),
            ("order_2", "shipped"),
        ],
        ["order_id", "order_status"],
    )

    items = spark.createDataFrame(
        [
            ("order_1", 1, 100.0),
            ("order_1", 2, 50.0),
            ("order_2", 1, 200.0),
        ],
        ["order_id", "order_item_id", "price"],
    )

    result = (
        orders.join(items, "order_id", "inner")
        .groupBy("order_id", "order_status")
        .agg(
            count("order_item_id").alias("item_count"),
            spark_round(
                spark_sum("price"), 2
            ).alias("total_item_revenue"),
        )
    )

    rows = {
        row["order_id"]: row
        for row in result.collect()
    }

    assert len(rows) == 2

    assert rows["order_1"]["item_count"] == 2
    assert rows["order_1"]["total_item_revenue"] == 150.0

    assert rows["order_2"]["item_count"] == 1
    assert rows["order_2"]["total_item_revenue"] == 200.0
