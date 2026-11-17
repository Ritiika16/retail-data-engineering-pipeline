# End-to-End Retail Data Engineering Pipeline

An end-to-end data engineering project built using **Python, PostgreSQL, Apache Airflow, PySpark, SQL, Parquet, and Docker**, processing the Brazilian Olist e-commerce dataset.

The project demonstrates data ingestion, transformation, warehouse modeling, incremental loading, workflow orchestration, automated data quality validation, and distributed data processing concepts.

## 1. Project Overview

This pipeline transforms raw e-commerce CSV datasets into structured analytical data using a multi-stage ETL architecture.

**Key capabilities:**
- Automated CSV extraction and data cleaning
- Parquet-based intermediate storage
- PostgreSQL staging and dimensional data warehouse
- Incremental order loading using UPSERT
- Airflow workflow orchestration with retries and logging
- Automated warehouse data quality checks
- PySpark-based order revenue aggregation
- Automated testing with pytest

## 2. Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python, SQL |
| Data Processing | pandas, PySpark |
| Database | PostgreSQL |
| Orchestration | Apache Airflow |
| Storage | CSV, Apache Parquet |
| Infrastructure | Docker, Docker Compose |
| Testing | pytest |
| Version Control | Git, GitHub |

## 3. Architecture

The pipeline follows this workflow:

```text
Olist E-commerce CSV Dataset
           |
           v
Python Extraction & Transformation
           |
           v
Processed Parquet Files
           |
           +------------------------+
           |                        |
           v                        v
PostgreSQL Staging              PySpark
           |                        |
           v                        v
Dimensional Warehouse       Revenue Aggregation
           |                        |
           v                        v
Data Quality Validation     Revenue Parquet Output
```

Apache Airflow orchestrates the pipeline, while Docker provides a reproducible execution environment for Airflow and Spark.

See [Architecture Documentation](docs/architecture.md).

## 4. Dataset

**Source:** Brazilian E-Commerce Public Dataset by Olist.

The project processes six primary datasets:

| Dataset | Records |
|---|---:|
| Orders | 99,441 |
| Customers | 99,441 |
| Order Items | 112,650 |
| Products | 32,951 |
| Sellers | 3,095 |
| Payments | 103,886 |

The data contains customer information, orders, products, sellers, payments, and transactional records.

## 5. ETL Pipeline

### Extraction

Python-based extraction reads raw CSV data from the local data directory.

### Transformation

The transformation layer performs data cleaning and validation, including:

- Missing-value handling
- Duplicate detection
- Data type conversion
- Date and timestamp normalization
- Numeric value validation
- Customer and seller location normalization

Processed datasets are stored in Apache Parquet format.

### Loading

The loading layer writes transformed datasets into PostgreSQL staging tables.

Order records use an incremental UPSERT strategy to support repeatable loads and update existing records when values change.

Other staging datasets use full-refresh loading.

## 6. Data Warehouse

The project implements a dimensional data warehouse using PostgreSQL.

**Dimension tables:**
- `dim_customers`
- `dim_products`
- `dim_sellers`
- `dim_date`

**Fact tables:**
- `fact_order_items`
- `fact_order_payments`

The warehouse supports analytical queries across customers, products, sellers, dates, orders, and payments.

## 7. Apache Airflow Orchestration

The pipeline is orchestrated through the `retail_data_pipeline` DAG.

**Task execution order:**

```text
run_etl
   |
   v
load_dimensions
   |
   v
load_facts
   |
   v
validate_warehouse
   |
   v
spark_order_revenue
```

The DAG includes:
- Task dependencies
- Automatic retries
- Error handling
- Execution logging
- Warehouse validation
- PySpark transformation execution

The DAG is configured for manual triggering.

## 8. Data Quality

The warehouse validation stage executes **20 automated data quality checks**.

Validation is integrated into Airflow so failures can stop downstream execution.

Additional pytest tests cover extraction and transformation behavior, including invalid records, duplicates, missing values, and normalization.

## 9. PySpark Processing

PySpark processes the transformed Parquet datasets to generate an order-level revenue dataset.

The transformation:
1. Reads orders and order items.
2. Joins the datasets using `order_id`.
3. Groups records by order.
4. Calculates item count and total item revenue.
