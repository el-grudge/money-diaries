
  create view "money_diaries"."money_diaries"."analytics_debt_worth__dbt_tmp"
    
    
  as (
    

SELECT 
  published_date ,
  age ,
  location ,
  debt ,
  net_worth
FROM "money_diaries"."money_diaries"."reporting_blog_content_metrics"
  );