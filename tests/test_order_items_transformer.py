
import pandas as pd
import pytest

from src.transform.order_items_transformer import transform_order_items


@pytest.fixture
def sample_order_items():
    return pd.DataFrame({
        "order_id": ["ORD001", "ORD001", "ORD002"],
        "order_item_id": [1, 2, 1],
        "product_id": ["PROD01", "PROD02", "PROD03"],
        "seller_id": ["SELL01", "SELL02", "SELL01"],
        "shipping_limit_date": [
            "2018-01-10 10:00:00",
            "2018-01-10 10:00:00",
            "2018-01-11 12:00:00",
        ],
        "price": [100.0, 200.0, 150.0],
        "freight_value": [10.0, 20.0, 15.0],
    })


def test_valid_order_items(sample_order_items):
    result = transform_order_items(sample_order_items)

    assert len(result) == 3
    assert not result.duplicated(
        subset=["order_id", "order_item_id"]
    ).any()


def test_datetime_conversion(sample_order_items):
    result = transform_order_items(sample_order_items)

    assert pd.api.types.is_datetime64_any_dtype(
        result["shipping_limit_date"]
    )


def test_duplicate_composite_key(sample_order_items):
    sample_order_items.loc[1, "order_item_id"] = 1

    with pytest.raises(ValueError, match="Duplicate order items"):
        transform_order_items(sample_order_items)


def test_missing_identifier(sample_order_items):
    sample_order_items.loc[0, "product_id"] = None

    with pytest.raises(ValueError, match="Missing order item identifiers"):
        transform_order_items(sample_order_items)


def test_negative_price(sample_order_items):
    sample_order_items.loc[0, "price"] = -100

    with pytest.raises(ValueError, match="Negative price"):
        transform_order_items(sample_order_items)


def test_invalid_freight_value(sample_order_items):

    # Allow the column to contain mixed data types
    sample_order_items["freight_value"] = (
        sample_order_items["freight_value"].astype(object)
    )
    sample_order_items.loc[0, "freight_value"] = "invalid"

    with pytest.raises(ValueError, match="Invalid freight_value"):
        transform_order_items(sample_order_items)


def test_invalid_shipping_date(sample_order_items):
    sample_order_items.loc[0, "shipping_limit_date"] = "not-a-date"

    with pytest.raises(ValueError, match="Invalid shipping limit dates"):
        transform_order_items(sample_order_items)


def test_missing_required_column(sample_order_items):
    sample_order_items = sample_order_items.drop(columns=["seller_id"])

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_order_items(sample_order_items)
