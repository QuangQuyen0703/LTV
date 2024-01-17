import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase):
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

    # Apply Funded CAC increase only for the specified years (2024 to 2028)
    mask = (data['Year'] >= 2024) & (data['Year'] <= 2028)
    data.loc[mask, 'Funded CAC'] = (data.loc[mask, 'Funded CAC'] * 0) + funded_cac_increase

    # Calculate GP/Active
    data['gp_per_active'] = (data['ARPU'] - data['Direct Cost'])

    # Calculate total gross profit
    data['total_gross_profit'] = data['gp_per_active'] * data['active_customer']

    # Calculate LTV
    data['ltv'] = (data['ARPU'] - data['Direct Cost']) / data['Churn Rate']

    # Calculate LTV/CAC
    data['ltv_cac_ratio'] = data['ltv'] / data['Funded CAC']

    # Calculate Payback
    data['payback'] = data['Funded CAC'] / (data['ARPU'] - data['Direct Cost'])
    data['payback'] = data['payback'].clip(lower=0)  # Set Payback to 0 if less than 0

    # Calculate New Customer
    data['new_customer'] = data['New Customer']

    return data

# Title of the app
st.title('LTV Simulator')

# Create a sidebar for input
st.sidebar.title("Input Settings")

# Raw Data
# st.sidebar.subheader('Raw Data')
data = pd.read_csv("./data.csv")
# st.sidebar.write(data)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Input for Funded CAC increase from 5 to 30
    funded_cac_increase = st.sidebar.number_input('Funded CAC Input 2024-2028 (Unit: USD)', min_value=5, max_value=30, step=1, value=10)

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')

    # Column chart for New Customer by year (Unit: Thousands)
    fig_new_customer_column = go.Figure()

    # Set the color to purple (#563D82)
    new_customer_color = '#563D82'
    fig_new_customer_column.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['new_customer'] / 1000,
                                             name='New Customer (in thousands)',
                                             marker_color=new_customer_color,
                                             text=(processed_data['new_customer'] / 1000).round(2),
                                             textposition='outside'))
    
    fig_new_customer_column.update_layout(title='New Customer Acquisition (Unit: Thousands)')
    fig_new_customer_column.update_xaxes(showgrid=False)  # Remove x-axis gridlines
    fig_new_customer_column.update_yaxes(showgrid=False)  # Remove y-axis gridlines

    st.plotly_chart(fig_new
