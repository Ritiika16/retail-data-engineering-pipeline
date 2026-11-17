
import pandas as pd
import pytest

from src.transform.payments_transformer import transform_payments


@pytest.fixture
def sample_payments():
    return pd.DataFrame({
        "order_id": ["ORD001", "ORD001", "ORD002"],
        "payment_sequential": [1, 2, 1],
        "payment_type": [
            " Credit_Card ",
            "voucher",
            "BOLETO"
        ],
        "payment_installments": [3, 0, 1],
        "payment_value": [100.50, 50.00, 200.00],
    })


# Test 1: Valid payments are preserved
def test_valid_payments(sample_payments):
    result = transform_payments(sample_payments)

    assert len(result) == 3
    assert not result.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any()


# Test 2: Payment types are normalized
def test_payment_type_normalization(sample_payments):
    result = transform_payments(sample_payments)

    assert result.loc[0, "payment_type"] == "credit_card"
    assert result.loc[2, "payment_type"] == "boleto"


# Test 3: Duplicate composite keys are rejected
def test_duplicate_payment_records(sample_payments):
    sample_payments.loc[1, "payment_sequential"] = 1

    with pytest.raises(
        ValueError,
        match="Duplicate payment records"
    ):
        transform_payments(sample_payments)


# Test 4: Missing order IDs are rejected
def test_missing_order_id(sample_payments):
    sample_payments.loc[0, "order_id"] = None

    with pytest.raises(
        ValueError,
        match="Missing order IDs"
    ):
        transform_payments(sample_payments)


# Test 5: Negative payment values are rejected
def test_negative_payment_value(sample_payments):
    sample_payments.loc[0, "payment_value"] = -100

    with pytest.raises(
        ValueError,
        match="Negative payment values"
    ):
        transform_payments(sample_payments)


# Test 6: Invalid payment values are rejected
def test_invalid_payment_value(sample_payments):
    sample_payments["payment_value"] = (
        sample_payments["payment_value"].astype(object)
    )
    sample_payments.loc[0, "payment_value"] = "invalid"

    with pytest.raises(
        ValueError,
        match="Invalid payment values"
    ):
        transform_payments(sample_payments)


# Test 7: Invalid payment sequence is rejected
def test_invalid_payment_sequence(sample_payments):
    sample_payments.loc[0, "payment_sequential"] = 0

    with pytest.raises(
        ValueError,
        match="Invalid payment sequence"
    ):
        transform_payments(sample_payments)


# Test 8: Negative installments are rejected
def test_negative_installments(sample_payments):
    sample_payments.loc[0, "payment_installments"] = -1

    with pytest.raises(
        ValueError,
        match="Negative installments"
    ):
        transform_payments(sample_payments)


# Test 9: Missing required columns are rejected
def test_missing_required_column(sample_payments):
    sample_payments = sample_payments.drop(
        columns=["payment_type"]
    )

    with pytest.raises(
        ValueError,
        match="Missing required columns"
    ):
        transform_payments(sample_payments)


# Test 10: Original DataFrame is not modified
def test_original_dataframe_unchanged(sample_payments):
    original = sample_payments.copy(deep=True)

    transform_payments(sample_payments)

    pd.testing.assert_frame_equal(
        sample_payments,
        original
    )
