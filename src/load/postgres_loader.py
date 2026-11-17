
import os
import logging
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


def get_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=(
            "host.docker.internal"
            if os.path.exists("/.dockerenv")
            else os.getenv("DB_HOST", "localhost")
        ),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME"),
    )

    return create_engine(database_url)


def load_orders(parquet_path: str | Path) -> None:
    """Load processed orders into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s orders", len(df))

    engine = get_engine()

    try:
        # A transaction ensures the delete and insert
        # either both succeed or both roll back.
        with engine.begin() as connection:

            connection.execute(
                text("DELETE FROM staging.orders")
            )

            df.to_sql(
                name="orders",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.orders")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Row count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s orders",
                count
            )

    finally:
        engine.dispose()


def load_customers(parquet_path: str | Path) -> None:
    """Load processed customers into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s customers", len(df))

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Clear existing customer staging records
            connection.execute(
                text("DELETE FROM staging.customers")
            )

            # Insert transformed customer records
            df.to_sql(
                name="customers",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            # Verify the loaded row count
            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.customers")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Customer row count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s customers",
                count
            )

    finally:
        engine.dispose()


def load_order_items(parquet_path: str | Path) -> None:
    """Load processed order items into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s order items", len(df))

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Clear existing staging records
            connection.execute(
                text("DELETE FROM staging.order_items")
            )

            # Insert order items in batches
            df.to_sql(
                name="order_items",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            # Verify row count
            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.order_items")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Order items count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s order items",
                count
            )

    finally:
        engine.dispose()



def load_products(parquet_path: str | Path) -> None:
    """Load cleaned products into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s products", len(df))

    # Convert count-based columns to nullable integers
    integer_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]

    for column in integer_columns:
        df[column] = df[column].astype("Int64")

    # Convert pandas missing values to SQL NULL
    df = df.astype(object).where(pd.notna(df), None)

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Full refresh inside one transaction
            connection.execute(
                text("DELETE FROM staging.products")
            )

            df.to_sql(
                name="products",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.products")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Products count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s products",
                count
            )

    finally:
        engine.dispose()


def load_sellers(parquet_path: str | Path) -> None:
    """Load transformed sellers into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s sellers", len(df))

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Clear existing records for a full refresh
            connection.execute(
                text("DELETE FROM staging.sellers")
            )

            # Insert transformed sellers
            df.to_sql(
                name="sellers",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            # Verify row count
            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.sellers")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Sellers count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s sellers",
                count
            )

    finally:
        engine.dispose()


def load_payments(parquet_path: str | Path) -> None:
    """Load transformed payments into PostgreSQL staging."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing to load %s payments", len(df))

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Clear existing records (full refresh)
            connection.execute(
                text("DELETE FROM staging.payments")
            )

            # Insert payment records
            df.to_sql(
                name="payments",
                con=connection,
                schema="staging",
                if_exists="append",
                index=False,
                chunksize=1000,
                method="multi",
            )

            # Verify loaded record count
            count = connection.execute(
                text("SELECT COUNT(*) FROM staging.payments")
            ).scalar_one()

            if count != len(df):
                raise ValueError(
                    f"Payments count mismatch: "
                    f"expected {len(df)}, found {count}"
                )

            logger.info(
                "Loaded and verified %s payments",
                count
            )

    finally:
        engine.dispose()


def load_orders_incremental(parquet_path: str | Path) -> int:
    """Insert new orders and update existing orders."""

    df = pd.read_parquet(parquet_path)

    logger.info("Preparing incremental load for %s orders", len(df))

    engine = get_engine()

    try:
        with engine.begin() as connection:

            # Temporary table exists only for this DB session.
            connection.execute(text("""
                CREATE TEMP TABLE temp_orders
                (LIKE staging.orders INCLUDING DEFAULTS)
                ON COMMIT DROP
            """))

            # Load incoming records into the temporary table.
            df.to_sql(
                name="temp_orders",
                con=connection,
                if_exists="append",
                index=False,
                chunksize=5000,
                method="multi",
            )

            # Insert new orders or update existing orders.
            result = connection.execute(text("""
                INSERT INTO staging.orders (
                    order_id,
                    customer_id,
                    order_status,
                    order_purchase_timestamp,
                    order_approved_at,
                    order_delivered_carrier_date,
                    order_delivered_customer_date,
                    order_estimated_delivery_date
                )
                SELECT
                    order_id,
                    customer_id,
                    order_status,
                    order_purchase_timestamp,
                    order_approved_at,
                    order_delivered_carrier_date,
                    order_delivered_customer_date,
                    order_estimated_delivery_date
                FROM temp_orders

                ON CONFLICT (order_id)
                DO UPDATE SET
                    customer_id = EXCLUDED.customer_id,
                    order_status = EXCLUDED.order_status,
                    order_purchase_timestamp =
                        EXCLUDED.order_purchase_timestamp,
                    order_approved_at = EXCLUDED.order_approved_at,
                    order_delivered_carrier_date =
                        EXCLUDED.order_delivered_carrier_date,
                    order_delivered_customer_date =
                        EXCLUDED.order_delivered_customer_date,
                    order_estimated_delivery_date =
                        EXCLUDED.order_estimated_delivery_date

                WHERE (
                    staging.orders.customer_id,
                    staging.orders.order_status,
                    staging.orders.order_purchase_timestamp,
                    staging.orders.order_approved_at,
                    staging.orders.order_delivered_carrier_date,
                    staging.orders.order_delivered_customer_date,
                    staging.orders.order_estimated_delivery_date
                ) IS DISTINCT FROM (
                    EXCLUDED.customer_id,
                    EXCLUDED.order_status,
                    EXCLUDED.order_purchase_timestamp,
                    EXCLUDED.order_approved_at,
                    EXCLUDED.order_delivered_carrier_date,
                    EXCLUDED.order_delivered_customer_date,
                    EXCLUDED.order_estimated_delivery_date
                )
            """))

            logger.info(
                "Incremental orders load completed. "
                "Inserted or updated rows: %s",
                result.rowcount,
            )

            return result.rowcount

    finally:
        engine.dispose()
