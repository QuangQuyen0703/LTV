import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_values):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer' and 'Active Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Calculate new funded customer
    data['new_funded_customer'] = data['New Customer'] * data['Funding Rate']

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / (data['Year'].map(funded_cac_values) * data['new_funded_customer'])

    # Calculate Payback
    data['payback'] = (data['ARPU'] - data['Direct Cost']) / funded_cac_values

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

data = pd.read_csv("./data.csv")
st.write(data)

# Allow user input for Funded CAC from 2024 to 2028
funded_cac_2024 = st.number_input('Enter Funded CAC for 2024', min_value=0.0)
funded_cac_2025 = st.number_input('Enter Funded CAC for 2025', min_value=0.0)
funded_cac_2026 = st.number_input('Enter Funded CAC for 2026', min_value=0.0)
funded_cac_2027 = st.number_input('Enter Funded CAC for 2027', min_value=0.0)
funded_cac_2028 = st.number_input('Enter Funded CAC for 2028', min_value=0.0)

# Store user input in a dictionary
funded_cac_values = {
    2024: funded_cac_2024,
    2025: funded_cac_2025,
    2026: funded_cac_2026,
    2027: funded_cac_2027,
    2028: funded_cac_2028
}

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Process and calculate additional metrics
    processed_data = calculate_metrics(data, funded_cac_values)
    
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
