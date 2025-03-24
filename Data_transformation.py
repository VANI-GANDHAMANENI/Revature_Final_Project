import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

# Create 'transformed_data' folder if it doesn't exist
transformed_folder = "transformed_data"
os.makedirs(transformed_folder, exist_ok=True)

# List of cleaned files to transform
files_to_transform = [
    "stock_prices.csv",
    "income_statement.csv",
    "balance_sheet.csv",
    "cash_flow.csv",
    "AAPL_income_statement.csv",
    "AAPL_balance_sheet.csv",
    "AAPL_cash_flow.csv",
    "AAPL_company_info.csv",
    "financial_statements.csv",
    "AAPL_historical_data.csv",
    "AAPL_dividends.csv"
]

# Initialize MinMaxScaler for numerical normalization
scaler = MinMaxScaler()

# Initialize LabelEncoder for categorical data
label_encoder = LabelEncoder()

# Function to transform data
def transform_dataframe(df):
    # Ensure 'Date' column exists and convert it to datetime
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Convert to datetime format

    # Normalize numerical columns (excluding 'Date')
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if "Date" in df.columns:
        numeric_cols = [col for col in numeric_cols if col != "Date"]  # Exclude Date from transformation

    if numeric_cols:  # Only apply transformation if numerical columns exist
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    # Encode categorical columns
    for col in df.select_dtypes(include=["object"]).columns:
        if df[col].nunique() < 50:  # Only encode if unique values are manageable
            df[col].fillna("Unknown", inplace=True)  # Replace NaN with 'Unknown'
            df[col] = label_encoder.fit_transform(df[col].astype(str))

    return df

# Process each file
for file in files_to_transform:
    file_path = os.path.join("cleaned_data", file)

    if os.path.exists(file_path):
        # Load the file without parsing dates initially
        df = pd.read_csv(file_path)

        # Check if "Date" column exists before parsing it
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")  # Convert 'Date' column if available

        # Transform the dataset
        df = transform_dataframe(df)

        # Save transformed data
        transformed_path = os.path.join(transformed_folder, file)
        df.to_csv(transformed_path, index=False)
        print(f"✅ Transformed file saved: {transformed_path}")

print("\n✅ All data transformed and stored in 'transformed_data' folder!")

# Verify the Date column in one transformed file
sample_file = "stock_prices.csv"
sample_path = os.path.join(transformed_folder, sample_file)
if os.path.exists(sample_path):
    df_transformed = pd.read_csv(sample_path)
    print(df_transformed.head())
