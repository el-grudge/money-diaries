import dlt 
import requests

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def get_json_from_url(blog_url, params = {'json': 'true'}):
    # get blog entries
    response = requests.get(blog_url, params=params)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    return response.json()

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
    
    pipeline = dlt.pipeline(
        pipeline_name='my_pipeline',
        destination='bigquery',
        dataset_name='money-diaries'
        )

    pipeline.run(
        [get_json_from_url(BASE_API_URL+url) for url in data['object__url']], 
        table_name="blog_entry", 
        write_disposition="replace"
        )