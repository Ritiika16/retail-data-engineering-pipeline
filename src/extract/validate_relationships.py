
from pathlib import Path
import zipfile
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw" / "olist"


def read_dataset(filename):
    path = DATA_DIR / filename

    if zipfile.is_zipfile(path):
        return pd.read_csv(path, compression="zip")

    return pd.read_csv(path)


customers = read_dataset("olist_customers_dataset.csv")
orders = read_dataset("olist_orders_dataset.csv")
order_items = read_dataset("olist_order_items_dataset.csv")
products = read_dataset("olist_products_dataset.csv")
sellers = read_dataset("olist_sellers_dataset.csv")

print("\n=== PRIMARY KEY VALIDATION ===")

for name, df, key in [
    ("Customers", customers, "customer_id"),
    ("Orders", orders, "order_id"),
    ("Products", products, "product_id"),
    ("Sellers", sellers, "seller_id"),
]:
    print(f"{name} - Duplicate {key}: {df[key].duplicated().sum()}")

print("\n=== FOREIGN KEY VALIDATION ===")

checks = [
    ("Orders -> Customers", orders, "customer_id",
     customers, "customer_id"),
    ("Order Items -> Orders", order_items, "order_id",
     orders, "order_id"),
    ("Order Items -> Products", order_items, "product_id",
     products, "product_id"),
    ("Order Items -> Sellers", order_items, "seller_id",
     sellers, "seller_id"),
]

for name, child, child_key, parent, parent_key in checks:
    unmatched = ~child[child_key].isin(parent[parent_key])

    print(f"{name}: {unmatched.sum()} unmatched rows")

print("\n=== ORDER ITEM GRAIN ===")

print(
    "Duplicate (order_id, order_item_id):",
    order_items.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()
)

print(
    "Orders with multiple items:",
    (order_items.groupby("order_id").size() > 1).sum()
)
