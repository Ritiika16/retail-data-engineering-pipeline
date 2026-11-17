
from pathlib import Path
import logging
import zipfile
import pandas as pd

logger = logging.getLogger(__name__)


def extract_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Extract a CSV file into a pandas DataFrame.

    Supports regular CSV files and ZIP-compressed CSV files.
    """

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Source file not found: {path}")

    logger.info("Extracting file: %s", path.name)

    if zipfile.is_zipfile(path):
        df = pd.read_csv(path, compression="zip")
    else:
        df = pd.read_csv(path, encoding="utf-8")

    logger.info(
        "Extracted %s rows and %s columns from %s",
        len(df),
        len(df.columns),
        path.name,
    )

    return df
