# # import pymysql
# # import pandas as pd

# # # ✅ Step 1: Database connection
# # def connect_db():
# #     try:
# #         conn = pymysql.connect(
# #             host="127.0.0.1",
# #             user="root",
# #             password="Vani@333",
# #             database="financial_reporting"
# #         )
# #         cursor = conn.cursor()
# #         print("✅ Database connected successfully.")
# #         return conn, cursor
# #     except pymysql.MySQLError as e:
# #         print(f"❌ Database connection failed: {e}")
# #         exit()

# # # ✅ Step 2: Load CSV and Normalize Column Names
# # def load_csv(file_path):
# #     try:
# #         df = pd.read_csv(file_path)
# #         print(f"📂 Loaded CSV with {df.shape[0]} rows and {df.shape[1]} columns.")

# #         # Normalize column names (lowercase & strip spaces)
# #         df.columns = df.columns.str.lower().str.strip()

# #         # Print actual column names for debugging
# #         print("🔍 Actual columns in CSV:", df.columns.tolist())

# #         # ✅ Improved Column Mapping (Alternative Names)
# #         column_mapping = {
# #             "company": "company",
# #             "total revenue": "total_revenue",
# #             "operating income": "operating_income",
# #             "net income_x": "net_income",  # ✅ Choose the correct version of net income
# #             "net income_y": "net_income",  # Backup option if needed
# #             "total expenses": "total_expenses",
# #             "current ratio": "current_ratio",
# #             "net profit margin": "profit_margin"
# #         }

# #         # Rename columns using the mapping
# #         df.rename(columns=column_mapping, inplace=True)

# #         # ✅ Ensure "net_income" exists
# #         if "net_income" not in df.columns:
# #             print("⚠️ Warning: 'net_income' column is still missing. Trying alternative columns...")

# #             # ✅ Try finding an alternative column if 'net_income' is missing
# #             possible_columns = ["net income_x", "net income_y", "net income"]
# #             for col in possible_columns:
# #                 if col in df.columns:
# #                     df["net_income"] = df[col]  # Copy existing column to new name
# #                     print(f"✅ Using '{col}' as 'net_income'.")
# #                     break

# #         # ✅ Check if all required columns exist
# #         required_columns = {"company", "total_revenue", "net_income", "total_expenses", "operating_income", "current_ratio", "profit_margin"}
# #         missing_columns = required_columns - set(df.columns)

# #         if missing_columns:
# #             print(f"❌ Missing columns in CSV after renaming: {missing_columns}")
# #             exit()

# #         return df
# #     except Exception as e:
# #         print(f"❌ Error loading CSV: {e}")
# #         exit()

# # # ✅ Step 3: Insert Data into MySQL
# # def insert_into_db(cursor, conn, df):
# #     if df.empty:
# #         print("⚠️ DataFrame is empty. No data to insert.")
# #         return

# #     for index, row in df.iterrows():
# #         print(f"\n🔍 Processing row {index + 1}: {row.to_dict()}")

# #         # Fetch company_id from dim_company table
# #         cursor.execute("SELECT company_id FROM dim_company WHERE company_name = %s", (row['company'],))
# #         company_result = cursor.fetchone()

# #         if company_result:
# #             company_id = company_result[0]
# #             print(f"✅ Found company '{row['company']}' with ID {company_id}.")
# #         else:
# #             print(f"⚠️ Warning: Company '{row['company']}' not found in dim_company! Skipping row.")
# #             continue  # Skip if company not found

# #         # Insert into fact_financials
# #         insert_query = """
# #         INSERT INTO fact_financials 
# #         (company_id, total_revenue, net_income, total_expenses, operating_income, current_ratio, profit_margin)
# #         VALUES (%s, %s, %s, %s, %s, %s, %s)
# #         """
# #         values = (
# #             company_id, 
# #             row['total_revenue'], 
# #             row['net_income'], 
# #             row['total_expenses'], 
# #             row['operating_income'], 
# #             row['current_ratio'], 
# #             row['profit_margin']
# #         )

# #         try:
# #             cursor.execute(insert_query, values)
# #             print(f"✅ Successfully inserted row {index + 1}.")
# #         except pymysql.MySQLError as e:
# #             print(f"❌ SQL Error on row {index + 1}: {e}")

# #     conn.commit()
# #     print("\n✅ All data inserted successfully!")

# # # ✅ Step 4: Main function
# # def main():
# #     conn, cursor = connect_db()
# #     file_path = r"F:\Revature_Project\data\final_financial_data.csv"
# #     df = load_csv(file_path)
# #     insert_into_db(cursor, conn, df)
    
# #     cursor.close()
# #     conn.close()
# #     print("🔻 Database connection closed.")

# # # ✅ Run the script
# # if __name__ == "__main__":
# #     main()





# # 

# import pandas as pd
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

# # ✅ Convert relevant columns to FLOAT and handle missing values
# columns_to_convert = ["revenue", "net_income", "total_expenses", "operating_income", "current_ratio", "profit_margin"]
# for col in columns_to_convert:
#     if col in df.columns:
#         df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to float
#         df[col] = df[col].fillna(value=None)  # ✅ Corrected fillna method
#     else:
#         print(f"⚠️ Warning: Column '{col}' missing in CSV.")

# # ✅ Insert data into MySQL
# sql_query = """
# INSERT INTO financial_data (company_id,revenue, net_income, total_expenses, operating_income, current_ratio, profit_margin)
# VALUES (%s, %s, %s, %s, %s, %s, %s)
# """

# for index, row in df.iterrows():
#     values = (
#         index + 1,  # Example company_id (replace as needed)
#         row['revenue'] if pd.notna(row['revenue']) else None,
#         row['net_income'] if pd.notna(row['net_income']) else None,
#         row['total_expenses'] if pd.notna(row['total_expenses']) else None,
#         row['operating_income'] if pd.notna(row['operating_income']) else None,
#         row['current_ratio'] if pd.notna(row['current_ratio']) else None,
#         row['profit_margin'] if pd.notna(row['profit_margin']) else None
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
columns_to_convert = ["revenue", "net_income", "total expenses", "operating income", "current_ratio", "profit_margin"]
for col in columns_to_convert:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to float
        df[col] = df[col].fillna(value=np.nan)  # ✅ Corrected fillna method
    else:
        print(f"⚠️ Warning: Column '{col}' missing in CSV.")

# ✅ Insert data into MySQL
sql_query = """
INSERT INTO financial_data (company_id, revenue, net_income, total expenses, operating income, current ratio, profit margin)
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
        row['profit margin'] if pd.notna(row['profit margin']) else None
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
