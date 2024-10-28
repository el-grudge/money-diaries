

SELECT
    result__ad_data__ad_entityid as id ,
    result__ad_data__ad_pageid as page_id,
    result__page_data__url_full as url ,
    _dlt_id as dlt_id
FROM "money_diaries"."money_diaries"."blog_entry"

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
