import mysql.connector

def connect_db():
    """Establishes a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",  # Replace with your MySQL username
            password="Vani@333",  # Replace with your MySQL password
            database="financial_reporting"
        )
        if conn.is_connected():
            print("✅ Connected to the database successfully!")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None
    

def close_db(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("🔌 Database connection closed.")

if __name__ == "__main__":
    conn = connect_db()
    close_db(conn)
