
CREATE TABLE IF NOT EXISTS warehouse.fact_order_items (

    order_item_key BIGINT
        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,

    order_item_id INTEGER NOT NULL,

    customer_key BIGINT NOT NULL
        REFERENCES warehouse.dim_customers(customer_key),

    product_key BIGINT NOT NULL
        REFERENCES warehouse.dim_products(product_key),

    seller_key BIGINT NOT NULL
        REFERENCES warehouse.dim_sellers(seller_key),

    order_date_key INTEGER NOT NULL
        REFERENCES warehouse.dim_date(date_key),

    price NUMERIC(12, 2) NOT NULL,

    freight_value NUMERIC(12, 2) NOT NULL,

    quantity INTEGER NOT NULL DEFAULT 1,

    total_item_value NUMERIC(12, 2)
        GENERATED ALWAYS AS (price + freight_value) STORED,

    CONSTRAINT uq_fact_order_item
        UNIQUE (order_id, order_item_id),

    CONSTRAINT chk_item_price
        CHECK (price >= 0),

    CONSTRAINT chk_item_freight
        CHECK (freight_value >= 0),

    CONSTRAINT chk_item_quantity
        CHECK (quantity > 0)

);
