import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Function to calculate additional metrics
def calculate_metrics(data):
    # Assuming 'Total Customer', 'Active Rate', 'New Customer', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'churn_rate', 'Funded CAC', 'Year' are columns in your data

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Calculate new funded customer
    data['new_funded_customer'] = data['New Customer'] * data['Funding Rate']

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost']) / data['active_customer']

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / (data['Funded CAC'] * data['new_funded_customer'])

    # Calculate Payback
    data['payback'] = (data['ARPU'] - data['Direct Cost']) /data['Funded CAC']

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

data = pd.read_csv("./data.csv")
st.write(data)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Process and calculate additional metrics
    processed_data = calculate_metrics(data)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Line chart for LTV/CAC by year
    fig_line_chart = px.line(processed_data, x='year', y='ltv_cac_ratio', title='LTV/CAC Ratio by Year')
    st.plotly_chart(fig_line_chart)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
