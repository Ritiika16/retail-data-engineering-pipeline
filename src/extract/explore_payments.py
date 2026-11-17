
from pathlib import Path
from src.extract.csv_extractor import extract_csv

BASE_DIR = Path(__file__).resolve().parents[2]

PAYMENTS_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "olist"
    / "olist_order_payments_dataset.csv"
)


def main():
    df = extract_csv(PAYMENTS_FILE)

    print("\nPAYMENTS DATASET PROFILE")
    print("------------------------")

    print(f"\nTotal records: {len(df):,}")

    print("\nColumn names and data types:")
    print(df.dtypes)

    print("\nMissing values per column:")
    print(df.isna().sum())

    print("\nDuplicate (order_id, payment_sequential) combinations:")
    print(
        df.duplicated(
            subset=["order_id", "payment_sequential"]
        ).sum()
    )

    print("\nPayment types:")
    print(df["payment_type"].value_counts(dropna=False))

    print("\nPayment value statistics:")
    print(df["payment_value"].describe())

    print("\nSample records:")
    print(df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()
