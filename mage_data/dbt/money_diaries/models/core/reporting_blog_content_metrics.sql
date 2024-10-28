{{
    config(
        materialized='table'
    )
}}

with blog as (
  select 
    a.id, 
    a.dlt_id as blog_dlt_id ,
    a.page_id, 
    a.url as blog_url
  from {{ ref('stg_blog_entries') }} as a
), 
contents as (
  select
    b.id ,
    b.dlt_parent_id ,
    b.dlt_id as content_dlt_id ,
    b.published_date 
  from {{ ref('stg_blog_contents') }} as b
), 
basic_information as (
  select 
    c.dlt_parent_id ,
    c.age,
    c.location,
    c.occupation ,
    c.industry ,
    c.salary,
    c.net_worth,
    c.debt
  from {{ ref('stg_blog_basic_information') }} as c
), 
expense_report as (
  select 
    d.dlt_parent_id,
    d.food_drink,
    d.entertainment,
    d.home_health,
    d.clothes_beauty,
    d.transportation,
    d.other  
  from {{ ref('stg_blog_expense_report') }} as d
)
select 
  -- identifiers 
  a.id, 
  a.blog_dlt_id ,
  b.content_dlt_id ,
  a.page_id, 
  
  -- page information
  a.blog_url ,
  b.published_date ,
  
  -- basic information 
  c.age,
  c.location,
  c.occupation ,
  c.industry ,
  c.salary,
  c.net_worth,
  c.debt,

  -- expense report 
  d.food_drink,
  d.entertainment,
  d.home_health,
  d.clothes_beauty,
  d.transportation,
  d.other
from blog as a 
left join contents as b 
on a.id = b.id 
and a.blog_dlt_id = b.dlt_parent_id
left join basic_information c 
on b.content_dlt_id = c.dlt_parent_id
left join expense_report d
on b.content_dlt_id = d.dlt_parent_id