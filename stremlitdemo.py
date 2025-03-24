import streamlit as st
import yfinance as yf
import pandas as pd

# Function to fetch financial data
def fetch_financial_data(ticker, period="1y"):
    try:
        company = yf.Ticker(ticker)
        return {
            "Stock Prices": company.history(period=period),
            "Income Statement": company.financials,
            "Balance Sheet": company.balance_sheet,
            "Cash Flow Statement": company.cashflow,
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to calculate financial ratios
def calculate_financial_ratios(balance_sheet, income_statement):
    ratios = {}
    try:
        ratios["Current Ratio"] = balance_sheet.loc["Total Current Assets"].iloc[0] / balance_sheet.loc["Total Current Liabilities"].iloc[0]
        ratios["Debt-to-Equity Ratio"] = balance_sheet.loc["Total Liabilities"].iloc[0] / balance_sheet.loc["Total Stockholder Equity"].iloc[0]
        ratios["Net Profit Margin"] = income_statement.loc["Net Income"].iloc[0] / income_statement.loc["Total Revenue"].iloc[0]
    except Exception as e:
        st.warning("Some financial ratios could not be calculated due to missing data.")
    return ratios

# Streamlit app layout
def main():
    st.title("📊 Financial Statement Generator")
    
    # User input for company ticker and period
    ticker = st.text_input("Enter Stock Ticker Symbol (e.g., AAPL, TSLA, MSFT)", "AAPL")
    period = st.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y", "2y","3y"])
    
    statement_type = st.selectbox("Select Financial Statement", ["Stock Prices", "Income Statement", "Balance Sheet", "Cash Flow Statement"])
    
    if st.button("Generate Report"):
        data = fetch_financial_data(ticker, period)
        
        if data and statement_type in data:
            st.subheader(statement_type)
            st.dataframe(data[statement_type])
            
            if statement_type == "Stock Prices":
                st.line_chart(data[statement_type]["Close"])
            
            if statement_type in ["Income Statement", "Balance Sheet"]:
                ratios = calculate_financial_ratios(data["Balance Sheet"], data["Income Statement"])
                st.subheader("📈 Key Financial Ratios")
                for key, value in ratios.items():
                    st.write(f"**{key}:** {value:.2f}")
                
            # Export functionality
            csv = data[statement_type].to_csv()
            st.download_button(
                label=f"Download {statement_type} as CSV",
                data=csv,
                file_name=f"{statement_type.lower().replace(' ', '_')}.csv",
                mime='text/csv',
            )

if __name__ == "__main__":
    main()
