import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase_percentage, start_year, end_year):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Calculate inactive customer
    data['inactive_customer'] = data['Total Customer'] - data['active_customer']

    # Calculate new funded customer
    data['new_funded_customer'] = data['New Customer'] * data['Funding Rate']

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Apply Funded CAC increase only for the specified years
    mask = (data['Year'] >= start_year) & (data['Year'] <= end_year)
    data.loc[mask, 'Funded CAC'] *= (1 + funded_cac_increase_percentage / 100)

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / data['Funded CAC']

    # Calculate Payback
    data['payback'] = (data['ARPU'] - data['Direct Cost']) / data['Funded CAC']

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

data = pd.read_csv("./data.csv")
st.write(data)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Slider for Funded CAC increase percentage from 2024 to 2028
    funded_cac_increase_percentage = st.slider('Funded CAC Increase Percentage (2024-2028)', min_value=0, max_value=100, step=1, value=0)

    # Slider for the start year
    start_year = st.slider('Start Year', min_value=data['Year'].min(), max_value=data['Year'].max(), step=1, value=data['Year'].min())

    # Slider for the end year
    end_year = st.slider('End Year', min_value=data['Year'].min(), max_value=data['Year'].max(), step=1, value=data['Year'].max())

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase_percentage, start_year, end_year)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Line chart for LTV/CAC by year
    fig_line_chart = go.Figure()
    fig_line_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['ltv_cac_ratio'], mode='lines+markers', name='LTV/CAC Ratio'))
    fig_line_chart.update_layout(title='LTV/CAC Ratio by Year')
    st.plotly_chart(fig_line_chart)

    # Line chart for Payback by year
    fig_payback_chart = go.Figure()
    fig_payback_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['payback'], mode='lines+markers', name='Payback'))
    fig_payback_chart.update_layout(title='Payback by Year')
    st.plotly_chart(fig_payback_chart)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
