# import pandas as pd
# import os

# # Define data path
# data_path = r'C:\Users\My Pc\.kaggle\data'

# # Define expected CSV files
# csv_files = {
#     "financial_stmts": "Financial Statements.csv",
#     "dataincome_statements": "AAPL_income_statement.csv",
#     "balance_sheets": "AAPL_balance_sheet.csv",
#     "cash_flows": "AAPL_cashflow.csv",
#     "companies": "AAPL_company_info.csv"
# }

# # Load datasets
# datasets = {}
# for key, filename in csv_files.items():
#     file_path = os.path.join(data_path, filename)
#     if os.path.exists(file_path):
#         datasets[key] = pd.read_csv(file_path)
#         print(f"✅ Loaded: {filename}")
#     else:
#         datasets[key] = pd.DataFrame()  # Create empty DataFrame if file not found
#         print(f"❌ File not found: {filename}")

# # Ensure all datasets have a common 'year' column
# for key, df in datasets.items():
#     if not df.empty:
#         df.dropna(inplace=True)  # Remove missing values
#         df.columns = df.columns.str.strip().str.lower()  # Standardize column names
        
#         # Rename common columns for consistency
#         if "company " in df.columns:
#             df.rename(columns={"company ": "company"}, inplace=True)
        
#         if "unnamed: 0" in df.columns:
#             df.rename(columns={"unnamed: 0": "year"}, inplace=True)

#         # Convert 'year' column to numeric format
#         if "year" in df.columns:
#             df["year"] = df["year"].astype(str).str.extract("(\\d+)").astype(float).astype("Int64")

# # Ensure 'financial_stmts' has 'year' and at least one financial metric column
# if "year" not in datasets["financial_stmts"].columns:
#     print("❌ 'year' column missing in financial statements. Merging will fail!")
# else:
#     # Merge all datasets on 'year' using an outer join to preserve all available data
#     df_merged = datasets["financial_stmts"]
#     for key in ["balance_sheets", "cash_flows", "dataincome_statements"]:
#         if not datasets[key].empty:
#             df_merged = df_merged.merge(datasets[key], on="year", how="outer")  # Outer join retains all data

#     # Fill NaN values with 0 for numeric analysis
#     df_merged.fillna(0, inplace=True)

#     # Remove duplicate or unwanted columns
#     df_merged = df_merged.loc[:, ~df_merged.columns.duplicated()]

#     # Save cleaned dataset
#     output_file = os.path.join(data_path, 'final_financial_data.csv')
#     df_merged.to_csv(output_file, index=False)

#     print(f"✅ Data Merging Successful! Saved to {output_file}")

# # Display final data preview
# print(df_merged.head())
import pandas as pd
import os

# Define path to cleaned datasets
data_path = r'F:\Revature_Project\cleaned_data'

# Load required datasets
files = {
    "income_statement": "income_statement.csv",
    "balance_sheet": "balance_sheet.csv",
    "cash_flow": "cash_flow.csv",
    "financial_statements": "Financial Statements.csv"
""
}

# Load datasets into Pandas
data = {}
for key, filename in files.items():
    file_path = os.path.join(data_path, filename)
    if os.path.exists(file_path):
        data[key] = pd.read_csv(file_path)
        print(f"✅ Loaded: {filename}")
    else:
        print(f"❌ Missing: {filename}")

# Ensure all datasets are loaded before analysis
if any(df.empty for df in data.values()):
    print("❌ Some datasets are missing or empty. Exiting...")
    exit()

# Convert year column to integer
for key, df in data.items():
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce').fillna(0).astype(int)

# Merge datasets on "year"
df_merged = data["financial_statements"]
for key in ["income_statement", "balance_sheet", "cash_flow"]:
    df_merged = df_merged.merge(data[key], on="year", how="left")

df_merged.fillna(0, inplace=True)

# Ensure required columns exist
if "revenue" not in df_merged.columns or "net_income" not in df_merged.columns:
    print("❌ 'Revenue' or 'Net Income' column is missing! Cannot proceed.")
    exit()

# 🔹 Revenue vs. Expenses Analysis
df_merged["total_expenses"] = df_merged["revenue"] - df_merged["net_income"]
df_merged["revenue_vs_expenses"] = df_merged["revenue"] - df_merged["total_expenses"]

# 🔹 Profit Margin Calculations
df_merged["net_profit_margin"] = df_merged["net_income"] / df_merged["revenue"]
df_merged["operating_profit_margin"] = df_merged["operating_cash_flow"] / df_merged["revenue"]

# 🔹 Year-on-Year Growth Analysis
df_merged["revenue_growth"] = df_merged["revenue"].pct_change() * 100
df_merged["net_income_growth"] = df_merged["net_income"].pct_change() * 100

# 🔹 Correlation Analysis
correlation_matrix = df_merged[["revenue", "net_income", "total_assets", "roe", "roa"]].corr()

# Print Key Metrics
print("\n📊 Revenue vs. Expenses:")
print(df_merged[["year", "revenue", "total_expenses", "revenue_vs_expenses"]])

print("\n📈 Profit Margins:")
print(df_merged[["year", "net_profit_margin", "operating_profit_margin"]])

print("\n📊 Year-on-Year Growth:")
print(df_merged[["year", "revenue_growth", "net_income_growth"]])

print("\n🔍 Correlation Matrix:")
print(correlation_matrix)

# Save final results
output_path = os.path.join(data_path, "financial_analysis_results.csv")
df_merged.to_csv(output_path, index=False)
print(f"\n✅ Financial Analysis Completed! Results saved to: {output_path}")
