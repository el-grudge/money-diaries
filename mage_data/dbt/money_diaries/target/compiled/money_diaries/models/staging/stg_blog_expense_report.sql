

WITH breakdown_data AS (
  SELECT
    _dlt_parent_id AS dlt_parent_id,
    (regexp_matches(content__alt_title, 'Food &amp; Drink:\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS food_and_drink,
    (regexp_matches(content__alt_title, 'Entertainment:\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS entertainment,
    (regexp_matches(content__alt_title, 'Home &amp; Health:\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS home_and_health,
    (regexp_matches(content__alt_title, 'Clothes &amp; Beauty\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS clothes_and_beauty,
    (regexp_matches(content__alt_title, 'Transportation\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS transportation,
    (regexp_matches(content__alt_title, 'Other\s*\$(\d+\.\d{2})', 'g'))[1]::numeric AS other    
  FROM "money_diaries"."money_diaries"."blog_entry__result__content__entries__sections__body"
  WHERE content__asset_id IS NOT NULL
    AND lower(content__alt_title) LIKE '%breakdown%'
)
SELECT
  dlt_parent_id,
  CAST(food_and_drink AS DOUBLE PRECISION) AS food_drink,
  CAST(entertainment AS DOUBLE PRECISION) AS entertainment,
  CAST(home_and_health AS DOUBLE PRECISION) AS home_health,
  CAST(clothes_and_beauty AS DOUBLE PRECISION) AS clothes_beauty,
  CAST(transportation AS DOUBLE PRECISION) AS transportation,
  CAST(other AS DOUBLE PRECISION) AS other
FROM breakdown_data

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
