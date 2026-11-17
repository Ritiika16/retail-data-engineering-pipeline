
import pandas as pd
import pytest

from src.transform.products_transformer import transform_products


@pytest.fixture
def sample_products():
    return pd.DataFrame({
        "product_id": ["PROD001", "PROD002", "PROD003"],
        "product_category_name": [
            "Electronics",
            "  Furniture  ",
            None
        ],
        "product_name_lenght": [40.0, 35.0, None],
        "product_description_lenght": [250.0, 180.0, None],
        "product_photos_qty": [2.0, 1.0, None],
        "product_weight_g": [500.0, 1000.0, None],
        "product_length_cm": [20.0, 30.0, None],
        "product_height_cm": [10.0, 15.0, None],
        "product_width_cm": [15.0, 25.0, None],
    })


# Test 1: Valid records are preserved
def test_valid_products(sample_products):
    result = transform_products(sample_products)

    assert len(result) == 3
    assert result["product_id"].is_unique


# Test 2: Categories are normalized
def test_category_normalization(sample_products):
    result = transform_products(sample_products)

    assert result.loc[0, "product_category_name"] == "electronics"
    assert result.loc[1, "product_category_name"] == "furniture"


# Test 3: Missing categories become "unknown"
def test_missing_category(sample_products):
    result = transform_products(sample_products)

    assert result.loc[2, "product_category_name"] == "unknown"


# Test 4: Missing numeric values remain missing
def test_missing_numeric_values(sample_products):
    result = transform_products(sample_products)

    assert pd.isna(result.loc[2, "product_weight_g"])
    assert pd.isna(result.loc[2, "product_photos_qty"])


# Test 5: Duplicate product IDs are rejected
def test_duplicate_product_ids(sample_products):
    sample_products.loc[1, "product_id"] = "PROD001"

    with pytest.raises(ValueError, match="Duplicate product IDs"):
        transform_products(sample_products)


# Test 6: Missing product IDs are rejected
def test_missing_product_ids(sample_products):
    sample_products.loc[0, "product_id"] = None

    with pytest.raises(ValueError, match="Missing product IDs"):
        transform_products(sample_products)


# Test 7: Negative measurements are rejected
def test_negative_weight(sample_products):
    sample_products.loc[0, "product_weight_g"] = -500

    with pytest.raises(ValueError, match="Negative values"):
        transform_products(sample_products)


# Test 8: Missing required columns are rejected
def test_missing_required_column(sample_products):
    sample_products = sample_products.drop(
        columns=["product_width_cm"]
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        transform_products(sample_products)


# Test 9: Numeric strings are converted
def test_numeric_conversion(sample_products):
    sample_products["product_weight_g"] = (
        sample_products["product_weight_g"].astype(object)
    )
    sample_products.loc[0, "product_weight_g"] = "750"

    result = transform_products(sample_products)

    assert result.loc[0, "product_weight_g"] == 750.0


# Test 10: Original DataFrame is not modified
def test_original_dataframe_unchanged(sample_products):
    original = sample_products.copy(deep=True)

    transform_products(sample_products)

    pd.testing.assert_frame_equal(sample_products, original)
