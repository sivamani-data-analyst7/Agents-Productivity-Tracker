import streamlit as st
import pandas as pd

st.title('Agent Performance Tracker')

# File upload widget
file = st.file_uploader("Upload your CSV file", type="csv")

if file is not None:
    # Read CSV with encoding handling
    try:
        my_data = pd.read_csv(file, encoding='ISO-8859-1')
    except UnicodeDecodeError:
        my_data = pd.read_csv(file, encoding='utf-8')

    # Strip spaces from column names
    my_data.columns = my_data.columns.str.strip()

    # Rename columns if necessary
    column_mapping = {
        'Agent nam': 'Agent name',
        'Processed': 'Processed Lots',
        'Target Lot': 'Target Lots'
    }
    my_data.rename(columns=column_mapping, inplace=True)

    # Convert 'Date' column to datetime
    my_data['Date'] = pd.to_datetime(my_data['Date'], format='%d/%m/%Y', errors='coerce')

    # Drop rows where Date is NaT (invalid)
    my_data = my_data.dropna(subset=['Date'])

    # Ensure 'Date' column is sorted
    my_data = my_data.sort_values(by='Date')

    # Get min/max dates safely
    min_date = my_data['Date'].min()
    max_date = my_data['Date'].max()

    # Input fields for Agent name and date range
    agent_name = st.selectbox('Select Agent Name', my_data['Agent name'].unique())

    if pd.isna(min_date) or pd.isna(max_date):
        st.error("Error: No valid dates found in the dataset.")
    else:
        start_date = st.date_input('Start Date', value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input('End Date', value=max_date, min_value=start_date, max_value=max_date)

        # ✅ Convert start_date and end_date to datetime64[ns]
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

        # Filter data
        filtered_data = my_data[(my_data['Agent name'] == agent_name) & 
                                (my_data['Date'].between(start_date, end_date))]

        # Calculate 'Target Achieved'
        filtered_data.loc[:, 'Target Achieved'] = filtered_data['Processed Lots'] >= filtered_data['Target Lots']

        # Display results
        if filtered_data.empty:
            st.warning("No data available for the selected agent and date range.")
        else:
            st.dataframe(filtered_data[['Date', 'Queue', 'Processed Lots', 'Target Lots', 'Reasons', 'Target Achieved']])

            # Check performance
            if filtered_data['Target Achieved'].all():
                st.success('🎯 Target Achieved!')
            else:
                st.warning('⚠️ Target Not Achieved')
