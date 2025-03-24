import pandas as pd
import numpy as np
import mysql.connector

# ✅ Database Connection
try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Vani@333",
        database="financial_reporting"
    )
    cursor = conn.cursor()
    print("✅ Database connected successfully.")
except mysql.connector.Error as err:
    print(f"❌ Database connection failed: {err}")
    exit()

# ✅ Load CSV
csv_file = r"F:\Revature_Project\data\final_financial_data.csv"
df = pd.read_csv(csv_file)
print(f"📂 Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")

# ✅ Ensure 'net_income' column exists & is a valid FLOAT
possible_columns = ["net income_x", "net income_y", "net income"]
for col in possible_columns:
    if col in df.columns:
        df["net_income"] = df[col]  # Assign first valid column
        print(f"✅ Using '{col}' as 'net_income'.")
        break
else:
    print("❌ 'net_income' column not found in CSV!")
    exit()

# ✅ Convert relevant columns to FLOAT and handle missing values
columns_to_convert = ["revenue", "net_income", "total expenses", "operating income", "current ratio", "net profit margin"]
for col in columns_to_convert:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to float
        df[col] = df[col].fillna(value=np.nan)  # ✅ Corrected fillna method
    else:
        print(f"⚠️ Warning: Column '{col}' missing in CSV.")

# ✅ Insert data into MySQL
sql_query = """
INSERT INTO financial_data (company_id, revenue, net_income, total expenses, operating income, current ratio,net profit margin)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for index, row in df.iterrows():
    values = (
        index + 1,  # Example company_id (replace as needed)
        row['revenue'] if pd.notna(row['revenue']) else None,
        row['net_income'] if pd.notna(row['net_income']) else None,
        row['total expenses'] if pd.notna(row['total expenses']) else None,
        row['operating income'] if pd.notna(row['operating income']) else None,
        row['current ratio'] if pd.notna(row['current ratio']) else None,
        row['net profit margin'] if pd.notna(row['net profit margin']) else None
    )
    
    try:
        cursor.execute(sql_query, values)
    except mysql.connector.Error as err:
        print(f"❌ SQL Error on row {index + 1}: {err}")
        print(f"🚨 Problematic data: {values}")
        continue  # Skip this row and continue

# ✅ Commit & Close Database Connection
conn.commit()
cursor.close()
conn.close()
print("✅ Data inserted successfully. 🔻 Database connection closed.")



# import pandas as pd
# import numpy as np
# import mysql.connector

# # ✅ Database Connection
# try:
#     conn = mysql.connector.connect(
#         host="127.0.0.1",
#         user="root",
#         password="Vani@333",
#         database="financial_reporting"
#     )
#     cursor = conn.cursor()
#     print("✅ Database connected successfully.")
# except mysql.connector.Error as err:
#     print(f"❌ Database connection failed: {err}")
#     exit()

# # ✅ Load CSV
# csv_file = r"F:\Revature_Project\data\final_financial_data.csv"
# df = pd.read_csv(csv_file)
# print(f"📂 Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")

# # ✅ Ensure 'net_income' column exists & is a valid FLOAT
# possible_columns = ["net income_x", "net income_y", "net income"]
# for col in possible_columns:
#     if col in df.columns:
#         df["net_income"] = df[col]  # Assign first valid column
#         print(f"✅ Using '{col}' as 'net_income'.")
#         break
# else:
#     print("❌ 'net_income' column not found in CSV!")
#     exit()

# # ✅ Define expected columns (check if they exist in CSV)
# expected_columns = ["revenue", "net_income", "total_expenses", "operating_income", "current_ratio", "profit_margin"]
# existing_columns = [col for col in expected_columns if col in df.columns]

# # ✅ Convert existing columns to FLOAT and handle missing values
# for col in existing_columns:
#     df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to float
#     df[col] = df[col].fillna(value=np.nan)  # ✅ Replace NaN with np.nan for MySQL NULL

# # ✅ Insert data into MySQL
# sql_query = """
# INSERT INTO financial_data (company_id, revenue, net_income, total_expenses, operating_income, current_ratio, profit_margin)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# """

# for index, row in df.iterrows():
#     values = (
#         index + 1,  # Example company_id (replace as needed)
#         row.get('revenue', None),
#         row.get('net_income', None),
#         row.get('total_expenses', None),
#         row.get('operating_income', None),
#         row.get('current_ratio', None),
#         row.get('profit_margin', None)
#     )
    
#     try:
#         cursor.execute(sql_query, values)
#     except mysql.connector.Error as err:
#         print(f"❌ SQL Error on row {index + 1}: {err}")
#         print(f"🚨 Problematic data: {values}")
#         continue  # Skip this row and continue

# # ✅ Commit & Close Database Connection
# conn.commit()
# cursor.close()
# conn.close()
# print("✅ Data inserted successfully. 🔻 Database connection closed.")
