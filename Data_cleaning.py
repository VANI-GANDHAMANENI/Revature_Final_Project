import pandas as pd
import os

# Define the path to the cleaned data folder
data_path = r'F:\Revature_Project\cleaned_data'

# List of required datasets
required_files = [
    "stock_prices.csv",
    "income_statement.csv",
    "balance_sheet.csv",
    "cash_flow.csv",
    "AAPL_income_statement.csv",
    "AAPL_balance_sheet.csv",
    "AAPL_cashflow.csv",
    "AAPL_company_info.csv",
    "Financial Statements.csv",
    "AAPL_historical_data.csv",
    "AAPL_dividends.csv"
]

# Load available datasets
datasets = {}
available_files = os.listdir(data_path)

# Convert to lowercase for case-insensitive comparison
available_files_lower = {file.lower(): file for file in available_files}

for file in required_files:
    file_lower = file.lower()
    if file_lower in available_files_lower:
        full_path = os.path.join(data_path, available_files_lower[file_lower])
        datasets[file] = pd.read_csv(full_path)
        print(f"✅ Loaded: {file}")
    else:
        print(f"❌ Missing: {file}")

# Check if all required datasets are loaded
missing_files = [file for file in required_files if file not in datasets]
if missing_files:
    print(f"\n❌ Required datasets not found in cleaned data folder: {missing_files}")
    exit()

print("\n✅ All required datasets successfully loaded!")
