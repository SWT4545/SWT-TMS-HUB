"""
Database initialization script for Smith & Williams Trucking TMS
"""
import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "swt_tms.db"

def init_database():
    """Initialize database with tables and default data"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1
    )''')
    
    # Create default super user if not exists
    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        password_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("admin", password_hash, "super_user", "System Administrator", "admin@swtrucking.com", 1))
        
        # Add Brandon as super user
        brandon_hash = hashlib.sha256("ceo123".encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("brandon", brandon_hash, "super_user", "Brandon Smith", "brandon@swtrucking.com", 1))
        
        # Add demo users
        demo_hash = hashlib.sha256("demo123".encode()).hexdigest()
        
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("executive", demo_hash, "executive", "John Executive", "exec@swtrucking.com", 1))
        
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("driver", demo_hash, "driver", "Bob Driver", "driver@swtrucking.com", 1))
        
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("dataentry", demo_hash, "data_feeder", "Alice Data", "data@swtrucking.com", 1))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")
    print("\nDefault Users Created:")
    print("------------------------")
    print("Username: admin | Password: admin123 | Role: Super User")
    print("Username: brandon | Password: ceo123 | Role: Super User")
    print("Username: executive | Password: demo123 | Role: Executive")
    print("Username: driver | Password: demo123 | Role: Driver")
    print("Username: dataentry | Password: demo123 | Role: Data Feeder")

if __name__ == "__main__":
    init_database()