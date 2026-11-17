
BEGIN;

INSERT INTO warehouse.fact_order_items (
    order_id,
    order_item_id,
    customer_key,
    product_key,
    seller_key,
    order_date_key,
    price,
    freight_value,
    quantity
)
SELECT
    oi.order_id,
    oi.order_item_id,
    dc.customer_key,
    dp.product_key,
    ds.seller_key,
    dd.date_key,
    oi.price,
    oi.freight_value,
    1 AS quantity

FROM staging.order_items oi

JOIN staging.orders o
    ON oi.order_id = o.order_id

JOIN warehouse.dim_customers dc
    ON o.customer_id = dc.customer_id

JOIN warehouse.dim_products dp
    ON oi.product_id = dp.product_id

JOIN warehouse.dim_sellers ds
    ON oi.seller_id = ds.seller_id

JOIN warehouse.dim_date dd
    ON CAST(o.order_purchase_timestamp AS DATE) = dd.full_date

ON CONFLICT (order_id, order_item_id)
DO UPDATE SET
    customer_key = EXCLUDED.customer_key,
    product_key = EXCLUDED.product_key,
    seller_key = EXCLUDED.seller_key,
    order_date_key = EXCLUDED.order_date_key,
    price = EXCLUDED.price,
    freight_value = EXCLUDED.freight_value,
    quantity = EXCLUDED.quantity;

COMMIT;
