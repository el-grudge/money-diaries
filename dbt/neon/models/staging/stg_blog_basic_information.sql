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
    regexp_replace(substring(content from '<strong>occupation:</strong>\s*([^<]+)'),'^[^:]*:\s*|\s+$','','g') as occupation,
    regexp_replace(substring(content from '<strong>industry:</strong>\s*([^<]+)'),'^[^:]*:\s*|\s+$','','g') as industry,
    CAST(regexp_replace(substring(content from '<strong>age:</strong>\s*([^<]+)'),'^[^:]*:\s*|\s+$','','g') AS INTEGER) as age,
    regexp_replace(substring(content from '<strong>location:</strong>\s*([^<]+)'),'^[^:]*:\s*|\s+$','','g') as location,
    CAST(regexp_replace(substring(content from '<strong>salary:</strong>\s*\$(\d+,?\d*)'),',','','g') AS INTEGER) as salary,
    -- Net worth extraction and calculation
    CAST(
      CASE
        WHEN (
          regexp_match(
            substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
            '(-?\$?[\d,\.]+)(\s*(million|m))?', 'i'
          )
        )[3] ~* 'million|m' THEN
          REPLACE(REPLACE((
            regexp_match(
              substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
              '(-?\$?[\d,\.]+)(\s*(million|m))?', 'i'
            )
          )[1], '$', ''), ',', '')::FLOAT * 1000000
        ELSE
          REPLACE(REPLACE((
            regexp_match(
              substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
              '(-?\$?[\d,\.]+)', 'i'
            )
          )[1], '$', ''), ',', '')::FLOAT
      END AS FLOAT
    ) AS net_worth,
    CAST(regexp_replace(substring(content from '<strong>debt:</strong>\s*\$?(\d+,?\d*)'),',','','g') AS INTEGER) as debt
FROM basic_information

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}