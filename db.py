import pandas as pd
import mysql.connector

# ✅ Load CSV
df = pd.read_csv("F:/Revature_Project/data/final_financial_data.csv")

# ✅ Connect to MySQL
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Vani@333",
    database="financial_reporting"
)
cursor = db.cursor()

# ✅ Insert into Company Dimension
company_dict = {}
for company in df['company'].unique():
    cursor.execute("INSERT IGNORE INTO company_dim (company_name) VALUES (%s)", (company,))
    db.commit()
    cursor.execute("SELECT company_id FROM company_dim WHERE company_name = %s", (company,))
    company_dict[company] = cursor.fetchone()[0]

# ✅ Insert into Year Dimension (Fixing numpy.int64 issue)
year_dict = {}
for year in df['year'].unique():
    year = int(year)  # Convert numpy.int64 to int
    cursor.execute("INSERT IGNORE INTO year_dim (fiscal_year) VALUES (%s)", (year,))
    db.commit()
    cursor.execute("SELECT year_id FROM year_dim WHERE fiscal_year = %s", (year,))
    year_dict[year] = cursor.fetchone()[0]

# ✅ Insert into Fact Table (Using original column names with spaces)
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO financial_data (
            company_id, year_id, revenue, net_income, `total expenses`, 
            `operating income`, ebitda, `net profit margin`
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        company_dict[row['company']],
        year_dict[int(row['year'])],  # Convert to int to avoid errors
        row.get('revenue', None),
        row.get('net_income', None),
        row.get('total expenses', None),  # Original column name with space
        row.get('operating income', None),  # Original column name with space
        row.get('ebitda', None),
        row.get('net profit margin', None)  # Original column name with space
    ))
    db.commit()

# ✅ Close Connection
cursor.close()
db.close()
print("✅ Data inserted successfully.")
