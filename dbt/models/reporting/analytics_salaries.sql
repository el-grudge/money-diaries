{{
    config(
        materialized='view'
    )
}}

SELECT 
  published_date ,
  age ,
  location ,
  salary
FROM {{ ref('reporting_blog_content_metrics') }}