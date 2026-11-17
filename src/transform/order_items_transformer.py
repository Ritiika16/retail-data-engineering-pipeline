
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_order_items(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting order items transformation")

    cleaned = df.copy()

    required_columns = [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ]

    missing_columns = set(required_columns) - set(cleaned.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Validate identifiers
    if cleaned[
        ["order_id", "order_item_id", "product_id", "seller_id"]
    ].isna().any().any():
        raise ValueError("Missing order item identifiers detected")

    # Composite primary key validation
    if cleaned.duplicated(
        subset=["order_id", "order_item_id"]
    ).any():
        raise ValueError("Duplicate order items detected")

    # Convert shipping deadline to datetime
    cleaned["shipping_limit_date"] = pd.to_datetime(
        cleaned["shipping_limit_date"],
        format="%Y-%m-%d %H:%M:%S",
        errors="coerce",
    )

    if cleaned["shipping_limit_date"].isna().any():
        raise ValueError("Invalid shipping limit dates detected")

    # Validate numeric values
    for column in ["price", "freight_value"]:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce",
        )

        if cleaned[column].isna().any():
            raise ValueError(f"Invalid {column} values detected")

        if (cleaned[column] < 0).any():
            raise ValueError(f"Negative {column} values detected")

    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Order items transformation completed: %s rows",
        len(cleaned),
    )

    return cleaned
