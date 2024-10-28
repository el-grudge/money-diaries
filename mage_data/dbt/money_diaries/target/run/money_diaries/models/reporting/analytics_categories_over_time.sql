
  create view "money_diaries"."money_diaries"."analytics_categories_over_time__dbt_tmp"
    
    
  as (
    

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
FROM "money_diaries"."money_diaries"."reporting_blog_content_metrics"
  );