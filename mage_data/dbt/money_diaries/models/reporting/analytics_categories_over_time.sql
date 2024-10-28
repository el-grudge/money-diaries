{{
    config(
        materialized='view'
    )
}}

SELECT 
  published_date,
  age ,
  location ,
  food_drink, 
  entertainment,
  home_health,
  clothes_beauty,
  transportation,
  other
FROM {{ ref('reporting_blog_content_metrics') }}