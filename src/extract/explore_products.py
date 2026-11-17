
from pathlib import Path
from src.extract.csv_extractor import extract_csv

BASE_DIR = Path(__file__).resolve().parents[2]

PRODUCTS_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "olist"
    / "olist_products_dataset.csv"
)

def main():
    df = extract_csv(PRODUCTS_FILE)

    print("\nPRODUCTS DATASET PROFILE")
    print("------------------------")

    print(f"\nTotal records: {len(df):,}")

    print("\nColumn names and data types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isna().sum())

    print("\nDuplicate product IDs:")
    print(df["product_id"].duplicated().sum())

    print("\nSample records:")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
