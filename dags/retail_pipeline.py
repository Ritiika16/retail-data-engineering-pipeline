import logging
import subprocess
from datetime import datetime , timedelta

from airflow.sdk import dag, task
from src.transform.spark_order_revenue import run_spark_order_revenue
logger = logging.getLogger(__name__)
@dag(
    dag_id="retail_data_pipeline",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    default_args={
        "retries": 2,
        "retry_delay": timedelta(minutes=2),
    },
    tags=["retail", "etl", "data-engineering"],
)
def retail_data_pipeline():


    @task
    def run_etl():
        logger.info("Starting Retail Data Engineering ETL...")

        try:
            subprocess.run(
                ["python", "-u", "src/main.py"],
                cwd="/opt/airflow/project",
                check=True,
            )

            logger.info("Retail ETL completed successfully!")

        except subprocess.CalledProcessError:
            logger.exception("ETL subprocess failed!")
            raise

        except Exception:
            logger.exception("Unexpected error during ETL execution!")
            raise



    @task
    def load_dimensions():
        from src.load.warehouse_loader import execute_sql_file

        dimension_scripts = [
            "load_dim_customers.sql",
            "load_dim_products.sql",
            "load_dim_sellers.sql",
            "load_dim_date.sql",
        ]

        try:
            logger.info("Starting warehouse dimension loading...")

            for filename in dimension_scripts:
                logger.info("Executing SQL file: %s", filename)
                execute_sql_file(filename)

            logger.info("All warehouse dimensions loaded successfully!")

        except Exception:
            logger.exception("Warehouse dimension loading failed!")
            raise



    @task
    def load_facts():
        from src.load.warehouse_loader import execute_sql_file

        fact_scripts = [
            "load_fact_order_items.sql",
            "load_fact_order_payments.sql",
        ]

        try:
            logger.info("Starting warehouse fact loading...")

            for filename in fact_scripts:
                logger.info("Executing SQL file: %s", filename)
                execute_sql_file(filename)

            logger.info("All warehouse facts loaded successfully!")

        except Exception:
            logger.exception("Warehouse fact loading failed!")
            raise




    @task
    def validate_warehouse():
        from src.load.data_quality import validate_warehouse as run_checks

        try:
            logger.info("Starting warehouse data quality validation...")

            run_checks()

            logger.info(
                "Warehouse data quality validation completed successfully!"
            )

        except Exception:
            logger.exception("Warehouse data quality validation failed!")
            raise

    @task
    def spark_order_revenue():
        run_spark_order_revenue()

    etl = run_etl()
    dimensions = load_dimensions()
    facts = load_facts()
    validation = validate_warehouse()
    spark_order_revenue_task = spark_order_revenue()

    etl >> dimensions >> facts >> validation >> spark_order_revenue_task

retail_data_pipeline()
