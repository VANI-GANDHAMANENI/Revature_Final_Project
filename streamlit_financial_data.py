import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 🔧 Streamlit Page Configuration
st.set_page_config(page_title="Financial Analytics Dashboard", layout="wide")

# ✅ Database Connection Function
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Vani@333", 
        database="financial_reporting"
    )

# ✅ Fetch Data from MySQL
@st.cache_data
def fetch_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT f.revenue, f.`net income_x`, f.`total expenses`, f.ebitda_x, f.`net profit margin`,
               f.company_id, f.year_id, f.category_id, f.market_cap_id, 
               cat.category, mc.`market cap(in b usd)`, y.year, sp.`date`, sp.`open price`, sp.`close price`
        FROM financial_data f
        JOIN company_dim c ON f.company_id = c.company_id
        JOIN year_dim y ON f.year_id = y.year_id
        JOIN category_dim cat ON f.category_id = cat.category_id
        JOIN market_cap_dim mc ON f.market_cap_id = mc.market_cap_id
        JOIN stock_prices_dim sp ON f.stock_id = sp.stock_id
        ORDER BY y.year DESC;
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    
    return pd.DataFrame(data)

# ✅ Load Data
df = fetch_data()

# 🔎 Debugging: Check if Data is Loaded
if df.empty:
    st.error("⚠ No data was fetched from the database. Check your SQL query and database connection.")
    st.stop()

st.write("✅ Data Loaded Successfully. Available columns:", df.columns)

# 🔍 **Sidebar Filters**
st.sidebar.header("🔍 Filter Data")

# Ensure required columns exist before applying filters
category_filter = st.sidebar.multiselect("📌 Select Category", df["category"].unique()) if "category" in df.columns else []
year_filter = st.sidebar.multiselect("📆 Select Year", df["year"].unique()) if "year" in df.columns else []
search_query = st.sidebar.text_input("🔎 Search by Company")

date_range = st.sidebar.date_input("📅 Select Date Range", [])

# ✅ Apply Filters
if category_filter:
    df = df[df["category"].isin(category_filter)]
if year_filter:
    df = df[df["year"].isin(year_filter)]
if search_query:
    df = df[df["company"].str.contains(search_query, case=False, na=False)]
if "date" in df.columns and len(date_range) == 2:
    df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

# 📊 **Key Financial Metrics**
total_revenue = df["revenue"].sum() if "revenue" in df.columns else 0
total_net_income = df["net income_x"].sum() if "net income_x" in df.columns else 0
total_expenses = df["total expenses"].sum() if "total expenses" in df.columns else 0
avg_net_profit_margin = df["net profit margin"].mean() if "net profit margin" in df.columns else 0

st.markdown("### 🧭 *Financial Analytics Dashboard*")
col1, col2, col3, col4 = st.columns(4)

col1.metric("📊 Total Revenue", f"${total_revenue:,.2f}")
col2.metric("💰 Total Net Income", f"${total_net_income:,.2f}")
col3.metric("📉 Total Expenses", f"${total_expenses:,.2f}")
col4.metric("📈 Avg. Net Profit Margin", f"{avg_net_profit_margin:.2f}%")

st.divider()

# 📄 **Data Preview**
st.subheader("💾 Data Preview")
st.dataframe(df, use_container_width=True)

# 📊 **Financial Visualizations**
st.subheader("📊 Insights & Analytics")

if not df.empty:
    # 📊 Revenue by Category
    if "category" in df.columns and "revenue" in df.columns:
        fig1 = px.bar(df, x="category", y="revenue", color="category", title="Total Revenue per Category")
        st.plotly_chart(fig1, use_container_width=True)

    # 📊 Net Income by Category
    if "category" in df.columns and "net income_x" in df.columns:
        fig2 = px.bar(df, x="category", y="net income_x", color="category", title="Total Net Income per Category")
        st.plotly_chart(fig2, use_container_width=True)

    # 📊 Total Expenses by Category
    if "category" in df.columns and "total expenses" in df.columns:
        fig4 = px.bar(df, x="category", y="total expenses", color="category", title="Total Expenses per Category")
        st.plotly_chart(fig4, use_container_width=True)

    # 📊 Net Profit Margin by Category
    if "category" in df.columns and "net profit margin" in df.columns:
        fig3 = px.bar(df, x="category", y="net profit margin", color="category", title="Net Profit Margin per Category")
        st.plotly_chart(fig3, use_container_width=True)

    # 📊 Stock Price Trends
    if "date" in df.columns and "open price" in df.columns and "close price" in df.columns:
        fig_line = px.line(df, x="date", y=["open price", "close price"], markers=True,
                           title="Stock Price Trends (Open vs Close)")
        st.plotly_chart(fig_line, use_container_width=True)

else:
    st.warning("⚠ No data available. Adjust filters or check database connection.")

st.sidebar.markdown("---")
st.success("✅ Data Loaded Successfully!")