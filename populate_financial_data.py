import mysql.connector
import pandas as pd
import os

# ✅ MySQL Connection
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Vani@333",  # Replace with your actual MySQL password
    database="financial_reporting"
)
cursor = db.cursor()

# ✅ Define File Path
file_path = "F:/Revature_Project/data/final_financial_data.csv"

# ✅ Check if file exists
if not os.path.exists(file_path):
    print(f"❌ Error: File {file_path} not found!")
    exit()

# ✅ Load Financial Data CSV
df = pd.read_csv(file_path)

# ✅ Print actual column names for debugging
print("📌 Column Names in CSV:", df.columns.tolist())

# ✅ Standardize column names (Remove spaces & lowercase for consistency)
df.rename(columns=lambda x: x.strip().lower(), inplace=True)

# ✅ Add missing date column using the 'year' column
df['date'] = df['year'].astype(str) + "-01-01"  # Default to January 1st of that year

# ✅ Required Columns for Financial Data
required_cols = {'company', 'year', 'revenue', 'net income_x', 'total expenses', 
                 'operating income', 'ebitda_x', 'net profit margin', 'category', 'market cap(in b usd)', 'date'}
missing_cols = required_cols - set(df.columns)

if missing_cols:
    print(f"❌ Error: Missing columns in CSV: {missing_cols}")
    exit()

# ✅ Function to get Dimension Table ID (Insert if not found)
def get_dimension_id(table_name, column_name, value):
    if pd.isna(value):
        return None  # Handle NULL values
    query = f"SELECT {table_name[:-4]}_id FROM {table_name} WHERE `{column_name}` = %s"
    cursor.execute(query, (value,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        insert_query = f"INSERT INTO {table_name} (`{column_name}`) VALUES (%s)"
        cursor.execute(insert_query, (value,))
        db.commit()
        return cursor.lastrowid

# ✅ Insert into Year Dimension
year_dict = {}
for year in df['year'].unique():
    year = int(year)  # Convert NumPy int64 to Python int
    cursor.execute("SELECT year_id FROM year_dim WHERE year = %s", (year,))
    result = cursor.fetchone()
    if result:
        year_dict[year] = result[0]
    else:
        cursor.execute("INSERT INTO year_dim (year) VALUES (%s)", (year,))
        db.commit()
        year_dict[year] = cursor.lastrowid

print("✅ Year dimension populated successfully.")

# ✅ Insert into Stock Prices Dimension
stock_dict = {}
for index, row in df.iterrows():
    stock_date = row['date']
    cursor.execute("SELECT stock_id FROM stock_prices_dim WHERE `date` = %s", (stock_date,))
    result = cursor.fetchone()
    if result:
        stock_dict[stock_date] = result[0]
    else:
        insert_query = """
            INSERT INTO stock_prices_dim (`date`, `open price`, `high price`, `low price`, 
                                          `close price`, `volume`, `dividends`, `stock splits`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            stock_date, row.get("open price", 0), row.get("high price", 0), row.get("low price", 0),
            row.get("close price", 0), row.get("volume", 0), row.get("dividends", 0), row.get("stock splits", 0)
        )
        cursor.execute(insert_query, values)
        db.commit()
        stock_dict[stock_date] = cursor.lastrowid

print("✅ Stock prices dimension populated successfully.")

# ✅ Insert into Financial Data Fact Table
for index, row in df.iterrows():
    stock_id = stock_dict.get(row['date'])
    company_id = get_dimension_id("company_dim", "company", row["company"])
    year_id = year_dict.get(row["year"])
    category_id = get_dimension_id("category_dim", "category", row["category"])
    market_cap_id = get_dimension_id("market_cap_dim", "market cap(in b usd)", row["market cap(in b usd)"])

    insert_query = """
        INSERT INTO financial_data (
            `stock_id`, `company_id`, `year_id`, `category_id`, `market_cap_id`, 
            `revenue`, `net income_x`, `ebitda_x`, `total expenses`, `net profit margin`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        stock_id, company_id, year_id, category_id, market_cap_id, 
        row["revenue"], row["net income_x"], row["ebitda_x"], 
        row["total expenses"], row["net profit margin"]
    )

    cursor.execute(insert_query, values)
    db.commit()

print("✅ Financial data fact table populated successfully.")

# ✅ Close Database Connection
cursor.close()
db.close()
print("🔌 Database connection closed.")
