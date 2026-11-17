
from pathlib import Path

from sqlalchemy import text

from src.load.postgres_loader import get_engine


BASE_DIR = Path(__file__).resolve().parents[2]
WAREHOUSE_SQL_DIR = BASE_DIR / "sql" / "warehouse"


def execute_sql_file(filename: str) -> None:
    """Execute a warehouse SQL file inside a database transaction."""

    sql_path = WAREHOUSE_SQL_DIR / filename

    if not sql_path.is_file():
        raise FileNotFoundError(f"SQL file not found: {sql_path}")

    sql = sql_path.read_text(encoding="utf-8-sig").strip()

    # Some existing SQL files contain BEGIN/COMMIT.
    # Let SQLAlchemy manage the transaction instead.
    statements = [
        statement.strip()
        for statement in sql.split(";")
        if statement.strip()
    ]

    statements = [
        statement
        for statement in statements
        if statement.upper() not in ("BEGIN", "COMMIT")
    ]

    engine = get_engine()

    try:
        with engine.begin() as connection:
            for statement in statements:
                connection.execute(text(statement))

        print(f"Successfully executed: {filename}")

    finally:
        engine.dispose()
