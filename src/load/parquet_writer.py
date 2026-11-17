
from pathlib import Path
import logging
import pandas as pd

logger = logging.getLogger(__name__)


def write_parquet(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Write a DataFrame to a Snappy-compressed Parquet file."""

    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        path,
        engine="pyarrow",
        compression="snappy",
        index=False,
    )

    logger.info("Saved %s rows to %s", len(df), path)

    return path
