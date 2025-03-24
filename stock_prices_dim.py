import pandas as pd
import mysql.connector

# ✅ Connect to MySQL Database
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Vani@333",
    database="financial_reporting"
)
cursor = db.cursor()

# ✅ Load CSV File
file_path = r"F:\Revature_Project\data\final_financial_data.csv"
df = pd.read_csv(file_path)

# ✅ Print Columns to Debug
# print("Columns in CSV:", df.columns.tolist())

# ✅ Select only needed columns from the dataset
# If you don't need 'company', remove it; otherwise, ensure your table has a matching column.
stock_price_df = df[['year', 'company', 'earning per share', 'ordinary shares number', 'cash dividends paid']].copy()
print(stock_price_df.head())
# ✅ Rename Columns to prepare for insertion:
# We'll use underscore naming for DataFrame keys, though SQL still uses backticks for names with spaces.
stock_price_df.rename(columns={
    'year': 'date',
    'earning per share': 'close_price',  
    'ordinary shares number': 'stock_splits',
    'cash dividends paid': 'dividends'
}, inplace=True)

# ✅ Convert the 'date' column from just year to a full date (assume January 1st)
# This will convert e.g., 2022 --> '2022-01-01'
stock_price_df['date'] = pd.to_datetime(stock_price_df['date'], format='%Y').dt.strftime('%Y-%m-%d')

# ✅ Decide on a strategy for the 'company' column:
# Option 1: Remove the company column from insertion if your table does not have it.
# Option 2: Ensure your table has a company column (e.g., ALTER TABLE stock_prices_dim ADD COLUMN `company` VARCHAR(255);)
#
# For this example, we'll assume the table has a 'company' column.
# If not, remove the company parts from the SELECT and INSERT statements.

# ✅ Prepare the INSERT statement.
# Note: Use backticks around column names if they include spaces.
insert_query = """
    INSERT INTO stock_prices_dim (`date`, `company`, `close price`, `stock splits`, `dividends`)
    VALUES (%s, %s, %s, %s, %s)
"""

# ✅ Insert Data into `stock_prices_dim` Table
for _, row in stock_price_df.iterrows():
    cursor.execute(insert_query, (
        row['date'], 
        row['company'], 
        row['close_price'], 
        row['stock_splits'], 
        row['dividends']
    ))

# ✅ Commit & Close Connection
db.commit()
cursor.close()
db.close()
print("✅ Data Inserted Successfully!")



