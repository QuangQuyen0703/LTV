import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Function to calculate additional metrics
def calculate_metrics(data, new_customer_value, funded_cac_value):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Calculate new funded customer with user input value
    data['new_funded_customer'] = new_customer_value * data['Funding Rate']

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / (funded_cac_value * data['new_funded_customer'])

    # Calculate Payback
    data['payback'] = (data['ARPU'] - data['Direct Cost']) / (funded_cac_value * data['new_funded_customer'])

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

data = pd.read_csv("./data.csv")
st.write(data)

# Slider for user input
new_customer_value = st.slider("Select 'New Customer' value for 2024-2028", min_value=0, max_value=100, value=10)
funded_cac_value = st.slider("Select 'Funded CAC' value for 2024-2028", min_value=0, max_value=100, value=5)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, new_customer_value, funded_cac_value)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Line chart for LTV/CAC by year
    fig_line_chart = px.line(processed_data, x='Year', y='ltv_cac_ratio', title='LTV/CAC Ratio by Year')
    st.plotly_chart(fig_line_chart)

    # Line chart for Payback by year
    fig_payback_chart = px.line(processed_data, x='Year', y='payback', title='Payback by Year')
    st.plotly_chart(fig_payback_chart)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
