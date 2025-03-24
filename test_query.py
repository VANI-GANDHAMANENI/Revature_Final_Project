import pymysql
from sqlalchemy import create_engine, text

# Database Configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Vani%40333",  # '@' is URL-encoded as '%40'
    "database": "financial_data"
}

# Create the database connection URL
DB_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

# Create an engine
engine = create_engine(DB_URI)

# Test Query
test_query = "SHOW TABLES;"  # Check if database connection works

try:
    with engine.connect() as connection:
        result = connection.execute(text(test_query))
        rows = result.fetchall()
        print("Database Tables:")
        for row in rows:
            print(row)
except Exception as e:
    print("Error executing test query:", e)
