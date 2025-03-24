# import mysql.connector
# from db_connection import connect_db, close_db

# def fetch_financial_data(ticker):
#     """Fetches financial data for a given stock ticker."""
#     conn = connect_db()
#     if not conn:
#         return
    
#     cursor = conn.cursor(dictionary=True)
#     query = """
#     SELECT date, revenue, net_income, total_assets, total_liabilities, stock_price
#     FROM fact_financials WHERE ticker = %s ORDER BY date DESC;
#     """
#     cursor.execute(query, (ticker,))
#     results = cursor.fetchall()
    
#     cursor.close()
#     close_db(conn)
#     return results

# def main():
#     """Retrieve and display financial data."""
#     ticker = input("Enter stock ticker symbol: ")
#     data = fetch_financial_data(ticker)
    
#     if data:
#         print("\n📊 Financial Data:")
#         for row in data:
#             print(row)
#     else:
#         print("❌ No data found for this ticker.")

# if __name__ == "__main__":
#     main()
import mysql.connector
import pandas as pd
from db_connection import connect_db, close_db

def insert_financial_data(ticker, data):
    """Inserts financial data into the database."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    query = """
    INSERT INTO fact_financials (ticker, date, revenue, net_income, total_assets, total_liabilities, stock_price)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    for index, row in data.iterrows():
        try:
            values = (
                ticker,
                row['Unnamed: 0'],  # Date column (renaming recommended before inserting)
                row.get('Free Cash Flow', 0),  
                row.get('Net Income From Continuing Operations', 0),  
                row.get('Total Assets', 0),  
                row.get('Total Liabilities', 0),  
                row.get('Operating Cash Flow', 0)  
            )
            print("Inserting values:", values)  # Debugging
            cursor.execute(query, values)
        except Exception as e:
            print(f"❌ Error inserting row {index}: {e}")
    
    conn.commit()
    print("✅ Data inserted successfully!")
    cursor.close()
    close_db(conn)

def main():
    """Loads financial data from CSV and inserts it into the database."""
    ticker = input("Enter stock ticker symbol: ").strip().upper()
    file_path = f"data/{ticker}_cashflow.csv"  # Adjust based on data source
    
    try:
        df = pd.read_csv(file_path)
        df.rename(columns={"Unnamed: 0": "Date"}, inplace=True)  # Rename for consistency
        insert_financial_data(ticker, df)
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

if __name__ == "__main__":
    main()