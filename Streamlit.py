import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# Load CSV Data
def load_data():
    df = pd.read_csv(r"data\final_financial_data.csv") 
    return df

# Fetch Data from MySQL (Join Fact and Dimension Table)
def fetch_data_from_mysql():
    connection = mysql.connector.connect(
        host="127.0.0.1", user="root", password="Vani@333", database="financial_reporting"
    )
    
    # SQL query to join fact and dimension tables
    query = """
    SELECT f.*, d.company, y.year
    FROM financial_data f
    JOIN company_dim d ON f.company_id = d.company_id
    JOIN year_dim y ON f.year_id = y.year_id
    """
    
    df = pd.read_sql(query, connection)
      # Print columns to check the result
    connection.close()
    return df

# Streamlit App
st.title("📊 Financial Data Dashboard")

# Load Data
data_source = st.sidebar.radio("Select Data Source", ["CSV", "MySQL"])
if data_source == "CSV":
    df = load_data()
else:
    df = fetch_data_from_mysql()

# Check if the 'company' column exists
if 'company' not in df.columns:
    st.error("'company' column not found in the data. Please check the column names.")
else:
    # Sidebar Filters
    company_list = df["company"].unique()
    selected_company = st.sidebar.selectbox("Select Company", company_list)
    
    # Check if the 'year' column exists after joining tables
    if 'year' not in df.columns:
        st.error("'year' column not found. Please check your SQL query and column names.")
    else:
        year_list = sorted(df["year"].unique(), reverse=True)
        selected_year = st.sidebar.selectbox("Select Year", year_list)

        # Filtered Data
        df_filtered = df[(df["company"] == selected_company) & (df["year"] == selected_year)]

        # Display Financial Summary
        st.subheader(f"Financial Summary for {selected_company} in {selected_year}")
        st.dataframe(df_filtered)

        # Metrics selection based on the data source
        if data_source == "CSV":
            metrics = ["revenue", "net income_x", "ebitda_x", "earning per share", "roe"]  # Keep 'roe' and 'eps' for CSV
        else:
            metrics = ["revenue", "net income_x", "ebitda_x", "total expenses", "net profit margin"]  # Replace 'roe' and 'eps' with 'total expenses' and 'net profit margin' for MySQL

        selected_metric = st.sidebar.selectbox("Select Metric", metrics)

        st.subheader(f"{selected_metric} Over Time")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df[df["company"] == selected_company], x="year", y=selected_metric, marker='o', ax=ax)
        plt.xlabel("Year")
        plt.ylabel(selected_metric)
        plt.title(f"{selected_company} {selected_metric} Trend")
        st.pyplot(fig)

st.write("Developed by Vani")





