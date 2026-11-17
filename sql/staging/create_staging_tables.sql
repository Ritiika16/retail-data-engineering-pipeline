
-- Create staging schema
CREATE SCHEMA IF NOT EXISTS staging;

-- Create orders staging table
CREATE TABLE IF NOT EXISTS staging.orders (
    order_id VARCHAR(32) PRIMARY KEY,
    customer_id VARCHAR(32) NOT NULL,
    order_status VARCHAR(30) NOT NULL,

    order_purchase_timestamp TIMESTAMP NOT NULL,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP NOT NULL
);


-- Customers staging table
CREATE TABLE IF NOT EXISTS staging.customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL,
    customer_zip_code_prefix VARCHAR(5) NOT NULL,
    customer_city TEXT NOT NULL,
    customer_state VARCHAR(2) NOT NULL
);



CREATE TABLE IF NOT EXISTS staging.products (
    product_id VARCHAR(32) PRIMARY KEY,
    product_category_name TEXT NOT NULL,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g NUMERIC(12, 2),
    product_length_cm NUMERIC(12, 2),
    product_height_cm NUMERIC(12, 2),
    product_width_cm NUMERIC(12, 2)
);


-- Sellers staging table
CREATE TABLE IF NOT EXISTS staging.sellers (
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(5) NOT NULL,
    seller_city TEXT NOT NULL,
    seller_state VARCHAR(2) NOT NULL
);



CREATE TABLE IF NOT EXISTS staging.payments (
    order_id VARCHAR(32) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type VARCHAR(30) NOT NULL,
    payment_installments INTEGER NOT NULL,
    payment_value NUMERIC(12, 2) NOT NULL,

    CONSTRAINT pk_staging_payments
        PRIMARY KEY (order_id, payment_sequential),

    CONSTRAINT chk_payment_sequential
        CHECK (payment_sequential >= 1),

    CONSTRAINT chk_payment_installments
        CHECK (payment_installments >= 0),

    CONSTRAINT chk_payment_value
        CHECK (payment_value >= 0)
);
