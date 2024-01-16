import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from io import StringIO

# Function to calculate additional metrics
def calculate_metrics(data):
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
    # Process and calculate additional metrics
    processed_data = calculate_metrics(data)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Line chart for LTV/CAC by year
    fig_line_chart = px.line(processed_data, x='Year', y='ltv_cac_ratio', title='LTV/CAC Ratio by Year')
    st.plotly_chart(fig_line_chart)

    # Line chart for Payback by year
    fig_payback_chart = px.line(processed_data, x='Year', y='payback', title='Payback by Year')
    st.plotly_chart(fig_payback_chart)

    # Stacked column chart for Total Customer with Active and Inactive subcategories
    fig_stacked_column = go.Figure()
    fig_stacked_column.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['active_customer'], name='Active Customer'))
    fig_stacked_column.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['inactive_customer'], name='Inactive Customer'))
    fig_stacked_column.update_layout(barmode='stack', title='Total Customer with Active and Inactive Subcategories')
    st.plotly_chart(fig_stacked_column)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
