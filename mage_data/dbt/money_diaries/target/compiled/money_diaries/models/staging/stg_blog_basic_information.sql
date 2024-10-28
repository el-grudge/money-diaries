


WITH basic_information AS (
  SELECT 
    _dlt_parent_id AS dlt_parent_id,
    lower(content) AS content
  FROM "money_diaries"."money_diaries"."blog_entry__result__content__entries__sections__body"
  WHERE lower(content) LIKE '%occupation%industry%age%'
)
SELECT 
  dlt_parent_id,
  regexp_replace(substring(content FROM '<strong>occupation:</strong>\s*([^<]+)'), '^[^:]*:\s*|&nbsp;|\s+$', '', 'g') AS occupation,
  regexp_replace(substring(content FROM '<strong>industry:</strong>\s*([^<]+)'), '^[^:]*:\s*|&nbsp;|\s+$', '', 'g') AS industry,
  CAST(regexp_replace(substring(content FROM '<strong>age:</strong>\s*([^<]+)'), '^[^:]*:\s*|&nbsp;|\s+$', '', 'g') AS INTEGER) AS age,
  regexp_replace(substring(content FROM '<strong>location:</strong>\s*([^<]+)'), '^[^:]*:\s*|&nbsp;|\s+$', '', 'g') AS location,
  CAST(regexp_replace(substring(content FROM '<strong>salary:</strong>\s*\$(\d+,?\d*)'), ',', '', 'g') AS INTEGER) AS salary,

  -- -- Net worth extraction and calculation
  -- CAST(
  --   CASE
  --     WHEN (
  --       regexp_match(
  --         substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
  --         '(-?\$?[\d,\.]+)(\s*(million|m))?', 'i'
  --       )
  --     )[3] ~* 'million|m' THEN
  --       REPLACE(REPLACE((
  --         regexp_match(
  --           substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
  --           '(-?\$?[\d,\.]+)(\s*(million|m))?', 'i'
  --         )
  --       )[1], '$', ''), ',', '')::FLOAT * 1000000
  --     ELSE
  --       REPLACE(REPLACE((
  --         regexp_match(
  --           substring(content FROM '<strong>net worth:</strong>\s*(.*?)(<br|$)'), 
  --           '(-?\$?[\d,\.]+)', 'i'
  --         )
  --       )[1], '$', ''), ',', '')::FLOAT
  --   END AS FLOAT
  -- ) AS net_worth,
  0 as net_worth,

  CAST(regexp_replace(substring(content FROM '<strong>debt:</strong>\s*\$?(\d+,?\d*)'), ',', '', 'g') AS INTEGER) AS debt
FROM basic_information

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
