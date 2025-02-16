import streamlit as st
import pandas as pd

# Streamlit app layout
st.title('Agent Performance Tracker')

# File upload widget
file = st.file_uploader("Upload your CSV file", type="csv")

if file is not None:
    # Read CSV with encoding handling
    try:
        my_data = pd.read_csv(file, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        my_data = pd.read_csv(file, encoding='utf-8')

    # Ensure column names are consistent
    my_data.columns = my_data.columns.str.strip()  # Remove extra spaces

    # Convert 'Date' column to datetime
    my_data['Date'] = pd.to_datetime(my_data['Date'], format='%d/%m/%Y', errors='coerce')

    # Drop rows where Date couldn't be parsed
    my_data = my_data.dropna(subset=['Date'])

    # Fix encoding issues in the "Reasons" column
    my_data['Reasons'] = my_data['Reasons'].astype(str).apply(lambda x: x.encode('latin1').decode('utf-8', 'ignore'))

    # Input fields for Agent name and date range
    agent_name = st.selectbox('Select Agent Name', my_data['Agent name'].unique())
    start_date = st.date_input('Start Date', min_value=my_data['Date'].min())
    end_date = st.date_input('End Date', min_value=start_date, max_value=my_data['Date'].max())

    # Filter the data
    filtered_data = my_data[(my_data['Agent name'] == agent_name) & 
                            (my_data['Date'].between(start_date, end_date))]

    # Calculate 'Performance' column safely
    filtered_data.loc[:, 'Target Achieved'] = filtered_data['Processed Lots'] >= filtered_data['Target Lots']

    # Display the results with 'Target Lots' column
    if filtered_data.empty:
        st.warning("No data available for the selected agent and date range.")
    else:
        st.dataframe(filtered_data[['Date', 'Queue', 'Processed Lots', 'Target Lots', 'Reasons', 'Target Achieved']])

        # Check if target was achieved for the entire period
        if filtered_data['Target Achieved'].all():
            st.success('🎯 Target Achieved!')
        else:
            st.warning('⚠️ Target Not Achieved')
