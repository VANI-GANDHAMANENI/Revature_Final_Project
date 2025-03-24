# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import mysql.connector

# # Load CSV Data
# def load_data():
#     df = pd.read_csv(r"data\final_financial_data.csv") 
#     return df

# # Fetch Data from MySQL (Join Fact and Dimension Table)
# def fetch_data_from_mysql():
#     connection = mysql.connector.connect(
#         host="127.0.0.1", user="root", password="Vani@333", database="financial_reporting"
#     )
    
#     # SQL query to join fact and dimension tables
#     query = """
#     SELECT f.*, d.company, y.year
#     FROM financial_data f
#     JOIN company_dim d ON f.company_id = d.company_id
#     JOIN year_dim y ON f.year_id = y.year_id
#     """
    
#     df = pd.read_sql(query, connection)
#       # Print columns to check the result
#     connection.close()
#     return df

# # Streamlit App
# st.title("📊 Financial Data Dashboard")

# # Load Data
# data_source = st.sidebar.radio("Select Data Source", ["CSV", "MySQL"])
# if data_source == "CSV":
#     df = load_data()
# else:
#     df = fetch_data_from_mysql()

# # Check if the 'company' column exists
# if 'company' not in df.columns:
#     st.error("'company' column not found in the data. Please check the column names.")
# else:
#     # Sidebar Filters
#     company_list = df["company"].unique()
#     selected_company = st.sidebar.selectbox("Select Company", company_list)
    
#     # Check if the 'year' column exists after joining tables
#     if 'year' not in df.columns:
#         st.error("'year' column not found. Please check your SQL query and column names.")
#     else:
#         year_list = sorted(df["year"].unique(), reverse=True)
#         selected_year = st.sidebar.selectbox("Select Year", year_list)

#         # Filtered Data
#         df_filtered = df[(df["company"] == selected_company) & (df["year"] == selected_year)]

#         # Display Financial Summary
#         st.subheader(f"Financial Summary for {selected_company} in {selected_year}")
#         st.dataframe(df_filtered)

#         # Metrics selection based on the data source
#         if data_source == "CSV":
#             metrics = ["revenue", "net income_x", "ebitda_x", "earning per share", "roe"]  # Keep 'roe' and 'eps' for CSV
#         else:
#             metrics = ["revenue", "net income_x", "ebitda_x", "total expenses", "net profit margin"]  # Replace 'roe' and 'eps' with 'total expenses' and 'net profit margin' for MySQL

#         selected_metric = st.sidebar.selectbox("Select Metric", metrics)

#         st.subheader(f"{selected_metric} Over Time")
#         fig, ax = plt.subplots(figsize=(10, 5))
#         sns.lineplot(data=df[df["company"] == selected_company], x="year", y=selected_metric, marker='o', ax=ax)
#         plt.xlabel("Year")
#         plt.ylabel(selected_metric)
#         plt.title(f"{selected_company} {selected_metric} Trend")
#         st.pyplot(fig)







import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch data from MySQL (replace this with your existing function if needed)
def fetch_data_from_mysql():
    connection = mysql.connector.connect(
        host="127.0.0.1", user="root", password="Vani@333", database="financial_reporting"
    )
    
    query = """
    SELECT f.*, d.company, y.year
    FROM financial_data f
    JOIN company_dim d ON f.company_id = d.company_id
    JOIN year_dim y ON f.year_id = y.year_id
    """
    
    df = pd.read_sql(query, connection)
    connection.close()
    return df

# Load CSV Data (if needed)
def load_data():
    df = pd.read_csv("final_financial_data.csv")  
    return df

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a Page", ["Information", "Dashboard", "Database Schema", "KPI"])

# Information Page
if page == "Information":
    st.title("📊 Financial Reporting Automation Framework")
    st.header("Project Information")
    st.write("""
    This project is focused on automating financial reporting for companies by fetching data from multiple sources,
    transforming and cleaning it, and presenting it in an easy-to-understand dashboard. 
    It integrates financial data, such as revenue, net income, expenses, and stock prices, into a MySQL database.
    
    The main goal of the project is to build an automated reporting framework that allows financial data analysis and visualization.
             
    Key Features:
    - Consolidates financial data from various sources (CSV, Kaggle, Yahoo Finance API).
    - Implements a star schema for financial data storage in MySQL.
    - Automates data extraction, cleaning, and transformation using Python.
    - Generates financial statements and visualizations using Streamlit and Matplotlib/Seaborn.
    - Facilitates automated period-end analysis and generates key financial metrics.
    
    ### Tools & Technologies:
    - Python, MySQL, Pandas, Matplotlib, Seaborn, Streamlit
    - MySQL Database: For storing financial data using dimensional modeling (Star Schema)
    - Streamlit: For creating an interactive web application for financial reporting
    
    ### Objective:
    - To automate financial reporting, provide insights, and make financial analysis more efficient.
    """)

# Dashboard Page
elif page == "Dashboard":
    st.title("📊 Financial Reporting Dashboard")
    
    # Load data from MySQL
    df = fetch_data_from_mysql()

    # Sidebar filters for selecting company and year
    company_list = df["company"].unique()
    selected_company = st.sidebar.selectbox("Select Company", company_list)

    # Get the years that have data for the selected company
    available_years = df[df["company"] == selected_company]["year"].unique()
    year_list = sorted(available_years, reverse=True)  # Sort the years in descending order

    if len(year_list) == 0:
        st.error(f"No data available for {selected_company}.")
    else:
        selected_year = st.sidebar.selectbox("Select Year", year_list)

        # Filter the data based on selected company and year
        df_filtered = df[(df["company"] == selected_company) & (df["year"] == selected_year)]

        # Check if data is available
        if not df_filtered.empty:
            st.subheader(f"Financial Summary for {selected_company} in {selected_year}")
            st.dataframe(df_filtered)

            # Metrics selection based on the data source
            metrics = ["revenue", "net income_x", "ebitda_x", "total expenses", "net profit margin"]

            selected_metric = st.sidebar.selectbox("Select Metric", metrics)

            # Display selected metric over time
            st.subheader(f"{selected_metric} Over Time")
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=df[df["company"] == selected_company], x="year", y=selected_metric, marker='o', ax=ax)
            plt.xlabel("Year")
            plt.ylabel(selected_metric)
            plt.title(f"{selected_company} {selected_metric} Trend")
            st.pyplot(fig)

        else:
            st.error("No data found for the selected company and year.")

# Database Schema Page
elif page == "Database Schema":
    st.title("📊 Database Schema Overview")
    st.write("""
    This schema represents the logical design of the database for the Financial Reporting Automation Framework.  
    It includes:
    - **Company Dimension**
    - **Year Dimension**
    - **Category Dimension**
    - **Stock Prices Dimension**
    - **Market Cap Dimension**
    - **Financial Data Fact Table**
    
    The schema allows us to efficiently store, retrieve, and analyze financial data across multiple dimensions.
    """)

    # Display the schema image (make sure the file path is correct)
    schema_image_path = r"C:\Users\My Pc\Desktop\schema_diagram.jpg"
    st.image(schema_image_path, caption="Database Schema", use_container_width=True)

# KPI Page
elif page == "KPI":
    st.title("📊 Key Performance Indicators (KPIs) Dashboard")

    # Load data from MySQL
    df = fetch_data_from_mysql()

    # Sidebar filters for selecting company and year
    company_list = df["company"].unique()
    selected_company = st.sidebar.selectbox("Select Company", company_list)

    # Get the years that have data for the selected company
    available_years = df[df["company"] == selected_company]["year"].unique()
    year_list = sorted(available_years, reverse=True)  # Sort the years in descending order

    if len(year_list) == 0:
        st.error(f"No data available for {selected_company}.")
    else:
        selected_year = st.sidebar.selectbox("Select Year", year_list)

        # Filter the data based on selected company and year
        df_filtered = df[(df["company"] == selected_company) & (df["year"] == selected_year)]

        # Check if data is available
        if not df_filtered.empty:
            # Extract KPIs from the data
            revenue = df_filtered["revenue"].iloc[0]
            net_income = df_filtered["net income_x"].iloc[0]
            ebitda = df_filtered["ebitda_x"].iloc[0]

            # Display KPIs using st.metric
            st.subheader(f"Key Performance Indicators (KPI) for {selected_company} in {selected_year}")

            st.metric(label="Revenue", value=f"${revenue:,.2f}")
            st.metric(label="Net Income", value=f"${net_income:,.2f}")
            st.metric(label="EBITDA", value=f"${ebitda:,.2f}")

            # Additional KPI - Profit Margin
            if revenue != 0:
                profit_margin = (net_income / revenue) * 100
                st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%")
            else:
                st.metric(label="Profit Margin", value="N/A")
        else:
            st.error("No data found for the selected company and year.")