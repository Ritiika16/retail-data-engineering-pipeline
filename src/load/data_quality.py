
from sqlalchemy import text

from src.load.postgres_loader import get_engine


def validate_warehouse():
    engine = get_engine()

    checks = {
        "customers_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.dim_customers
        """,
        "products_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.dim_products
        """,
        "sellers_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.dim_sellers
        """,
        "dates_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.dim_date
        """,
        "order_items_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.fact_order_items
        """,
        "payments_not_empty": """
            SELECT COUNT(*) > 0
            FROM warehouse.fact_order_payments
        """,
        "order_items_no_duplicates": """
            SELECT COUNT(*) = COUNT(DISTINCT (order_id, order_item_id))
            FROM warehouse.fact_order_items
        """,
        "payments_no_duplicates": """
            SELECT COUNT(*) = COUNT(DISTINCT (order_id, payment_sequential))
            FROM warehouse.fact_order_payments
        """,
        "order_items_valid_keys": """
            SELECT COUNT(*) = 0
            FROM warehouse.fact_order_items
            WHERE customer_key IS NULL
               OR product_key IS NULL
               OR seller_key IS NULL
               OR order_date_key IS NULL
        """,
        "payments_valid_keys": """
            SELECT COUNT(*) = 0
            FROM warehouse.fact_order_payments
            WHERE customer_key IS NULL
               OR order_date_key IS NULL
        """,


        "order_items_count_match": """
            SELECT
                (SELECT COUNT(*) FROM staging.order_items) =
                (SELECT COUNT(*) FROM warehouse.fact_order_items)
        """,

        "payments_count_match": """
            SELECT
                (SELECT COUNT(*) FROM staging.payments) =
                (SELECT COUNT(*) FROM warehouse.fact_order_payments)
        """,

        "order_items_keys_match": """
            SELECT NOT EXISTS (
                (SELECT order_id, order_item_id
                 FROM staging.order_items
                 EXCEPT
                 SELECT order_id, order_item_id
                 FROM warehouse.fact_order_items)

                UNION ALL

                (SELECT order_id, order_item_id
                 FROM warehouse.fact_order_items
                 EXCEPT
                 SELECT order_id, order_item_id
                 FROM staging.order_items)
            )
        """,

        "payments_keys_match": """
            SELECT NOT EXISTS (
                (SELECT order_id, payment_sequential
                 FROM staging.payments
                 EXCEPT
                 SELECT order_id, payment_sequential
                 FROM warehouse.fact_order_payments)

                UNION ALL

                (SELECT order_id, payment_sequential
                 FROM warehouse.fact_order_payments
                 EXCEPT
                 SELECT order_id, payment_sequential
                 FROM staging.payments)
            )
        """,


        "order_items_customer_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_items f
                LEFT JOIN warehouse.dim_customers d
                    ON f.customer_key = d.customer_key
                WHERE d.customer_key IS NULL
            )
        """,

        "order_items_product_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_items f
                LEFT JOIN warehouse.dim_products d
                    ON f.product_key = d.product_key
                WHERE d.product_key IS NULL
            )
        """,

        "order_items_seller_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_items f
                LEFT JOIN warehouse.dim_sellers d
                    ON f.seller_key = d.seller_key
                WHERE d.seller_key IS NULL
            )
        """,

        "order_items_date_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_items f
                LEFT JOIN warehouse.dim_date d
                    ON f.order_date_key = d.date_key
                WHERE d.date_key IS NULL
            )
        """,

        "payments_customer_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_payments f
                LEFT JOIN warehouse.dim_customers d
                    ON f.customer_key = d.customer_key
                WHERE d.customer_key IS NULL
            )
        """,

        "payments_date_fk": """
            SELECT NOT EXISTS (
                SELECT 1
                FROM warehouse.fact_order_payments f
                LEFT JOIN warehouse.dim_date d
                    ON f.order_date_key = d.date_key
                WHERE d.date_key IS NULL
            )
        """,

    }

    failed_checks = []

    try:
        with engine.connect() as connection:
            for name, query in checks.items():
                passed = connection.execute(text(query)).scalar()

                if passed:
                    print(f"PASS: {name}")
                else:
                    print(f"FAIL: {name}")
                    failed_checks.append(name)

    finally:
        engine.dispose()

    if failed_checks:
        raise ValueError(
            f"Data quality checks failed: {failed_checks}"
        )

    print(f"All {len(checks)} data quality checks passed!")
