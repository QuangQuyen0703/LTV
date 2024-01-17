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

    # Line chart for LTV/CAC by year
    forecast_start_year = 2024
    forecast_end_year = 2028

    # Create a row for the first set of charts (New Customer, Funded CAC, and LTV)
    st.subheader('Chart Set 1')
    col1, col2 = st.beta_columns(2)

    # Line chart for Payback by year
    fig_payback_chart = go.Figure()

    # Highlight the forecast period with a shaded rectangle
    fig_payback_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['payback'],
                                          mode='lines+markers', name='Payback',
                                          text=processed_data['payback'].round(2),
                                          textposition='top center'))
    
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

    # Column chart for New Customer and Funded CAC & LTV by year
    fig_chart_set1 = go.Figure()

    # Add New Customer to the column chart
    fig_chart_set1.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['new_customer'] / 1000,
                                    name='New Customer (in thousands)',
                                    text=(processed_data['new_customer'] / 1000).round(2),
                                    textposition='outside'))

    # Add Funded CAC to the column chart
    fig_chart_set1.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['Funded CAC'],
                                    name='Funded CAC',
                                    text=processed_data['Funded CAC'].round(2),
                                    textposition='outside'))

    # Add LTV to the column chart
    fig_chart_set1.add_trace(go.Bar(x=processed_data['Year'], y=processed_data['ltv'],
                                    name='LTV',
                                    text=processed_data['ltv'].round(2),
                                    textposition='outside'))

    fig_chart_set1.update_layout(barmode='group', title='New Customer, Funded CAC, and LTV by Year')

    # Display the combined chart for Chart Set 1
    col1.plotly_chart(fig_chart_set1)

    # Create a row for the second set of charts (LTV/CAC and Payback)
    st.subheader('Chart Set 2')
    col3, col4 = st.beta_columns(2)

    # Line chart for LTV/CAC by year
    fig_line_chart = go.Figure()

    # Highlight the forecast period with a shaded rectangle
    fig_line_chart.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['ltv_cac_ratio'],
                                       mode='lines+markers', name='LTV/CAC Ratio',
                                       text=processed_data['ltv_cac_ratio'].round(2),
                                       textposition='top center'))

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

    # Line chart for Payback by year
    fig_payback_chart_set2 = go.Figure()

    # Highlight the forecast period with a shaded rectangle
    fig_payback_chart_set2.add_trace(go.Scatter(x=processed_data['Year'], y=processed_data['payback'],
                                                mode='lines+markers', name='Payback',
                                                text=processed_data['payback'].round(2),
                                                textposition='top center'))

    fig_payback_chart_set2.update_layout(title='Payback by Year')

    # Add a shaded rectangle to highlight the forecast period
    fig_payback_chart_set2.update_layout(shapes=[
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

    # Display the line chart for LTV/CAC and the line chart for Payback for Chart Set 2
    col3.plotly_chart(fig_line_chart)
    col4.plotly_chart(fig_payback_chart_set2)

    # Additional insights
    st.subheader('Insights')
    st.write("Your insights here based on the calculated data.")
