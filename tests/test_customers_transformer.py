
import pandas as pd
import pytest

from src.transform.customers_transformer import transform_customers


@pytest.fixture
def sample_customers():
    return pd.DataFrame({
        "customer_id": ["C001", "C002"],
        "customer_unique_id": ["U001", "U002"],
        "customer_zip_code_prefix": [1234, 56789],
        "customer_city": [" São Paulo ", "Rio De Janeiro"],
        "customer_state": ["sp", "rj"],
    })


def test_valid_customers(sample_customers):
    result = transform_customers(sample_customers)

    assert len(result) == 2
    assert result["customer_id"].is_unique


def test_city_and_state_normalization(sample_customers):
    result = transform_customers(sample_customers)

    assert result["customer_city"].iloc[0] == "são paulo"
    assert result["customer_state"].iloc[0] == "SP"


def test_zip_code_formatting(sample_customers):
    result = transform_customers(sample_customers)

    assert result["customer_zip_code_prefix"].iloc[0] == "01234"
    assert result["customer_zip_code_prefix"].iloc[1] == "56789"


def test_duplicate_customer_id(sample_customers):
    sample_customers.loc[1, "customer_id"] = "C001"

    with pytest.raises(ValueError, match="Duplicate customer IDs"):
        transform_customers(sample_customers)


def test_missing_customer_id(sample_customers):
    sample_customers.loc[0, "customer_id"] = None

    with pytest.raises(ValueError, match="Missing customer IDs"):
        transform_customers(sample_customers)


def test_missing_required_column(sample_customers):
    sample_customers = sample_customers.drop(
        columns=["customer_unique_id"]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_customers(sample_customers)
