
CREATE TABLE IF NOT EXISTS warehouse.dim_products (

    product_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    product_id VARCHAR(32) NOT NULL UNIQUE,

    product_category_name TEXT,

    product_name_lenght INTEGER,

    product_description_lenght INTEGER,

    product_photos_qty INTEGER,

    product_weight_g INTEGER,

    product_length_cm INTEGER,

    product_height_cm INTEGER,

    product_width_cm INTEGER

);
