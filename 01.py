from sqlalchemy import create_engine
import pandas as pd

# ✅ MySQL Database URL (Replace with your actual credentials)
db_url = "mysql+pymysql://root:Vani@333@127.0.0.1/financial_reporting"
engine = create_engine(db_url)

# ✅ Define SQL Query BEFORE Calling get_data()
total_revenue_query = """
    SELECT c.company, SUM(f.revenue) AS total_revenue
    FROM financial_data f
    JOIN company_dim c ON f.company_id = c.company_id
    GROUP BY c.company
    ORDER BY total_revenue DESC;
"""

# ✅ Function to Fetch Data
def get_data(query):
    return pd.read_sql(query, engine)

# ✅ Fetch Data
data_revenue = get_data(total_revenue_query)

# ✅ Print Output
print(data_revenue)
