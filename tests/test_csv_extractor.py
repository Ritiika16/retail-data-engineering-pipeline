
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.extract.csv_extractor import extract_csv


def test_extract_customers():
    file_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "olist"
        / "olist_customers_dataset.csv"
    )

    df = extract_csv(file_path)

    assert len(df) == 99441
    assert "customer_id" in df.columns
    assert df["customer_id"].is_unique


def test_extract_compressed_orders():
    file_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "olist"
        / "olist_orders_dataset.csv"
    )

    df = extract_csv(file_path)

    assert len(df) == 99441
    assert "order_id" in df.columns
