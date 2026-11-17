
SELECT
    COUNT(*) AS total_order_items,

    COUNT(*) FILTER (
        WHERE o.order_id IS NULL
    ) AS missing_orders,

    COUNT(*) FILTER (
        WHERE dc.customer_key IS NULL
    ) AS missing_customers,

    COUNT(*) FILTER (
        WHERE dp.product_key IS NULL
    ) AS missing_products,

    COUNT(*) FILTER (
        WHERE ds.seller_key IS NULL
    ) AS missing_sellers,

    COUNT(*) FILTER (
        WHERE dd.date_key IS NULL
    ) AS missing_dates

FROM staging.order_items oi

LEFT JOIN staging.orders o
    ON oi.order_id = o.order_id

LEFT JOIN warehouse.dim_customers dc
    ON o.customer_id = dc.customer_id

LEFT JOIN warehouse.dim_products dp
    ON oi.product_id = dp.product_id

LEFT JOIN warehouse.dim_sellers ds
    ON oi.seller_id = ds.seller_id

LEFT JOIN warehouse.dim_date dd
    ON CAST(o.order_purchase_timestamp AS DATE) = dd.full_date;
