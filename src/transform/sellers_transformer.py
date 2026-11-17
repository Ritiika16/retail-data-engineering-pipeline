
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_sellers(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting sellers transformation")

    cleaned = df.copy()

    required_columns = [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ]

    missing_columns = set(required_columns) - set(cleaned.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if cleaned["seller_id"].isna().any():
        raise ValueError("Missing seller IDs detected")

    if cleaned["seller_id"].duplicated().any():
        raise ValueError("Duplicate seller IDs detected")

    if cleaned[
        ["seller_zip_code_prefix", "seller_city", "seller_state"]
    ].isna().any().any():
        raise ValueError("Missing seller location data detected")

    # Normalize ZIP codes to five-character strings
    cleaned["seller_zip_code_prefix"] = (
        cleaned["seller_zip_code_prefix"]
        .astype("string")
        .str.strip()
        .str.zfill(5)
    )

    # Normalize cities and states
    cleaned["seller_city"] = (
        cleaned["seller_city"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    cleaned["seller_state"] = (
        cleaned["seller_state"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Sellers transformation completed: %s rows",
        len(cleaned)
    )

    return cleaned
