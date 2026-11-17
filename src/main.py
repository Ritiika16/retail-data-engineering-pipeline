import pandas as pd
from load.parquet_writer import write_parquet
from pathlib import Path
import logging

from extract.csv_extractor import extract_csv
from transform.orders_transformer import transform_orders
from transform.sellers_transformer import transform_sellers
from transform.payments_transformer import transform_payments
from load.postgres_loader import (
    load_orders_incremental,
    load_customers,
    load_order_items,
    load_products,
    load_sellers,
    load_payments,
)
from transform.customers_transformer import transform_customers
from transform.order_items_transformer import transform_order_items
from transform.products_transformer import transform_products

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

BASE_DIR = Path(__file__).resolve().parents[1]

ORDERS_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "olist"
    / "olist_orders_dataset.csv"
)

PAYMENTS_FILE = (
    BASE_DIR / "data" / "raw" / "olist"
    / "olist_order_payments_dataset.csv"
)

CUSTOMERS_FILE = (
    BASE_DIR / "data" / "raw" / "olist" / "olist_customers_dataset.csv"
)

ORDER_ITEMS_FILE = (
    BASE_DIR / "data" / "raw" / "olist" / "olist_order_items_dataset.csv"
)

PRODUCTS_FILE = (
    BASE_DIR / "data" / "raw" / "olist" / "olist_products_dataset.csv"
)

SELLERS_FILE = (
    BASE_DIR / "data" / "raw" / "olist" / "olist_sellers_dataset.csv"
)
def main():
    print("\nStarting Retail Data Engineering Pipeline")

    # Step 1: Extract
    raw_orders = extract_csv(ORDERS_FILE)

    # Step 2: Transform
    clean_orders = transform_orders(raw_orders)

    # Step 3: Save transformed orders as Parquet
    output_path = BASE_DIR / "data" / "processed" / "orders.parquet"

    write_parquet(clean_orders, output_path)

    # Step 4: Verify the saved data
    saved_orders = pd.read_parquet(output_path)

    assert len(saved_orders) == len(clean_orders)
    assert saved_orders["order_id"].equals(clean_orders["order_id"])

    print(f"\nParquet verification passed: {len(saved_orders):,} rows")
    print(f"File location: {output_path}")
    print(f"File size: {output_path.stat().st_size / (1024 * 1024):.2f} MB")

    # Step 5: Load processed orders into PostgreSQL
    load_orders_incremental(output_path)

    print("\nPostgreSQL staging load completed!")
    print("\nPipeline Summary")
    print("----------------------")
    print(f"Raw orders: {len(raw_orders):,}")
    print(f"Clean orders: {len(clean_orders):,}")

    print("\nTransformed column types:")
    print(clean_orders.dtypes)

    print("\nSample transformed records:")
    print(
        clean_orders[
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp",
                "order_delivered_customer_date",
            ]
        ].head()
    )

    # Customer extraction
    raw_customers = extract_csv(CUSTOMERS_FILE)

    # Customer transformation
    clean_customers = transform_customers(raw_customers)

    # Save customers to Parquet
    customers_output = (
        BASE_DIR / "data" / "processed" / "customers.parquet"
    )

    write_parquet(clean_customers, customers_output)

    # Verify saved data
    saved_customers = pd.read_parquet(customers_output)

    assert len(saved_customers) == len(clean_customers)
    assert saved_customers["customer_id"].equals(
        clean_customers["customer_id"]
    )

    print("\nCustomer Pipeline Summary")
    print("-------------------------")
    print(f"Raw customers: {len(raw_customers):,}")
    print(f"Clean customers: {len(clean_customers):,}")
    print(f"Parquet records: {len(saved_customers):,}")
    print(f"File location: {customers_output}")

    # Load customers into PostgreSQL
    load_customers(customers_output)


    # Step 8: Process order items

    # Extract
    raw_order_items = extract_csv(ORDER_ITEMS_FILE)

    # Transform
    clean_order_items = transform_order_items(raw_order_items)

    # Save to Parquet
    order_items_output = (
        BASE_DIR / "data" / "processed" / "order_items.parquet"
    )

    write_parquet(clean_order_items, order_items_output)

    # Verify saved records
    saved_order_items = pd.read_parquet(order_items_output)

    assert len(saved_order_items) == len(clean_order_items)

    assert saved_order_items[
        ["order_id", "order_item_id"]
    ].equals(
        clean_order_items[["order_id", "order_item_id"]]
    )

    print("\nOrder Items Pipeline Summary")
    print("----------------------------")
    print(f"Raw order items: {len(raw_order_items):,}")
    print(f"Clean order items: {len(clean_order_items):,}")
    print(f"Parquet records: {len(saved_order_items):,}")
    print(f"File location: {order_items_output}")

    print("\nPostgreSQL customers staging load completed!")

    # Load order items into PostgreSQL
    load_order_items(order_items_output)

    print("\nPostgreSQL order items staging load completed!")


    # Step 9: Products ETL

    # Extract products
    raw_products = extract_csv(PRODUCTS_FILE)

    # Transform products
    clean_products = transform_products(raw_products)

    # Save transformed products as Parquet
    products_output = (
        BASE_DIR / "data" / "processed" / "products.parquet"
    )

    write_parquet(clean_products, products_output)

    # Read back and verify
    saved_products = pd.read_parquet(products_output)

    if len(saved_products) != len(clean_products):
        raise ValueError("Products Parquet row count mismatch")

    if saved_products["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs in Parquet")

    if saved_products["product_id"].isna().any():
        raise ValueError("Missing product IDs in Parquet")

    print("\nProducts Pipeline Summary")
    print("-------------------------")
    print(f"Raw products: {len(raw_products):,}")
    print(f"Clean products: {len(clean_products):,}")
    print(f"Parquet records: {len(saved_products):,}")
    print(f"Unknown categories: {(saved_products['product_category_name'] == 'unknown').sum():,}")
    print(f"File location: {products_output}")

    # Load products into PostgreSQL
    load_products(products_output)

    print("\nPostgreSQL products staging load completed!")



    # Step 10: Sellers ETL

    # Extract
    raw_sellers = extract_csv(SELLERS_FILE)

    # Transform
    clean_sellers = transform_sellers(raw_sellers)

    # Save to Parquet
    sellers_output = (
        BASE_DIR / "data" / "processed" / "sellers.parquet"
    )

    write_parquet(clean_sellers, sellers_output)

    # Verify saved data
    saved_sellers = pd.read_parquet(sellers_output)

    if len(saved_sellers) != len(clean_sellers):
        raise ValueError("Sellers Parquet row count mismatch")

    if saved_sellers["seller_id"].duplicated().any():
        raise ValueError("Duplicate seller IDs in Parquet")

    if saved_sellers["seller_id"].isna().any():
        raise ValueError("Missing seller IDs in Parquet")

    print("\nSellers Pipeline Summary")
    print("------------------------")
    print(f"Raw sellers: {len(raw_sellers):,}")
    print(f"Clean sellers: {len(clean_sellers):,}")
    print(f"Parquet records: {len(saved_sellers):,}")
    print(f"File location: {sellers_output}")

    # Load sellers into PostgreSQL
    load_sellers(sellers_output)

    print("\nPostgreSQL sellers staging load completed!")



    # Step 11: Payments ETL

    # Extract
    raw_payments = extract_csv(PAYMENTS_FILE)

    # Transform
    clean_payments = transform_payments(raw_payments)

    # Save to Parquet
    payments_output = (
        BASE_DIR / "data" / "processed" / "payments.parquet"
    )

    write_parquet(clean_payments, payments_output)

    # Verify saved data
    saved_payments = pd.read_parquet(payments_output)

    if len(saved_payments) != len(clean_payments):
        raise ValueError("Payments Parquet row count mismatch")

    if saved_payments.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any():
        raise ValueError("Duplicate payment records in Parquet")

    if saved_payments["order_id"].isna().any():
        raise ValueError("Missing order IDs in Parquet")

    print("\nPayments Pipeline Summary")
    print("-------------------------")
    print(f"Raw payments: {len(raw_payments):,}")
    print(f"Clean payments: {len(clean_payments):,}")
    print(f"Parquet records: {len(saved_payments):,}")
    print(f"File location: {payments_output}")

    # Load payments into PostgreSQL
    load_payments(payments_output)

    print("\nPostgreSQL payments staging load completed!")

if __name__ == "__main__":
    main()
