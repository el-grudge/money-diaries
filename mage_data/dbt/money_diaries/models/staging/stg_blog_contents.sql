{{ config(
    materialized='table',
    partition_by={
      "field": "published_date",
      "data_type": "date",
      "granularity": "day"
    },
    cluster_by = "id"
)}}

with data as (
SELECT
    id ,
    title as salary , 
    TO_TIMESTAMP(published)::DATE AS published_date,  
    _dlt_id as dlt_id,
    _dlt_parent_id as dlt_parent_id
FROM {{ source('staging','blog_entry__result__content__entries') }}
)
select 
  id ,
  salary ,
  published_date ,
  dlt_id ,
  dlt_parent_id
from data

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=false) %}

  limit 100

{% endif %}