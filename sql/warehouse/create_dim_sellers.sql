
CREATE TABLE IF NOT EXISTS warehouse.dim_sellers (

    seller_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    seller_id VARCHAR(32) NOT NULL UNIQUE,

    seller_zip_code_prefix VARCHAR(5) NOT NULL,

    seller_city TEXT NOT NULL,

    seller_state VARCHAR(2) NOT NULL

);
