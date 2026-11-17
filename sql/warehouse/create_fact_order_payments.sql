
CREATE TABLE IF NOT EXISTS warehouse.fact_order_payments (

    payment_key BIGINT
        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    order_id VARCHAR(32) NOT NULL,

    payment_sequential INTEGER NOT NULL,

    customer_key BIGINT NOT NULL
        REFERENCES warehouse.dim_customers(customer_key),

    order_date_key INTEGER NOT NULL
        REFERENCES warehouse.dim_date(date_key),

    payment_type VARCHAR(30) NOT NULL,

    payment_installments INTEGER NOT NULL,

    payment_value NUMERIC(12, 2) NOT NULL,

    CONSTRAINT uq_fact_order_payment
        UNIQUE (order_id, payment_sequential),

    CONSTRAINT chk_fact_payment_sequential
        CHECK (payment_sequential >= 1),

    CONSTRAINT chk_fact_payment_installments
        CHECK (payment_installments >= 0),

    CONSTRAINT chk_fact_payment_value
        CHECK (payment_value >= 0)

);
