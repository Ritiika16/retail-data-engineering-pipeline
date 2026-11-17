
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Starting products transformation")

    cleaned = df.copy()

    required_columns = [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    missing_columns = set(required_columns) - set(cleaned.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Validate product identifiers
    if cleaned["product_id"].isna().any():
        raise ValueError("Missing product IDs detected")

    if cleaned["product_id"].duplicated().any():
        raise ValueError("Duplicate product IDs detected")

    # Normalize category names
    cleaned["product_category_name"] = (
        cleaned["product_category_name"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace("", pd.NA)
        .fillna("unknown")
    )

    # Convert numeric attributes
    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce"
        )

        # Negative measurements are invalid
        if (cleaned[column].dropna() < 0).any():
            raise ValueError(
                f"Negative values detected in {column}"
            )

    # Preserve missing measurements as NULL
    # rather than replacing them with zero

    if len(cleaned) != len(df):
        raise ValueError("Unexpected row count change")

    logger.info(
        "Products transformation completed: %s rows",
        len(cleaned)
    )

    return cleaned
