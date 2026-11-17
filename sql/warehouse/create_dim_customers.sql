
CREATE TABLE IF NOT EXISTS warehouse.dim_customers (

    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    customer_id VARCHAR(32) NOT NULL UNIQUE,

    customer_unique_id VARCHAR(32) NOT NULL,

    customer_zip_code_prefix VARCHAR(5),

    customer_city TEXT,

    customer_state VARCHAR(2)

);
