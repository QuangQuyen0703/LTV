import streamlit as st
import pandas as pd
import plotly.express as px

# Function to calculate additional metrics
def calculate_metrics(data, new_customer_values, funded_cac_values):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Make sure both new_customer_values and Funding Rate have the same length
    new_customer_values = new_customer_values[:len(data['Funding Rate'])]
    funded_cac_values = funded_cac_values[:len(data['Funding Rate'])]

    # Calculate new funded customer with user input values
    data['new_funded_customer'] = new_customer_values * data['Funding Rate']

    # Set values for years 2024-2028 to be the same as 2023
    data.loc[data['Year'] >= 2024, ['ARPU', 'Direct Cost', 'Churn Rate']] = data.loc[data['Year'] == 2023, ['ARPU', 'Direct Cost', 'Churn Rate']].values[0]

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / (funded_cac_values * data['new_funded_customer'])

    # Calculate Payback
    data['payback'] = (data['ARPU'] - data['Direct Cost']) / (funded_cac_values * data['new_funded_customer'])

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

# Sample data loading
data = pd.read_csv("./data.csv")
st.write(data)

# Separate historical data (2021-2023) and forecast data (2024-2028)
historical_data = data[data['Year'] <= 2023]
forecast_data = data[data['Year'] >= 2024]

# Text inputs for user input
new_customer_values = st.text_input(f"Enter 'New Customer' values for 2024-2028 (comma-separated):", "400000,400000,400000,400000,400000")
funded_cac_values = st.text_input(f"Enter 'Funded CAC' values for 2024-2028 (comma-separated):", "2000,2000,2000,2000,2000")

# Convert input strings to lists of integers
new_customer_values = [int(value.strip()) for value in new_customer_values.split(',')]
funded_cac_values = [int(value.strip()) for value in funded_cac_values.split(',')]

# Check if data is available and then process it
if not historical_data.empty:
    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(historical_data, new_customer_values, funded_cac_values)

    # Combine historical data with forecast data
    processed_data = pd.concat([processed_data, forecast_data], ignore_index=True)

    # Visualization
    st.subheader('Additional Metrics Visualization')

    # Line chart for Total Customer by year
    fig_chart_1 = px.line(processed_data, x='Year', y='Total Customer', title='Total Customer by Year')
    fig_chart_1.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_1)

    # Line chart for New Customer by year
    fig_chart_2 = px.line(processed_data, x='Year', y='new_funded_customer', title='New Funded Customer by Year')
    fig_chart_2.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_2)

    # Line chart for Active Rate by year
    fig_chart_3 = px.line(processed_data, x='Year', y='Active Rate', title='Active Rate by Year')
    fig_chart_3.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_3)

    # Line chart for Funded Customer by year
    fig_chart_4 = px.line(processed_data, x='Year', y='new_funded_customer', title='Funded Customer by Year')
    fig_chart_4.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_4)

    # Line chart for GP/Active by year
    fig_chart_5 = px.line(processed_data, x='Year', y='gp_per_active', title='GP per Active Customer by Year')
    fig_chart_5.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_5)

    # Line chart for LTV/Funded CAC by year
    fig_chart_6 = px.line(processed_data, x='Year', y='ltv_cac_ratio', title='LTV/Funded CAC Ratio by Year')
    fig_chart_6.update_xaxes(type='category', tickmode='linear', categoryorder='category ascending')
    st.plotly_chart(fig_chart_6)

    # Line chart for Payback by year
    fig_chart_7 = px.line(processed
