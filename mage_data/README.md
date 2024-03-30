By default, the pipeline only extracts the posts on the blog's home page, to extract more posts change the value of `n_pages` variable in [extract_home_url.py](./data_loaders/extract_home_url.py). Make this change in Mage.ai and run the pipeline

```python
@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    BASE_API_URL = 'https://www.refinery29.com'
    blog_main_url = '/en-us/money-diary'
    pipeline = dlt.pipeline(
        pipeline_name='my_pipeline',
        destination='bigquery',
        dataset_name='money-diaries'
        )
    
    
    n_pages=0 # increase this to extract more posts
    pipeline.run(
        paginated_getter(BASE_API_URL, blog_main_url, n_pages=n_pages), 
        table_name="diary_links", 
        write_disposition="replace"
    )

    return {}
```

