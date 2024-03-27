{{ config(
    materialized='table',
    cluster_by = "dlt_parent_id"
)}}

WITH breakdown_data AS (
  SELECT
    _dlt_parent_id as dlt_parent_id,
    REGEXP_EXTRACT(content__alt_title, r'Food &amp; Drink: \$([\d.]+)') AS food_drink,
    REGEXP_EXTRACT(content__alt_title, r'Entertainment: \$([\d.]+)') AS entertainment,
    REGEXP_EXTRACT(content__alt_title, r'Home &amp; Health: \$([\d.]+)') AS home_health,
    REGEXP_EXTRACT(content__alt_title, r'Clothes &amp; Beauty \$([\d.]+)') AS clothes_beauty,
    REGEXP_EXTRACT(content__alt_title, r'Transportation \$([\d.]+)') AS transportation,
    REGEXP_EXTRACT(content__alt_title, r'Other \$([\d.]+)') AS other
FROM {{ source('staging','blog_entry__result__content__entries__sections__body') }}
where content__asset_id is not null
and lower(content__alt_title ) like '%breakdown%'
)
SELECT
  dlt_parent_id,
  CAST(food_drink AS FLOAT64) AS food_drink,
  CAST(entertainment AS FLOAT64) AS entertainment,
  CAST(home_health AS FLOAT64) AS home_health,
  CAST(clothes_beauty AS FLOAT64) AS clothes_beauty,
  CAST(transportation AS FLOAT64) AS transportation,
  CAST(other AS FLOAT64) AS other
FROM breakdown_data

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}