
from pathlib import Path
import sys
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.transform.orders_transformer import transform_orders


def sample_orders():
    return pd.DataFrame({
        "order_id": ["ORD001", "ORD002"],
        "customer_id": ["C001", "C002"],
        "order_status": ["delivered", "shipped"],
        "order_purchase_timestamp": [
            "2018-01-15 10:30:00",
            "2018-01-16 11:00:00",
        ],
        "order_approved_at": [None, None],
        "order_delivered_carrier_date": [None, None],
        "order_delivered_customer_date": [None, None],
        "order_estimated_delivery_date": [
            "2018-01-25",
            "2018-01-26",
        ],
    })


def test_transform_orders():
    result = transform_orders(sample_orders())

    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(
        result["order_purchase_timestamp"]
    )


def test_missing_delivery_date():
    result = transform_orders(sample_orders())

    assert pd.isna(
        result.loc[0, "order_delivered_customer_date"]
    )


def test_duplicate_order_ids():
    df = sample_orders()
    df.loc[1, "order_id"] = "ORD001"

    with pytest.raises(ValueError, match="Duplicate order IDs"):
        transform_orders(df)


def test_invalid_purchase_timestamp():
    df = sample_orders()
    df.loc[0, "order_purchase_timestamp"] = "invalid-date"

    with pytest.raises(ValueError, match="purchase timestamps"):
        transform_orders(df)
