
import pandas as pd
import pytest

from src.transform.sellers_transformer import transform_sellers


@pytest.fixture
def sample_sellers():
    return pd.DataFrame({
        "seller_id": ["SELL001", "SELL002", "SELL003"],
        "seller_zip_code_prefix": ["1234", "45678", "9876"],
        "seller_city": [
            " São Paulo ",
            "RIO DE JANEIRO",
            " Curitiba "
        ],
        "seller_state": ["sp", "RJ", "pr"],
    })


def test_valid_sellers(sample_sellers):
    result = transform_sellers(sample_sellers)

    assert len(result) == 3
    assert result["seller_id"].is_unique


def test_zip_code_normalization(sample_sellers):
    result = transform_sellers(sample_sellers)

    assert result.loc[0, "seller_zip_code_prefix"] == "01234"
    assert result.loc[1, "seller_zip_code_prefix"] == "45678"


def test_city_normalization(sample_sellers):
    result = transform_sellers(sample_sellers)

    assert result.loc[0, "seller_city"] == "são paulo"
    assert result.loc[1, "seller_city"] == "rio de janeiro"


def test_state_normalization(sample_sellers):
    result = transform_sellers(sample_sellers)

    assert result.loc[0, "seller_state"] == "SP"
    assert result.loc[2, "seller_state"] == "PR"


def test_duplicate_seller_ids(sample_sellers):
    sample_sellers.loc[1, "seller_id"] = "SELL001"

    with pytest.raises(ValueError, match="Duplicate seller IDs"):
        transform_sellers(sample_sellers)


def test_missing_seller_id(sample_sellers):
    sample_sellers.loc[0, "seller_id"] = None

    with pytest.raises(ValueError, match="Missing seller IDs"):
        transform_sellers(sample_sellers)


def test_missing_location(sample_sellers):
    sample_sellers.loc[0, "seller_city"] = None

    with pytest.raises(ValueError, match="Missing seller location"):
        transform_sellers(sample_sellers)


def test_missing_required_column(sample_sellers):
    sample_sellers = sample_sellers.drop(columns=["seller_state"])

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_sellers(sample_sellers)


def test_original_dataframe_unchanged(sample_sellers):
    original = sample_sellers.copy(deep=True)

    transform_sellers(sample_sellers)

    pd.testing.assert_frame_equal(sample_sellers, original)
