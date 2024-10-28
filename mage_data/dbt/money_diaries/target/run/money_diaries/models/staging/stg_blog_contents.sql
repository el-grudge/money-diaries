
  
    

  create  table "money_diaries"."money_diaries"."stg_blog_contents__dbt_tmp"
  
  
    as
  
  (
    

with data as (
SELECT
    id ,
    title as salary , 
    TO_TIMESTAMP(published)::DATE AS published_date,  
    _dlt_id as dlt_id,
    _dlt_parent_id as dlt_parent_id
FROM "money_diaries"."money_diaries"."blog_entry__result__content__entries"
)
select 
  id ,
  salary ,
  published_date ,
  dlt_id ,
  dlt_parent_id
from data

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'

  );
  