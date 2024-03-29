Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

DBT supports paritioning and clustering for BigQuery using the following format:

```lua
{{ config(
    materialized="incremental",
    partition_by={
      "field": "created_date",
      "data_type": "timestamp",
      "granularity": "day",
      "time_ingestion_partitioning": true
    }, 
    cluster_by = ["customer_id", "order_id"]
) }}

select
  user_id,
  event_name,
  created_at,
  -- values of this column must match the data type + granularity defined above
  timestamp_trunc(created_at, day) as created_date

from {{ ref('events') }}
```