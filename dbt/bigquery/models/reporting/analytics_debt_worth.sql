{{
    config(
        materialized='view'
    )
}}

SELECT 
  published_date ,
  age ,
  location ,
  debt ,
  net_worth
FROM {{ ref('reporting_blog_content_metrics') }}