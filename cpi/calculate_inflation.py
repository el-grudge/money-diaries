import pandas as pd
import numpy as np

def calculate_inflation(prices_data):
    """
    Calculate inflation using CPI method with weighted basket of goods    
    Parameters:
    prices_data (dict): Dictionary containing goods, their prices across years,
                       and their weights in the consumer basket
    Returns:
    DataFrame with CPI and inflation rates
    """
    # Sample basket of common consumer goods and services
    df = pd.DataFrame(prices_data)    
    # Calculate weighted price for each item
    for item in df.columns[:-1]:  # Exclude weights column
        df[f'{item}_weighted'] = df[item] * df['weights']
    # Calculate CPI for each year (sum of weighted prices / base year * 100)
    weighted_cols = [col for col in df.columns if 'weighted' in col]
    df['CPI'] = df[weighted_cols].sum(axis=1) / df[weighted_cols].iloc[0].sum() * 100
    # Calculate year-over-year inflation rate
    df['Inflation_Rate'] = df['CPI'].pct_change() * 100
    return df[['CPI', 'Inflation_Rate']]

# Example usage with sample data
sample_data = {
    'food': [100, 105, 112, 118],        # Food prices
    'housing': [1200, 1250, 1320, 1400], # Housing prices
    'transport': [200, 210, 225, 240],   # Transportation prices
    'weights': [0.3, 0.4, 0.3, 0.3]      # Weights in consumer basket
}

# Create DataFrame with years as index
df = pd.DataFrame(sample_data, index=[2020, 2021, 2022, 2023])

# Calculate inflation
result = calculate_inflation(sample_data)
print("\nCPI and Inflation Rates:")
print(result.round(2))