import streamlit as st
import pandas as pd

st.title("📊 Agent Performance Tracker (Excel Upload)")

# File upload widget
file = st.file_uploader("📂 Upload your Excel file", type=["xlsx"])

if file is not None:
    # Load Excel file
    df = pd.read_excel(file, sheet_name="Sheet1")  # Adjust sheet name if needed
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True)  # Ensure Date format

    # Show uploaded data
    st.write("### 🔍 Uploaded Data Preview:")
    st.dataframe(df)

    # Agent Selection
    agent_name = st.selectbox("👤 Select Agent Name", df["Agent name"].unique())

    # Date Range Selection
    start_date = st.date_input("📅 Start Date", min_value=df["Date"].min())
    end_date = st.date_input("📅 End Date", min_value=start_date, max_value=df["Date"].max())

    # Filter Data
    filtered_data = df[(df["Agent name"] == agent_name) & 
                       (df["Date"].between(start_date, end_date))]

    # Add 'Target Achieved' column
    filtered_data["Target Achieved"] = filtered_data["Processed Lots"] >= filtered_data["Target Lots"]

    # Show filtered data
    st.write(f"### 📊 Performance Data for {agent_name}:")
    st.dataframe(filtered_data)

    # Display Target Achievement Status
    if filtered_data["Target Achieved"].all():
        st.success("✅ Target Achieved!")
    else:
        st.warning("⚠ Target Not Achieved!")

else:
    st.info("🔹 Please upload an Excel file to proceed.")

