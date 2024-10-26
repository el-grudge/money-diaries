import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import asyncio
from sqlalchemy import text
from dotenv import load_dotenv
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine
import pandas as pd
import nest_asyncio
import numpy as np
import streamlit as st

load_dotenv()

def run_query(query):
    tmpPostgres = urlparse(st.secrets["neon"]["DATABASE_URL"])

    async def async_run():
        engine = create_async_engine(
            f"postgresql+asyncpg://{tmpPostgres.username}:{tmpPostgres.password}@{tmpPostgres.hostname}{tmpPostgres.path}?ssl=require", 
            echo=True
        )
        
        # Debug: Check connection string
        print(f"Connecting to database at: {tmpPostgres.hostname}")

        async with engine.connect() as conn:
            print("Executing query...")
            result = await conn.execute(text(query))
            rows = result.fetchall()  # This should not be awaited
            
            # Debug: Print the fetched rows
            print(f"Rows fetched: {rows}")

        await engine.dispose()
        return rows

    # Directly run the async function
    return asyncio.run(async_run())

def calculate_expenditure_weights(household_data):
    """
    Calculate consumer expenditure weights based on household survey data
    Parameters:
    household_data (DataFrame): Survey data of household spending by category
    Returns:
    DataFrame with calculated weights and summary statistics
    """
    def calculate_relative_importance(data):
        # Calculate percentage of total expenditure for each category
        total_spending = data.sum()
        return (data / total_spending * 100).round(2)
    # Calculate average spending per household
    avg_spending = household_data.mean()
    # Calculate weights (relative importance)
    weights = calculate_relative_importance(avg_spending)
    # Calculate standard error to show variation in spending patterns
    std_error = household_data.std() / np.sqrt(len(household_data))
    # Combine results
    results = pd.DataFrame({
        'Average_Annual_Spending': avg_spending.round(2),
        'Weight_Percentage': weights,
        'Std_Error': std_error.round(2)
    })
    return results

# Calculate CPI
def calculate_simple_cpi(price_data, weights):
    """
    Calculate CPI using weights and price data
    """
    # Create empty DataFrame for results
    results = pd.DataFrame(index=price_data.index)
    # Calculate weighted prices for each year
    weighted_prices = price_data.multiply(weights)
    # Calculate CPI (sum of weighted prices divided by base year sum, times 100)
    base_year_weighted_sum = weighted_prices.iloc[0].sum()
    results['CPI'] = (weighted_prices.sum(axis=1) / base_year_weighted_sum) * 100
    # Calculate inflation rate
    results['Inflation_Rate'] = results['CPI'].pct_change()
    return results

def get_official_cpi():
    # BLS API endpoint
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'

    # Series ID for CPI (All Urban Consumers, All Items, Not Seasonally Adjusted)
    series_id = 'CUUR0000SA0'

    # API request parameters
    data = json.dumps({
        "seriesid": [series_id],
        "startyear": "2021",
        "endyear": "2024",
        "registrationkey": "d7ba76b4ba7b4f0fbec2d1d704a819d1"  # Replace with your BLS API key
    })

    # Send request to BLS API
    headers = {'Content-type': 'application/json'}
    response = requests.post(url, data=data, headers=headers)

    # Parse the JSON response
    json_data = json.loads(response.text)

    # Extract the data series
    series = json_data['Results']['series'][0]

    # Create a list of dictionaries with the data
    data_list = []
    for item in series['data']:
        year = int(item['year'])
        month = int(item['period'][1:])  # Remove 'M' prefix from month
        date = datetime(year, month, 1)
        value = float(item['value'])
        data_list.append({'Date': date, 'CPI': value})

    # Create a DataFrame
    df = pd.DataFrame(data_list)
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)

    # Calculate month-over-month inflation rate
    df['MoM_Inflation'] = df['CPI'].pct_change() * 100

    # Calculate year-over-year inflation rate
    df['YoY_Inflation'] = df['CPI'].pct_change(periods=12) * 100

    start_date = '2021-11-01'
    end_date = '2022-02-01'
    filtered_df = df.loc[start_date:end_date]

    return filtered_df

def calculate_user_response_cpi():
    # Apply nest_asyncio
    nest_asyncio.apply()

    query = f"""
    select * FROM money_diaries.analytics_categories_over_time
    """
    # Execute the query and convert the results to a Pandas DataFrame
    df = pd.DataFrame(run_query(query))
    df['published_date'] = pd.to_datetime(df['published_date'])
    col_names = ['published_date', 'food_drink', 'entertainment', 'home_health', 'clothes_beauty', 'transportation', 'other']
    df = df[col_names]
    df['month'] = df['published_date'].dt.to_period('M')

    # Step 1: Convert 'published_date' to datetime
    df['published_date'] = pd.to_datetime(df['published_date'])

    # Step 2: Set 'published_date' as the index
    df.set_index('published_date', inplace=True)
    df.drop(['month'], axis=1, inplace=True)

    # Step 3: Group by year and month, then calculate the mean
    monthly_means = df.resample('M').mean()

    # Calculate weights
    results = calculate_expenditure_weights(df[['food_drink', 'entertainment', 'home_health', 'clothes_beauty', 'transportation', 'other']])
    sorted_results = results.sort_values('Weight_Percentage', ascending=False)

    # Get weights from sorted_results (converting from percentage back to decimal)
    weights = sorted_results['Weight_Percentage'] / 100

    cpi_results = calculate_simple_cpi(monthly_means, weights)

    return cpi_results
