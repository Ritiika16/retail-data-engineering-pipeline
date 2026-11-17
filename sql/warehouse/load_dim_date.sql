
INSERT INTO warehouse.dim_date (
    date_key,
    full_date,
    year,
    quarter,
    month,
    month_name,
    day,
    day_of_week,
    day_name,
    week_of_year,
    is_weekend
)
SELECT
    TO_CHAR(d.full_date, 'YYYYMMDD')::INTEGER,
    d.full_date,
    EXTRACT(YEAR FROM d.full_date)::INTEGER,
    EXTRACT(QUARTER FROM d.full_date)::INTEGER,
    EXTRACT(MONTH FROM d.full_date)::INTEGER,
    TRIM(TO_CHAR(d.full_date, 'Month')),
    EXTRACT(DAY FROM d.full_date)::INTEGER,
    EXTRACT(ISODOW FROM d.full_date)::INTEGER,
    TRIM(TO_CHAR(d.full_date, 'Day')),
    EXTRACT(WEEK FROM d.full_date)::INTEGER,
    EXTRACT(ISODOW FROM d.full_date) IN (6, 7)
FROM generate_series(
    DATE '2016-01-01',
    DATE '2020-12-31',
    INTERVAL '1 day'
) AS d(full_date)

ON CONFLICT (date_key) DO NOTHING;
