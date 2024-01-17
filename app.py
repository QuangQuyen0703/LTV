import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
    data['payback'] = (data['ARPU'] - data['Direct Cost']) / data['Funded CAC']

    # Calculate New Customer
    data['new_customer'] = data['New Customer']

    return data

# Title of the app
st.title('LTV:CAC Visualization App')

data = pd.read_csv("./data.csv")
st.write(data)

# Check if data is available and then process it
if 'data' in locals() and not data.empty:
    # Slider for Funded CAC increase from 5 to 40
    funded_cac_increase = st.slider('Funded CAC Input 2024-2028 ($)', min_value=10, max_value=40, step=1, value=10)

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Highlight the forecast period with a shaded rectangle
    forecast_start_year = 2024
    forecast_end_year = 2028

    # Create subplots with 2 rows and 1 column
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=['LTV/CAC Ratio', 'Funded CAC and LTV'])

    # Line chart for LTV/CAC by year (Top subplot)
    fig.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['ltv_cac_ratio'],
                             mode='lines+markers', name='LTV/CAC Ratio',
                             text=processed_data['ltv_cac_ratio'].round(2),
                             textposition='top center'), row=1, col=1)
    
    # Add a shaded rectangle to highlight the forecast period
    fig.update_layout(shapes=[
        dict(
            type='rect',
            x0=forecast_start_year,
            x1=forecast_end_year,
            y0=processed_data['ltv_cac_ratio'].min(),
            y1=processed_data['ltv_cac_ratio'].max(),
            fillcolor='rgba(0, 100, 0, 0.1)',
            layer='below',
            line=dict(width=0),
        )
    ], row=1, col=1)

    # Column chart for Funded CAC and LTV by year (Bottom subplot)
    fig.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['Funded CAC'],
                         name='Funded CAC',
                         text=processed_data['Funded CAC'].round(2),
                         textposition='outside'), row=2, col=1)
    
    fig.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['ltv'],
                         name='LTV',
                         text=processed_data['ltv'].round(2),
                         textposition='outside'), row=2, col=1)

    fig.update_layout(barmode='group', title_text='Funded CAC and LTV by Year', showlegend=False)

    st.plotly_chart(fig)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
