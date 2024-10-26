{{ config(
    materialized='table',
    cluster_by = "dlt_parent_id"
)}}

WITH basic_information AS (
  SELECT 
    _dlt_parent_id as dlt_parent_id ,
    lower(content) as content
  FROM {{ source('staging','blog_entry__result__content__entries__sections__body') }}
  where lower(content) like '%occupation%industry%age%'
)
SELECT 
    dlt_parent_id,
    REGEXP_EXTRACT(content, r'<strong>occupation:</strong>\s*([^<]+)') AS occupation,
    REGEXP_EXTRACT(content, r'<strong>industry:</strong>\s*([^<]+)') AS industry,
    CAST(REGEXP_EXTRACT(content, r'<strong>age:</strong>\s*(\d+)') AS INT64) AS age,
    REGEXP_EXTRACT(content, r'<strong>location:</strong>\s*([^<]+)') AS location,
    REGEXP_EXTRACT(content, r'<strong>.*salary:</strong>\s*([^<]+)') AS salary,
    REGEXP_EXTRACT(content, r'<strong>net worth:</strong>\s*([^<]+)') AS net_worth,
    REGEXP_EXTRACT(content, r'<strong>debt:</strong>\s*([^<]+)') AS debt
FROM basic_information

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}