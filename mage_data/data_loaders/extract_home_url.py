import dlt 
import requests
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def paginated_getter(BASE_API_URL, blog_main_url, n_pages=1):
    page_number = 0

    while page_number <= n_pages:
        # Set the query parameters
        params = {'json':'true', 'page': page_number}

        # Make the GET request to the API
        response = requests.get(f'{BASE_API_URL}{blog_main_url}', params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()['result']['content']['modules']
        print(f'got page number {page_number} with {len(page_json)} records')

        # if the page has no records, stop iterating
        if page_json:
            yield page_json
            page_number += 1
        else:
            # No more data, break the loop
            break

# Load environment variables from the .env file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('path_to_keyfile')
# make this parameterized to be set by user
project_id = os.getenv('GCP_PROJECT_ID')

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    BASE_API_URL = 'https://www.refinery29.com'
    blog_main_url = '/en-us/money-diary'
    # Define your pipeline
    pipeline = dlt.pipeline(
        pipeline_name='my_pipeline',
        destination='bigquery',
        dataset_name='money-diaries'
        )
    
    
    n_pages=0
    pipeline.run(
        paginated_getter(BASE_API_URL, blog_main_url, n_pages=n_pages), 
        table_name="diary_links", 
        write_disposition="replace"
    )

    return {}