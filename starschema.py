# import pandas as pd
# from sqlalchemy import create_engine

# # Connect to SQL Database
# engine = create_engine('Mysql://username:password@localhost/financial_db')

# # Load Datasets
# financial_data = pd.read_csv("final_financial_data.csv")

# # Load Dim Company Table
# dim_company = financial_data[['Company Name', 'Industry', 'Country']].drop_duplicates().reset_index(drop=True)
# dim_company.to_sql('dim_company', engine, if_exists='replace', index=False)

# # Load Dim Time Table
# dim_time = financial_data[['Year', 'Quarter', 'Month', 'Date']].drop_duplicates().reset_index(drop=True)
# dim_time.to_sql('dim_time', engine, if_exists='replace', index=False)

# # Load Fact Table
# fact_financials = financial_data[['Company Name', 'Year', 'Revenue', 'Net Income', 'Total Assets', 'Total Liabilities']]
# fact_financials.to_sql('fact_financials', engine, if_exists='replace', index=False)

# print("✅ Star Schema Created Successfully!")
import pandas as pd
import mysql.connector

# Load Dataset
file_path = r"F:\Revature_Project\data\final_financial_data.csv"
df = pd.read_csv(file_path)

# MySQL Connection Config
db_config = {
    "host": "127.0.0.1",  # Change to your MySQL server
    "user": "root",  # Your MySQL username
    "password": "Vani@333",  # Your MySQL password
    "database": "financial_reporting"
}

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Create Database
cursor.execute("CREATE DATABASE IF NOT EXISTS financial_db;")
cursor.execute("USE financial_db;")

# Create Tables (Star Schema)
tables_sql = [
    """
    CREATE TABLE IF NOT EXISTS dim_company (
        company_id INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(100) UNIQUE NOT NULL,
        category VARCHAR(50) NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_time (
        time_id INT AUTO_INCREMENT PRIMARY KEY,
        year INT UNIQUE NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_market (
        market_id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT,
        market_cap DECIMAL(15,2),
        FOREIGN KEY (company_id) REFERENCES dim_company(company_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS dim_financials (
        financial_id INT AUTO_INCREMENT PRIMARY KEY,
        ebitda DECIMAL(15,2),
        shareholder_equity DECIMAL(15,2),
        earning_per_share DECIMAL(10,2),
        interest_expense DECIMAL(15,2),
        interest_income DECIMAL(15,2)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS fact_financials (
        fact_id INT AUTO_INCREMENT PRIMARY KEY,
        company_id INT,
        time_id INT,
        market_id INT,
        financial_id INT,
        revenue DECIMAL(15,2),
        gross_profit DECIMAL(15,2),
        net_income DECIMAL(15,2),
        total_revenue DECIMAL(15,2),
        operating_revenue DECIMAL(15,2),
        FOREIGN KEY (company_id) REFERENCES dim_company(company_id),
        FOREIGN KEY (time_id) REFERENCES dim_time(time_id),
        FOREIGN KEY (market_id) REFERENCES dim_market(market_id),
        FOREIGN KEY (financial_id) REFERENCES dim_financials(financial_id)
    );
    """
]

# Execute Table Creation
for query in tables_sql:
    cursor.execute(query)

# Insert Data into Dimension Tables
# dim_company
cursor.executemany(
    "INSERT IGNORE INTO dim_company (company_name, category) VALUES (%s, %s);",
    list(df[['company', 'category']].drop_duplicates().itertuples(index=False, name=None))
)

# dim_time
cursor.executemany(
    "INSERT IGNORE INTO dim_time (year) VALUES (%s);",
    list(df[['year']].drop_duplicates().itertuples(index=False, name=None))
)

# dim_market
cursor.executemany(
    """
    INSERT IGNORE INTO dim_market (company_id, market_cap) 
    SELECT dc.company_id, %s 
    FROM dim_company dc 
    WHERE dc.company_name = %s;
    """,
    list(df[['market cap(in b usd)', 'company']].drop_duplicates().itertuples(index=False, name=None))
)

# dim_financials
cursor.executemany(
    """
    INSERT IGNORE INTO dim_financials (ebitda, shareholder_equity, earning_per_share, interest_expense, interest_income)
    VALUES (%s, %s, %s, %s, %s);
    """,
    list(df[['ebitda_x', 'share holder equity', 'earning per share', 
             'interest expense non operating', 'interest income non operating']]
         .drop_duplicates().itertuples(index=False, name=None))
)

# Insert Data into Fact Table
cursor.execute("""
    INSERT INTO fact_financials (company_id, time_id, market_id, financial_id, revenue, gross_profit, net_income, total_revenue, operating_revenue)
    SELECT 
        dc.company_id,
        dt.time_id,
        dm.market_id,
        df.financial_id,
        ffd.revenue,
        ffd.`gross profit_x`,
        ffd.net_income_x,
        ffd.total_revenue,
        ffd.operating_revenue
    FROM final_financial_data ffd
    JOIN dim_company dc ON ffd.company = dc.company_name
    JOIN dim_time dt ON ffd.year = dt.year
    JOIN dim_market dm ON dc.company_id = dm.company_id
    JOIN dim_financials df ON ffd.ebitda_x = df.ebitda
        AND ffd.`share holder equity` = df.shareholder_equity
        AND ffd.`earning per share` = df.earning_per_share;
""")

conn.commit()

# Reporting Queries
reporting_queries = {
    "Total Revenue per Company": """
        SELECT c.company_name, SUM(f.total_revenue) AS total_revenue
        FROM fact_financials f
        JOIN dim_company c ON f.company_id = c.company_id
        GROUP BY c.company_name
        ORDER BY total_revenue DESC;
    """,
    "Yearly Revenue Trend for AAPL": """
        SELECT t.year, f.total_revenue
        FROM fact_financials f
        JOIN dim_time t ON f.time_id = t.time_id
        JOIN dim_company c ON f.company_id = c.company_id
        WHERE c.company_name = 'AAPL'
        ORDER BY t.year ASC;
    """,
    "Top 10 Companies by Market Cap": """
        SELECT c.company_name, m.market_cap
        FROM dim_market m
        JOIN dim_company c ON m.company_id = c.company_id
        ORDER BY m.market_cap DESC
        LIMIT 10;
    """
}

# Run Reporting Queries
for title, query in reporting_queries.items():
    cursor.execute(query)
    print(f"\n--- {title} ---")
    for row in cursor.fetchall():
        print(row)

# Close Connection
cursor.close()
conn.close()
print("\n✅ Data Inserted and Queries Executed Successfully!")
