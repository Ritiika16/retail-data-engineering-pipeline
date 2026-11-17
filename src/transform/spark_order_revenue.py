
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    count,
    round as spark_round,
    sum as spark_sum,
)


def run_spark_order_revenue():
    spark = (
        SparkSession.builder
        .appName("RetailOrderRevenueETL")
        .master("local[2]")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    try:
        base = Path("/opt/airflow/project/data/processed")

        orders = spark.read.parquet(
            str(base / "orders.parquet")
        )

        items = spark.read.parquet(
            str(base / "order_items.parquet")
        )

        revenue = (
            orders.join(items, "order_id", "inner")
            .groupBy("order_id", "order_status")
            .agg(
                count("order_item_id").alias("item_count"),
                spark_round(
                    spark_sum("price"), 2
                ).alias("total_item_revenue"),
            )
        )

        output = base / "spark_order_revenue"

        revenue.write.mode("overwrite").parquet(
            str(output)
        )

        result = spark.read.parquet(str(output))

        row_count = result.count()
        total_items = result.agg(
            spark_sum("item_count")
        ).first()[0]

        assert total_items == 112650

        print(f"Revenue records: {row_count}")
        print(f"Items represented: {total_items}")
        print("SPARK ORDER REVENUE ETL: PASSED")

    finally:
        spark.stop()
