
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_payments(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting payments transformation")

    cleaned = df.copy()

    required_columns = [
        "order_id",
        "payment_sequential",
        "payment_type",
        "payment_installments",
        "payment_value",
    ]

    missing_columns = set(required_columns) - set(cleaned.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Validate identifiers
    if cleaned["order_id"].isna().any():
        raise ValueError("Missing order IDs detected")

    if cleaned.duplicated(
        subset=["order_id", "payment_sequential"]
    ).any():
        raise ValueError("Duplicate payment records detected")

    # Validate integer fields
    for column in ["payment_sequential", "payment_installments"]:
        numeric = pd.to_numeric(cleaned[column], errors="coerce")

        if numeric.isna().any():
            raise ValueError(f"Invalid {column} values detected")

        if (numeric % 1 != 0).any():
            raise ValueError(f"Non-integer {column} values detected")

        if column == "payment_sequential" and (numeric < 1).any():
            raise ValueError("Invalid payment sequence detected")

        if column == "payment_installments" and (numeric < 0).any():
            raise ValueError("Negative installments detected")

        cleaned[column] = numeric.astype("int64")

    # Normalize payment types
    cleaned["payment_type"] = (
        cleaned["payment_type"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    if (
        cleaned["payment_type"].isna().any()
        or cleaned["payment_type"].eq("").any()
    ):
        raise ValueError("Missing payment types detected")

    # Validate payment values
    cleaned["payment_value"] = pd.to_numeric(
        cleaned["payment_value"],
        errors="coerce"
    )

    if cleaned["payment_value"].isna().any():
        raise ValueError("Invalid payment values detected")

    if (cleaned["payment_value"] < 0).any():
        raise ValueError("Negative payment values detected")

    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Payments transformation completed: %s rows",
        len(cleaned)
    )

    return cleaned
