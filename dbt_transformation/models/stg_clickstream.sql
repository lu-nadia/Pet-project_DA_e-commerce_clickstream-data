{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT * 
    FROM {{ source('staging_ecommerce', 'raw_clickstream') }}
)

SELECT
    -- Приводим к правильным типам данных и чистим пропуски
    CAST(event_time AS TIMESTAMP) AS event_timestamp,
    CAST(event_type AS STRING) AS event_type,
    CAST(product_id AS INT64) AS product_id,
    CAST(category_id AS INT64) AS category_id,
    
    -- Заменяем NULL, которые мы нашли во время анализа
    COALESCE(category_code, 'unknown_category') AS category_code,
    COALESCE(brand, 'unknown_brand') AS brand,
    
    CAST(price AS FLOAT64) AS price,
    CAST(user_id AS INT64) AS user_id,
    CAST(user_session AS STRING) AS user_session
FROM raw_data