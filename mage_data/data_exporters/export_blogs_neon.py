import os
import dlt 
import requests

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def get_json_from_url(blog_url, params = {'json': 'true'}):
    try:
        response = requests.get(blog_url, params=params, timeout=10)  # Added timeout
        response.raise_for_status()
        return response.json()
    except:
        print(f"Failed to fetch data from {blog_url}")
        return None

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    BASE_API_URL = 'https://www.refinery29.com'
    
    host = os.getenv("NEON_HOST")
    dbname = os.getenv("NEON_DB")
    user = os.getenv("NEON_USER")
    password = os.getenv("NEON_PASSWORD")
    postgres_connection_url = f"postgresql://{user}:{password}@{host}/{dbname}?sslmode=require"

    pipeline = dlt.pipeline(
        pipeline_name='my_pipeline',
        destination='postgres',
        dataset_name='money-diaries',
        credentials=postgres_connection_url
        )

    pipeline.run(
        [get_json_from_url(BASE_API_URL+url) for url in data['object__url']], 
        table_name="blog_entry", 
        write_disposition="replace"
        )