import mysql.connector
from db_connection import connect_db, close_db

def fetch_financial_data(ticker):
    """Fetches financial data for a given stock ticker."""
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    query = """
    SELECT date, revenue, net_income, total_assets, total_liabilities, stock_price
    FROM fact_financials WHERE ticker = %s ORDER BY date DESC;
    """
    cursor.execute(query, (ticker,))
    results = cursor.fetchall()
    
    cursor.close()
    close_db(conn)
    return results

def main():
    """Retrieve and display financial data."""
    ticker = input("Enter stock ticker symbol: ")
    data = fetch_financial_data(ticker)
    
    if data:
        print("\n📊 Financial Data:")
        for row in data:
            print(row)
    else:
        print("❌ No data found for this ticker.")

if __name__ == "__main__":
    main()
