import streamlit as st
import pandas as pd
import plotly.express as px

# Function to calculate additional metrics
def calculate_metrics(data, new_customer_values, active_rate_values, funding_rate_values, arpu_values, direct_cost_values, churn_rate_values, funded_cac_values):
    # Assuming 'Year', 'Total Customer', 'Active Rate', 'Funding Rate',
    # 'ARPU', 'Direct Cost', 'Churn Rate', 'Funded CAC' are columns in your data

    # Convert 'Direct Cost' to numeric
    data['Direct Cost'] = pd.to_numeric(data['Direct Cost'], errors='coerce')

    # Convert 'Total Customer', 'Active Rate', 'Funding Rate', 'ARPU', 'Churn Rate' to numeric if needed
    data['Total Customer'] = pd.to_numeric(data['Total Customer'], errors='coerce')
    data['Active Rate'] = pd.to_numeric(data['Active Rate'], errors='coerce')
    data['Funding Rate'] = pd.to_numeric(data['Funding Rate'], errors='coerce')
    data['ARPU'] = pd.to_numeric(data['ARPU'], errors='coerce')
    data['Churn Rate'] = pd.to_numeric(data['Churn Rate'], errors='coerce')

    # Calculate active customer
    data['active_customer'] = data['Total Customer'] * data['Active Rate']

    # Make sure all user input values have the same length as 'Funding Rate'
    new_customer_values = new_customer_values[:len(data['Funding Rate'])]
    active_rate_values = active_rate_values[:len(data['Funding Rate'])]
    funding_rate_values = funding_rate_values[:len(data['Funding Rate'])]
    arpu_values = arpu_values[:len(data['Funding Rate'])]
    direct_cost_values = direct_cost_values[:len(data['Funding Rate'])]
    churn_rate_values = churn_rate_values[:len(data['Funding Rate'])]
    funded_cac_values = funded_cac_values[:len(data['Funding Rate'])]

    # Update data with user input values
    data['New Customer'] = new_customer_values
    data['Active Rate'] = active_rate_values
    data['Funding Rate'] = funding_rate_values
    data['ARPU'] = arpu_values
    data['Direct Cost'] = direct_cost_values
    data['Churn Rate'] = churn_rate_values

    # Calculate new funded customer with user input values
    data['new_funded_customer'] = new_customer_values * data['Funding Rate']

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

# Get the maximum year from the dataset
max_year = data['Year'].max()

# Text inputs for user input
new_customer_values = st.text_input(f"Enter 'New Customer' values for 2024-{max_year} (comma-separated):", "400000,400000,400000,400000,400000")
active_rate_values = st.text_input(f"Enter 'Active Rate' values for 2024-{max_year} (comma-separated):", "0.8,0.8,0.8,0.8,0.8")
funding_rate_values = st.text_input(f"Enter 'Funding Rate' values for 2024-{max_year} (comma-separated):", "0.1,0.1,0.1,0.1,0.1")
arpu_values = st.text_input(f"Enter 'ARPU' values for 2024-{max_year} (comma-separated):", "100,100,100,100,100")
direct_cost_values = st.text_input(f"Enter 'Direct Cost' values for 2024-{max_year} (comma-separated):", "50,50,50,50,50")
churn_rate_values = st.text_input(f"Enter 'Churn Rate' values for 2024-{max_year} (comma-separated):", "0.05,0.
