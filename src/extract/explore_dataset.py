
from pathlib import Path
import zipfile
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw" / "olist"

csv_files = sorted(DATA_DIR.glob("*.csv"))

for file in csv_files:
    print(f"\n{'=' * 60}")
    print(f"Dataset: {file.name}")

    # Detect compressed files, even if they have a .csv extension
    if zipfile.is_zipfile(file):
        print("ZIP archive detected. Reading compressed CSV.")
        df = pd.read_csv(file, compression="zip")
    else:
        df = pd.read_csv(file, encoding="utf-8")

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")
    print(f"Duplicate rows: {df.duplicated().sum():,}")

    print("\nColumn Information:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())
