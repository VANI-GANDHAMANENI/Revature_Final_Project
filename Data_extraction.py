import yfinance as yf
import kaggle
import pandas as pd
import os

# Create a 'data' folder if it doesn't exist
data_folder = "data"
os.makedirs(data_folder, exist_ok=True)


# Define the stock ticker symbol (Change this to any stock symbol you want)
ticker_symbol = "AAPL"  # Example: Apple Inc.

# Fetch data from Yahoo Finance
company = yf.Ticker(ticker_symbol)

# Fetch historical stock prices (Last 1 month)
stock_prices = company.history(period="1mo")
income_statement = company.financials  # Income Statement
balance_sheet = company.balance_sheet  # Balance Sheet
cash_flow = company.cashflow  # Cash Flow Statement

# Save Yahoo Finance data to CSV
stock_prices.to_csv(os.path.join(data_folder, "stock_prices.csv"))
income_statement.to_csv(os.path.join(data_folder, "income_statement.csv"))
balance_sheet.to_csv(os.path.join(data_folder, "balance_sheet.csv"))
cash_flow.to_csv(os.path.join(data_folder, "cash_flow.csv"))


# Set Kaggle API config path
os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\My Pc\.kaggle"
kaggle.api.authenticate()

# Download and unzip the dataset
kaggle.api.dataset_download_files('vanigandhamaneni/financialdata-automation', path=data_folder, unzip=True)

# Read Kaggle dataset files
dataincome_statements = pd.read_csv(os.path.join(data_folder, "AAPL_income_statement.csv"))
balance_sheets = pd.read_csv(os.path.join(data_folder, "AAPL_balance_sheet.csv"))
cash_flows = pd.read_csv(os.path.join(data_folder, "AAPL_cashflow.csv"))
companies = pd.read_csv(os.path.join(data_folder, "AAPL_company_info.csv"))
financial_stmts = pd.read_csv(os.path.join(data_folder, "Financial Statements.csv"))
historical_data = pd.read_csv(os.path.join(data_folder, "AAPL_historical_data.csv"))
dividends = pd.read_csv(os.path.join(data_folder, "AAPL_dividends.csv"))


print("Stock Prices (Yahoo Finance):\n", stock_prices.head())
print("\nIncome Statement (Yahoo Finance):\n", income_statement.head())

print("\nIncome Statement (Kaggle):\n", dataincome_statements.head())
print("\nBalance Sheet (Kaggle):\n", balance_sheets.head())
print("\nCash Flow Statement (Kaggle):\n", cash_flows.head())

print(f"\n✅ All data successfully extracted and saved in the '{data_folder}' folder!")
