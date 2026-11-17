
import logging
import pandas as pd

logger = logging.getLogger(__name__)

DATE_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and validate raw orders data.
    """

    logger.info("Starting orders transformation")

    # Work on a copy to preserve the raw DataFrame
    cleaned = df.copy()

    # Convert string timestamps into datetime values
    for column in DATE_COLUMNS:
        cleaned[column] = pd.to_datetime(
            cleaned[column],
            format="%Y-%m-%d %H:%M:%S",
            errors="coerce"
        )

    # Validate order IDs
    if cleaned["order_id"].isna().any():
        raise ValueError("Missing order IDs detected")

    if cleaned["order_id"].duplicated().any():
        raise ValueError("Duplicate order IDs detected")

    # Purchase timestamp is required
    if cleaned["order_purchase_timestamp"].isna().any():
        raise ValueError(
            "Missing or invalid purchase timestamps detected"
        )

    # Check row count preservation
    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Orders transformation completed: %s rows",
        len(cleaned)
    )

    return cleaned
