import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Define database configuration
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Vani@333",  # Original password
    "database": "financial_reporting"
}

# URL-encode the password
encoded_password = quote_plus(DB_CONFIG["password"])

# Correct DB_URI with encoded password
DB_URI = f"mysql+pymysql://{DB_CONFIG['user']}:{encoded_password}@{DB_CONFIG['host']}/{DB_CONFIG['database']}"

# Create the engine
engine = create_engine(DB_URI, echo=True)

# Test the connection
try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")
