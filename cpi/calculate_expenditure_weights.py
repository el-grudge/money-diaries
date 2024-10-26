import pandas as pd
import numpy as np


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

# Example with realistic household survey data (amounts in dollars)
# Sample of 1000 households
np.random.seed(42)  # For reproducibility
n_households = 1000

sample_data = pd.DataFrame({
    'Housing': np.random.normal(18000, 4000, n_households),     # Rent/mortgage, utilities, maintenance
    'Food': np.random.normal(8000, 2000, n_households),        # Food at home and away
    'Transportation': np.random.normal(9000, 2500, n_households), # Car, fuel, public transit
    'Healthcare': np.random.normal(5000, 1500, n_households),   # Medical expenses, insurance
    'Entertainment': np.random.normal(3000, 1000, n_households), # Recreation, streaming, etc.
    'Education': np.random.normal(2500, 800, n_households),     # Tuition, books, supplies
    'Clothing': np.random.normal(1800, 500, n_households),      # Apparel and services
    'Other': np.random.normal(4000, 1000, n_households)        # Miscellaneous expenses
})

# Remove any negative values (unrealistic for spending data)
sample_data = sample_data.clip(lower=0)

# Calculate weights
results = calculate_expenditure_weights(sample_data)

# Sort by weight percentage in descending order
sorted_results = results.sort_values('Weight_Percentage', ascending=False)
print("\nExpenditure Category Weights Analysis:")
print(sorted_results)

# Calculate summary statistics
total_spending = results['Average_Annual_Spending'].sum()
print(f"\nTotal Average Annual Household Spending: ${total_spending:,.2f}")
print(f"Number of households surveyed: {n_households}")





# First, let's simulate price data for the same categories over several years
def generate_price_data(base_data, num_years=4):
    """
    Generate price data for each category with small increases each year
    """
    years = range(2020, 2020 + num_years)
    price_trends = {}    
    # Start with base year prices (average spending from sample_data)
    base_prices = base_data.mean()
    for year in years:
        if year == 2020:
            # Base year prices
            price_trends[year] = base_prices
        else:
            # Add random price increases (between 2% and 8%) for each category
            random_increases = 1 + np.random.uniform(0.02, 0.08, len(base_prices))
            price_trends[year] = price_trends[year-1] * random_increases
    return pd.DataFrame(price_trends).T

# Generate price data using our sample_data as the base
price_data = generate_price_data(sample_data)

# Get weights from sorted_results (converting from percentage back to decimal)
weights = sorted_results['Weight_Percentage'] / 100

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
    results['Inflation_Rate'] = results['CPI'].pct_change() * 100
    return results

# Calculate CPI and inflation
cpi_results = calculate_simple_cpi(price_data, weights)

# Display results
print("\nPrice Data (Average prices by category and year):")
print(price_data.round(2))

print("\nWeights used:")
print(weights)

print("\nCPI and Inflation Results:")
print(cpi_results.round(2))

# Calculate category-specific contributions to inflation
def calculate_category_contributions(price_data, weights):
    """
    Calculate how much each category contributes to overall inflation
    """
    contributions = pd.DataFrame(index=price_data.index)
    for category in price_data.columns:
        # Calculate price relative (current price / base year price)
        price_relative = price_data[category] / price_data[category].iloc[0]
        # Calculate year-over-year change
        yearly_change = price_relative.pct_change()
        # Multiply by category weight to get contribution
        contributions[f'{category}_contribution'] = yearly_change * weights[category] * 100
    return contributions

# Calculate and display category contributions
contributions = calculate_category_contributions(price_data, weights)
print("\nCategory Contributions to Inflation Rate:")
print(contributions.round(2))