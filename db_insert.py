import mysql.connector
import pandas as pd
import os

# ✅ MySQL Database Connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Vani@333",  # Replace with your actual MySQL password
    database="financial_data"
)
cursor = conn.cursor()

# ✅ Create `stock_prices` table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_prices (
        Date DATE,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Volume BIGINT,
        Dividends FLOAT,
        Stock_Splits FLOAT
    )
""")

# ✅ Define File Path
file_path = r"F:\Revature_Project\stock_prices.csv"

if os.path.exists(file_path):
    # ✅ Read CSV File Properly
    df = pd.read_csv(file_path, header=0)  # Ensure first row is treated as header
    
    # ✅ Convert 'Date' column to proper datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True).dt.date  # Fixes timezone issue

    # ✅ Print Data to Debug
    print("📊 First 5 rows of DataFrame:\n", df.head())

    # ✅ Convert DataFrame to List of Tuples
    data_to_insert = [tuple(x) for x in df.to_numpy()]
    print(f"📌 Total rows to insert: {len(data_to_insert)}")

    # ✅ SQL Query for Bulk Insert
    insert_query = """
        INSERT INTO stock_prices (Date, Open, High, Low, Close, Volume, Dividends, Stock_Splits)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # ✅ Insert all rows
    cursor.executemany(insert_query, data_to_insert)
    conn.commit()

    print(f"✅ Successfully inserted {cursor.rowcount} rows into stock_prices table.")

else:
    print(f"❌ Error: {file_path} not found!")

# ✅ Close connection
cursor.close()
conn.close()
print("🔌 Database connection closed.")
