
  create view "money_diaries"."money_diaries"."analytics_salaries__dbt_tmp"
    
    
  as (
    

SELECT 
  published_date ,
  age ,
  location ,
  salary
FROM "money_diaries"."money_diaries"."reporting_blog_content_metrics"
  );