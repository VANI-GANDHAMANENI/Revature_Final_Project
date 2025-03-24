# import pandas as pd
# import os

# # Define data path

# data_path = r'F:\Revature_Project\data'
# final_file_path = os.path.join(data_path, 'final_financial_data.csv')

# # List of expected CSV files
# csv_files = {
#     "financial_stmts": "Financial Statements.csv",
#     "dataincome_statements": "AAPL_income_statement.csv",
#     "balance_sheets": "AAPL_balance_sheet.csv",
#     "cash_flows": "AAPL_cashflow.csv",
#     "companies": "AAPL_company_info.csv"
# }

# # Load available datasets
# datasets = {}
# for key, filename in csv_files.items():
#     file_path = os.path.join(data_path, filename)
#     if os.path.exists(file_path):
#         datasets[key] = pd.read_csv(file_path)
#         print(f"✅ Loaded: {filename}")
#     else:
#         print(f"❌ File not found: {filename}")

# # Handle missing datasets by creating empty dataframes
# for key in csv_files.keys():
#     if key not in datasets:
#         datasets[key] = pd.DataFrame()
#         print(f"⚠️ Creating empty dataframe for {key}")

# # Data Cleaning & Processing
# for key, df in datasets.items():
#     if not df.empty:
#         df.dropna(inplace=True)
#         df.columns = df.columns.str.strip().str.lower()

# # Rename columns to ensure consistency
# if "company " in datasets["financial_stmts"].columns:
#     datasets["financial_stmts"].rename(columns={"company ": "company"}, inplace=True)

# for key in ["balance_sheets", "cash_flows", "dataincome_statements"]:
#     if "unnamed: 0" in datasets[key].columns:
#         datasets[key].rename(columns={"unnamed: 0": "year"}, inplace=True)

# # Convert "year" column to numeric for merging
# for key in datasets.keys():
#     if "year" in datasets[key].columns:
#         datasets[key]["year"] = datasets[key]["year"].astype(str).str.extract("(\\d+)").astype(float).astype("Int64")

# # Merge datasets on "year"
# df_merged = datasets["financial_stmts"]
# for key in ["balance_sheets", "cash_flows", "dataincome_statements"]:
#     df_merged = df_merged.merge(datasets[key], on="year", how="left")

# df_merged.fillna(0, inplace=True)

# # Check if the merged dataset is empty
# if df_merged.empty:
#     print("❌ Merged dataset is empty! Check input files.")
# else:
#     # Save the dataset using multiple methods to ensure it writes successfully
#     try:
#         df_merged.to_csv(final_file_path, index=False, mode='w', encoding='utf-8')
#         print(f"✅ Data saved successfully at: {final_file_path}")
#     except Exception as e:
#         print(f"❌ Error saving file: {e}")
        
#     # Alternative save method
#     try:
#         with open(final_file_path, 'w', encoding='utf-8') as f:
#             df_merged.to_csv(f, index=False)
#         print(f"✅ Data successfully saved using alternative method: {final_file_path}")
#     except Exception as e:
#         print(f"❌ Alternative save failed: {e}")
    
#     # Load the saved dataset into VS Code
#     try:
#         df_final = pd.read_csv(final_file_path)
#         print("✅ Final financial data loaded successfully!")
        
#         # Display first few rows
#         print(df_final.head())
        
#         # Display column names
#         print("Columns in dataset:", df_final.columns)
        
#         # Aggregate Total Revenue and Average Net Income
#         if "revenue" in df_final.columns:
#             total_revenue = df_final["revenue"].sum()
#             print(f"📊 Total Revenue: {total_revenue}")

#         if "net_income" in df_final.columns:
#             avg_net_income = df_final["net_income"].mean()
#             print(f"📊 Average Net Income: {avg_net_income}")
#     except Exception as e:
#         print(f"❌ Error loading saved file: {e}")
import pandas as pd
import os

# Define data path
data_path = r'F:\Revature_Project\data'
final_file_path = os.path.join(data_path, 'final_financial_data.csv')

# List of expected CSV files
csv_files = {
    "financial_stmts": "Financial Statements.csv",
    "income_statements": "AAPL_income_statement.csv",
    "balance_sheets": "AAPL_balance_sheet.csv",
    "cash_flows": "AAPL_cashflow.csv",
    "companies": "AAPL_company_info.csv"
}

# Load available datasets
datasets = {}
for key, filename in csv_files.items():
    file_path = os.path.join(data_path, filename)
    if os.path.exists(file_path):
        datasets[key] = pd.read_csv(file_path)
        print(f"✅ Loaded: {filename}")
    else:
        print(f"❌ File not found: {filename}")

# Handle missing datasets by creating empty dataframes
for key in csv_files.keys():
    if key not in datasets:
        datasets[key] = pd.DataFrame()
        print(f"⚠️ Creating empty dataframe for {key}")

# Data Cleaning & Processing
for key, df in datasets.items():
    if not df.empty:
        df.dropna(inplace=True)
        df.columns = df.columns.str.strip().str.lower()

# Rename columns to ensure consistency
if "company " in datasets["financial_stmts"].columns:
    datasets["financial_stmts"].rename(columns={"company ": "company"}, inplace=True)

for key in ["balance_sheets", "cash_flows", "income_statements"]:
    if "unnamed: 0" in datasets[key].columns:
        datasets[key].rename(columns={"unnamed: 0": "year"}, inplace=True)

# Convert "year" column to numeric for merging
for key in datasets.keys():
    if "year" in datasets[key].columns:
        datasets[key]["year"] = datasets[key]["year"].astype(str).str.extract("(\\d+)").astype(float).astype("Int64")

# Merge datasets on "year"
df_merged = datasets["financial_stmts"]
for key in ["balance_sheets", "cash_flows", "income_statements"]:
    df_merged = df_merged.merge(datasets[key], on="year", how="left")

df_merged.fillna(0, inplace=True)

# Check if the merged dataset is empty
if df_merged.empty:
    print("❌ Merged dataset is empty! Check input files.")
else:
    # ✅ Calculate Financial Ratios

    # 1️⃣ **Current Ratio** = Total Assets / Total Liabilities
    if "total_assets" in df_merged.columns and "total_liabilities" in df_merged.columns:
        df_merged["current_ratio"] = df_merged["total_assets"] / df_merged["total_liabilities"]

    # 2️⃣ **Return on Assets (ROA)** = Net Income / Total Assets
    if "net_income" in df_merged.columns and "total_assets" in df_merged.columns:
        df_merged["roa"] = df_merged["net_income"] / df_merged["total_assets"]

    # 3️⃣ **Return on Equity (ROE)** = Net Income / Shareholder Equity
    if "net_income" in df_merged.columns and "total_equity" in df_merged.columns:
        df_merged["roe"] = df_merged["net_income"] / df_merged["total_equity"]

    # 4️⃣ **Net Profit Margin** = Net Income / Revenue
    if "net_income" in df_merged.columns and "revenue" in df_merged.columns:
        df_merged["net_profit_margin"] = df_merged["net_income"] / df_merged["revenue"]

    # 5️⃣ **P/E Ratio (Price-to-Earnings)** = Stock Price / Earnings Per Share (EPS)
    if "pe_ratio" in df_merged.columns:
        df_merged["pe_ratio"] = df_merged["pe_ratio"]

    # 6️⃣ **Rate of Interest** = Interest Expense / Total Debt
    if "interest_expense" in df_merged.columns and "total_debt" in df_merged.columns:
        df_merged["rate_of_interest"] = df_merged["interest_expense"] / df_merged["total_debt"]

    # ✅ Save the dataset
    try:
        df_merged.to_csv(final_file_path, index=False, mode='w', encoding='utf-8')
        print(f"✅ Data saved successfully at: {final_file_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

    # ✅ Load the saved dataset
    try:
        df_final = pd.read_csv(final_file_path)
        print("✅ Final financial data loaded successfully!")

        # Display first few rows
        print(df_final.head())

        # Display column names
        print("Columns in dataset:", df_final.columns)

        # 📊 Aggregate Total Revenue and Average Net Income
        if "revenue" in df_final.columns:
            total_revenue = df_final["revenue"].sum()
            print(f"📊 Total Revenue: {total_revenue}")

        if "net_income" in df_final.columns:
            avg_net_income = df_final["net_income"].mean()
            print(f"📊 Average Net Income: {avg_net_income}")

        # 📈 Display calculated ratios
        if "current_ratio" in df_final.columns:
            print(f"📊 Average Current Ratio: {df_final['current_ratio'].mean()}")

        if "roa" in df_final.columns:
            print(f"📊 Return on Assets (ROA): {df_final['roa'].mean()}")

        if "roe" in df_final.columns:
            print(f"📊 Return on Equity (ROE): {df_final['roe'].mean()}")

        if "net_profit_margin" in df_final.columns:
            print(f"📊 Net Profit Margin: {df_final['net_profit_margin'].mean()}")

        if "pe_ratio" in df_final.columns:
            print(f"📊 P/E Ratio: {df_final['pe_ratio'].mean()}")

        if "rate_of_interest" in df_final.columns:
            print(f"📊 Rate of Interest: {df_final['rate_of_interest'].mean()}")

    except Exception as e:
        print(f"❌ Error loading saved file: {e}")
