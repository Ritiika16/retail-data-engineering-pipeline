
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting customers transformation")

    cleaned = df.copy()

    required_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    missing_columns = set(required_columns) - set(cleaned.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if cleaned["customer_id"].isna().any():
        raise ValueError("Missing customer IDs detected")

    if cleaned["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer IDs detected")

    if cleaned[required_columns].isna().any().any():
        raise ValueError("Missing customer information detected")

    # Normalize text values
    cleaned["customer_city"] = (
        cleaned["customer_city"].str.strip().str.lower()
    )

    cleaned["customer_state"] = (
        cleaned["customer_state"].str.strip().str.upper()
    )

    # Keep ZIP code prefixes as five-character strings
    cleaned["customer_zip_code_prefix"] = (
        cleaned["customer_zip_code_prefix"]
        .astype(str)
        .str.zfill(5)
    )

    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Customers transformation completed: %s rows",
        len(cleaned),
    )

    return cleaned
