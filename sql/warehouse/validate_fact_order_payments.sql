
SELECT
    COUNT(*) AS total_payments,

    COUNT(*) FILTER (
        WHERE o.order_id IS NULL
    ) AS missing_orders,

    COUNT(*) FILTER (
        WHERE dc.customer_key IS NULL
    ) AS missing_customers,

    COUNT(*) FILTER (
        WHERE dd.date_key IS NULL
    ) AS missing_dates

FROM staging.payments p

LEFT JOIN staging.orders o
    ON p.order_id = o.order_id

LEFT JOIN warehouse.dim_customers dc
    ON o.customer_id = dc.customer_id

LEFT JOIN warehouse.dim_date dd
    ON CAST(o.order_purchase_timestamp AS DATE) = dd.full_date;
