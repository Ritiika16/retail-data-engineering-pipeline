
BEGIN;

INSERT INTO warehouse.fact_order_payments (
    order_id,
    payment_sequential,
    customer_key,
    order_date_key,
    payment_type,
    payment_installments,
    payment_value
)
SELECT
    p.order_id,
    p.payment_sequential,
    dc.customer_key,
    dd.date_key,
    p.payment_type,
    p.payment_installments,
    p.payment_value

FROM staging.payments p

JOIN staging.orders o
    ON p.order_id = o.order_id

JOIN warehouse.dim_customers dc
    ON o.customer_id = dc.customer_id

JOIN warehouse.dim_date dd
    ON CAST(o.order_purchase_timestamp AS DATE) = dd.full_date

ON CONFLICT (order_id, payment_sequential)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    order_date_key = EXCLUDED.order_date_key,
    payment_type = EXCLUDED.payment_type,
    payment_installments = EXCLUDED.payment_installments,
    payment_value = EXCLUDED.payment_value;

COMMIT;
