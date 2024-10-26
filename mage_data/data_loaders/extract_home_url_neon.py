import dlt 
import requests
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def paginated_getter(BASE_API_URL, blog_main_url, n_pages=15):
    page_number = 15

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

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    BASE_API_URL = 'https://www.refinery29.com'
    blog_main_url = '/en-us/money-diary'

    host = os.getenv("NEON_HOST")
    dbname = os.getenv("NEON_DB")
    user = os.getenv("NEON_USER")
    password = os.getenv("NEON_PASSWORD")
    postgres_connection_url = f"postgresql://{user}:{password}@{host}/{dbname}?sslmode=require"

    # Define your pipeline
    pipeline = dlt.pipeline(
        pipeline_name='my_pipeline',
        destination='postgres',
        dataset_name='money-diaries',
        credentials=postgres_connection_url
        )
    
    n_pages=15
    pipeline.run(
        paginated_getter(BASE_API_URL, blog_main_url, n_pages=n_pages), 
        table_name="diary_links", 
        write_disposition="replace"
    )

    return {}