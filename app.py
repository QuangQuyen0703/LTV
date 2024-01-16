import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate additional metrics
def calculate_metrics(data, funded_cac_increase_percentage):
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
    data.loc[mask, 'Funded CAC'] *= (1 + funded_cac_increase_percentage / 100)

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
    # Slider for Funded CAC increase percentage from 2024 to 2028
    funded_cac_increase_percentage = st.slider('Funded CAC Increase Percentage (2024-2028)', min_value=0, max_value=100, step=1, value=0)

    # Process and calculate additional metrics with user input values
    processed_data = calculate_metrics(data, funded_cac_increase_percentage)
    
    # Visualization
    st.subheader('Additional Metrics Visualization')
    
    # Line chart for LTV/CAC by year
    fig_line_chart = go.Figure()

    # Highlight the forecast period with a shaded rectangle
    forecast_start_year = 2024
    forecast_end_year = 2028
    fig_line_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['ltv_cac_ratio'],
                                        mode='lines+markers', name='LTV/CAC Ratio',
                                        line=dict(color='red', width=2) if (2021 <= processed_data['Year'].min() <= 2023) else dict(color='darkgray', width=2)))

    fig_line_chart.update_layout(title='LTV/CAC Ratio by Year')

    # Add a shaded rectangle to highlight the forecast period
    fig_line_chart.update_layout(shapes=[
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
    ])

    st.plotly_chart(fig_line_chart)

    # Line chart for Payback by year
    fig_payback_chart = go.Figure()

    # Highlight the forecast period with a shaded rectangle
    fig_payback_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['payback'],
                                           mode='lines+markers', name='Payback',
                                           line=dict(color='red', width=2) if (2021 <= processed_data['Year'].min() <= 2023) else dict(color='darkgray', width=2)))

    fig_payback_chart.update_layout(title='Payback by Year')

    # Add a shaded rectangle to highlight the forecast period
    fig_payback_chart.update_layout(shapes=[
        dict(
            type='rect',
            x0=forecast_start_year,
            x1=forecast_end_year,
            y0=processed_data['payback'].min(),
            y1=processed_data['payback'].max(),
            fillcolor='rgba(0, 100, 0, 0.1)',
            layer='below',
            line=dict(width=0),
        )
    ])

    st.plotly_chart(fig_payback_chart)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
