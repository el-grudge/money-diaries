{{ config(
    materialized='table',
    cluster_by="id"
)}}

SELECT
    result__ad_data__ad_entityid as id ,
    result__ad_data__ad_pageid as page_id,
    result__page_data__url_full as url ,
    _dlt_id as dlt_id
FROM {{ source('staging','blog_entry') }}

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}