import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import altair as alt
import pandas as pd
import os
import subprocess


def is_gcloud_authenticated():
    try:
        # Run gcloud auth list command
        result = subprocess.run(['gcloud', 'auth', 'list'], capture_output=True, text=True)
        
        # Check if the output contains "ACTIVE" which indicates authentication
        if "ACTIVE" in result.stdout:
            return True
        else:
            return False
    except FileNotFoundError:
        # Handle case where gcloud command is not found
        print("gcloud command not found. Please make sure gcloud SDK is installed and configured.")
        return False


@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows


# Define a function to create age groups
def create_age_group(age):
    if pd.isna(age):
        return pd.NA
    else:
        return f"{(age // 5) * 5}-{((age // 5) * 5) + 4}"


if __name__ == "__main__":

    if is_gcloud_authenticated():
        print("gcloud is authenticated.")
        client = bigquery.Client()
        project_id = os.getenv("GOOGLE_PROJECT_ID")
    else:
        # Create API client.
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(credentials=credentials)
        project_id = st.secrets["gcp_service_account"]["project_id"]

    st.set_page_config(
        page_title = 'Money Diaries',
        page_icon = '💵',
        layout = 'wide'
    )

    # dashboard title
    st.title("Money: An Oral History")

    # creating a single-element container.
    placeholder = st.empty()

    with placeholder.container():
        col1, col2, col3 = st.columns([1, 0.15, 1])
        with col1:
            st.markdown(
                """
                <br> <!-- Empty new line -->
                <div style="font-size: 20px;">
                    <a href="https://www.refinery29.com/en-us/money-diary" style="color: blue; text-decoration: underline;">Money Diaries</a> is a blog created and hosted by Refinery29. The blog's first post came out in 2016, and each week three new anonymous contributes post about their money spending habits. The blog is a rich source for anyone who wants to learn about how money shapes our lives, whether the disconnect between financial reports and people's sentiment about inflation can be backed by data, salary distribution, and debt / net worth ratio. I hope you find it useful
                </div>
                """,
                unsafe_allow_html=True
            )

            # Decrease column width
            st.markdown(
                """
                <style>
                    .reportview-container .main .block-container {
                        max-width: 50%;
                    }
                </style>
                """,
                unsafe_allow_html=True
            )

        with col3:
            # Query to retrieve salary data
            query = f"""
            select * FROM `{project_id}.money_diaries.analytics_categories_over_time`
            """
            # Execute the query and convert the results to a Pandas DataFrame
            df = pd.DataFrame(run_query(query))

            # Convert 'published_date' to datetime
            df = df[df['food_drink'].notnull()] # remove this line after implementing google vision extraction 
            df['published_date'] = pd.to_datetime(df['published_date'])
            current_month = df['published_date'].max() - pd.DateOffset(months=1)
            previous_month = current_month - pd.DateOffset(months=1)

            current_df = df[(df['published_date'] >= current_month)]
            previous_df = df[(df['published_date'] >= previous_month) & (df['published_date'] < current_month)]

            # averages
            cur_avg = current_df.mean(numeric_only=True).round().to_dict()
            pre_avg = previous_df.mean(numeric_only=True).round().to_dict()

            # create three columns
            st.markdown("### Prices (per week)")
            kpi1, kpi2, kpi3 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs 
            kpi1.metric(label="Food + Drink 🍔🥤", value=f"$ {cur_avg['food_drink']}", delta=cur_avg['food_drink']-pre_avg['food_drink'])
            kpi2.metric(label="Entertainment 🎡", value=f"$ {cur_avg['entertainment']}", delta=cur_avg['entertainment']-pre_avg['entertainment'])
            kpi3.metric(label="Home + Health 🏠💊", value=f"$ {cur_avg['home_health']}", delta=cur_avg['home_health']-pre_avg['home_health'])

            # create three columns
            kpi4, kpi5, kpi6 = st.columns(3)

            # fill in those three columns with respective metrics or KPIs 
            kpi4.metric(label="Clothes + Beauty 👗💅", value=f"$ {cur_avg['clothes_beauty']}", delta=cur_avg['clothes_beauty']-pre_avg['clothes_beauty'])
            kpi5.metric(label="Transportation 🛻", value=f"$ {cur_avg['transportation']}", delta=cur_avg['transportation']-pre_avg['transportation'])
            kpi6.metric(label="Other 🟣", value=f"$ {cur_avg['other']}", delta=cur_avg['other']-pre_avg['other'])

        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            # Query to retrieve salary data
            query = f"""
            select * FROM `{project_id}.money_diaries.analytics_salaries`
            """
            # Execute the query and convert the results to a Pandas DataFrame
            df = pd.DataFrame(run_query(query))
            df['salary'] = df['salary'].str.extract('(\d+,?\d+)')[0].str.replace(',','').str.replace('~','').astype(float)

            st.markdown("### Salary distribution")
            # Plotting the histogram using Altair
            histogram_chart = alt.Chart(df).mark_bar(color='#e4fb2d').encode(
                alt.X("salary:Q", bin=alt.Bin(maxbins=50), title="Salary"),
                alt.Y('count():Q', title="Frequency"),
            ).properties(
                width=750,
                height=550
            ).configure_axis(
                labelFontSize=12,
                titleFontSize=14
            ).configure_title(
                fontSize=20,
                color='#27345e'
            )        
            st.write(histogram_chart)

        with fig_col2:
            # Query to retrieve salary data
            query = f"""
            select * FROM `{project_id}.money_diaries.analytics_categories_over_time`
            """
            # Execute the query and convert the results to a Pandas DataFrame
            df = pd.DataFrame(run_query(query))
            df['published_date'] = pd.to_datetime(df['published_date'])
            col_names = ['published_date', 'food_drink', 'entertainment', 'home_health', 'clothes_beauty', 'transportation', 'other']
            df = df[col_names]
            df['month'] = df['published_date'].dt.to_period('M')
            
            # Group by 'month' and calculate mean
            df = df.groupby('month').mean()
            df_melted = df.melt(id_vars='published_date', var_name='category', value_name='value')

            # Plotting line charts using Altair
            st.markdown("### Prices over time")

            # Define colors for each category
            category_colors = {
                'food_drink': '#2bfb2b',
                'entertainment': '#2be4fb',
                'home_health': '#2b2bfb',
                'clothes_beauty': '#fb2be4',
                'transportation': '#fb2b2b',
                'other': '#fbe42b'
            }

            # Create individual charts for each category
            charts = []
            for category in col_names[1:]:
                chart = alt.Chart(df_melted[df_melted['category'] == category]).mark_line().encode(
                    x='published_date:T',
                    y='value:Q',
                    color=alt.Color('category:N', scale=alt.Scale(range=list(category_colors.values())), legend=None)
                ).properties(
                    width=200,
                    height=150,
                    title=category
                )
                charts.append(chart)

            # Combine charts into a grid
            facet = alt.vconcat(alt.hconcat(*charts[:3], spacing=20), alt.hconcat(*charts[3:], spacing=20), spacing=20)
            st.write(facet)

        col1, col2, col3 = st.columns([0.7, 1, 1])
        with col2:
            # Query to retrieve salary data
            query = f"""
            select * FROM `{project_id}.money_diaries.analytics_debt_worth`
            """
            # Execute the query and convert the results to a Pandas DataFrame
            df = pd.DataFrame(run_query(query))
            df['debt'] = -1*df['debt'].str.extract('(\d+,?\d+)')[0].str.replace(',','').astype(float)
            df['net_worth'] = df['net_worth'].str.extract('(-?.?\d+,?\d+)')[0].str.replace(',','').str.replace('$','').str.replace('~','').str.replace('/','').astype(float)
            df['age_group'] = df['age'].apply(create_age_group)

            col_names = ['age_group','debt','net_worth']
            df = df[col_names]

            df_melted = df[col_names].melt(id_vars='age_group', var_name='category', value_name='value').groupby(['age_group', 'category']).agg({'value': 'mean'}).reset_index()

            title = 'Net worth / debt per age group'
            subtitle = 'Debt' + ' '*10 + 'Net Wealth'

            # Create the chart
            chart = alt.Chart(df_melted).mark_bar().encode(
                x=alt.X('value:Q', axis=alt.Axis(title='Value')),
                y=alt.Y('age_group:N', axis=alt.Axis(title='Age Group')),
                color=alt.Color('category:N', scale=alt.Scale(domain=['net_worth', 'debt'], range=['#182760', '#fb08d3']), legend=None),
                tooltip=['value:Q']
            ).properties(
                width=850,
                height=650
            ).configure_axis(
                grid=False
            )

            # Combine chart and text
            divergent_bar_chart = (chart)

            # Show the chart
            title = 'Net worth / debt per age group'
            st.markdown(f"<h3 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True)  # Center-align 
            st.altair_chart(chart, use_container_width=True)
            