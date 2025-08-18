"""
Database configuration and connection management for SWT TMS Hub
"""
import sqlite3
import os
from pathlib import Path
import hashlib
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DB_DIR / "swt_tms.db"

# Ensure data directory exists
DB_DIR.mkdir(exist_ok=True)

def get_connection():
    """Get database connection with proper configuration"""
    try:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def init_database():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('super_user', 'ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting')),
            full_name TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_by INTEGER REFERENCES users(id),
            permissions TEXT
        )''')
        
        # Customers table
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_code TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            contact_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            credit_limit DECIMAL(10,2),
            payment_terms TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Shipments table
        cursor.execute('''CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            load_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER REFERENCES customers(id),
            origin_address TEXT,
            origin_city TEXT,
            origin_state TEXT,
            origin_zip TEXT,
            destination_address TEXT,
            destination_city TEXT,
            destination_state TEXT,
            destination_zip TEXT,
            pickup_date DATE,
            pickup_time TEXT,
            delivery_date DATE,
            delivery_time TEXT,
            status TEXT DEFAULT 'New' CHECK(status IN ('New', 'Assigned', 'Dispatched', 'In Transit', 'Delivered', 'Cancelled', 'On Hold')),
            weight DECIMAL(10,2),
            pieces INTEGER,
            commodity TEXT,
            equipment_type TEXT,
            rate DECIMAL(10,2),
            miles INTEGER,
            special_instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Carriers table
        cursor.execute('''CREATE TABLE IF NOT EXISTS carriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            carrier_code TEXT UNIQUE NOT NULL,
            carrier_name TEXT NOT NULL,
            carrier_type TEXT CHECK(carrier_type IN ('Company', 'Owner Operator', 'Partner Carrier')),
            dot_number TEXT,
            mc_number TEXT,
            insurance_exp DATE,
            contact_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Drivers table
        cursor.execute('''CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_code TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            carrier_id INTEGER REFERENCES carriers(id),
            cdl_number TEXT,
            cdl_state TEXT,
            cdl_expiry DATE,
            medical_cert_expiry DATE,
            phone TEXT,
            email TEXT,
            status TEXT DEFAULT 'Available' CHECK(status IN ('Available', 'On Duty', 'Off Duty', 'On Leave')),
            home_terminal TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Trucks table
        cursor.execute('''CREATE TABLE IF NOT EXISTS trucks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            truck_number TEXT UNIQUE NOT NULL,
            carrier_id INTEGER REFERENCES carriers(id),
            vin TEXT,
            make TEXT,
            model TEXT,
            year INTEGER,
            license_plate TEXT,
            status TEXT DEFAULT 'Available' CHECK(status IN ('Available', 'In Transit', 'Out of Service', 'Maintenance')),
            current_location TEXT,
            gps_latitude REAL,
            gps_longitude REAL,
            last_inspection DATE,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Dispatches table
        cursor.execute('''CREATE TABLE IF NOT EXISTS dispatches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispatch_number TEXT UNIQUE NOT NULL,
            shipment_id INTEGER REFERENCES shipments(id),
            driver_id INTEGER REFERENCES drivers(id),
            truck_id INTEGER REFERENCES trucks(id),
            carrier_id INTEGER REFERENCES carriers(id),
            dispatched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            pickup_arrival TIMESTAMP,
            pickup_departure TIMESTAMP,
            delivery_arrival TIMESTAMP,
            delivery_departure TIMESTAMP,
            carrier_rate DECIMAL(10,2),
            fuel_advance DECIMAL(10,2),
            detention_time INTEGER,
            detention_rate DECIMAL(10,2),
            lumper_fee DECIMAL(10,2),
            other_charges DECIMAL(10,2),
            notes TEXT,
            status TEXT DEFAULT 'Dispatched' CHECK(status IN ('Dispatched', 'En Route to Pickup', 'At Pickup', 'Loaded', 'In Transit', 'At Delivery', 'Delivered', 'Completed'))
        )''')
        
        # Invoices table
        cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER REFERENCES customers(id),
            shipment_id INTEGER REFERENCES shipments(id),
            invoice_date DATE,
            due_date DATE,
            amount DECIMAL(10,2),
            fuel_surcharge DECIMAL(10,2),
            accessorial_charges DECIMAL(10,2),
            total_amount DECIMAL(10,2),
            status TEXT DEFAULT 'Pending' CHECK(status IN ('Draft', 'Pending', 'Sent', 'Paid', 'Past Due', 'Cancelled')),
            paid_date DATE,
            payment_method TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # System settings table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_by INTEGER REFERENCES users(id)
        )''')
        
        # Create default super user (Brandon Smith)
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'Brandon'")
        if cursor.fetchone()[0] == 0:
            password_hash = hashlib.sha256('ceo123'.encode()).hexdigest()
            cursor.execute("""INSERT INTO users 
                (username, password_hash, role, full_name, email, phone, permissions) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                ('Brandon', password_hash, 'super_user', 'Brandon Smith', 
                 'brandon@swtrucking.com', '(951) 437-5474', 'ALL'))
            logger.info("Default super user created: Brandon")
        
        # Create performance indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_shipments_dates ON shipments(pickup_date, delivery_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_dispatches_status ON dispatches(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_customers_code ON customers(customer_code)')
        
        # Insert default system settings
        default_settings = [
            ('company_name', 'Smith & Williams Trucking LLC', 'Company legal name'),
            ('company_phone', '(951) 437-5474', 'Main company phone number'),
            ('company_email', 'Dispatch@smithwilliamstrucking.com', 'Main company email'),
            ('session_timeout', '60', 'Session timeout in minutes'),
            ('default_currency', 'USD', 'Default currency for transactions'),
            ('timezone', 'PST', 'Default timezone'),
            ('date_format', 'MM/DD/YYYY', 'Default date format')
        ]
        
        for key, value, desc in default_settings:
            cursor.execute("""INSERT OR IGNORE INTO system_settings 
                (setting_key, setting_value, description) VALUES (?, ?, ?)""",
                (key, value, desc))
        
        conn.commit()
        logger.info(f"Database initialized successfully at {DB_PATH}")
        
    except Exception as e:
        conn.rollback()
        logger.error(f"Database initialization error: {e}")
        raise
    finally:
        conn.close()

def backup_database(backup_name=None):
    """Create a backup of the database"""
    if not backup_name:
        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    backup_path = DB_DIR / f"{backup_name}.db"
    
    try:
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        logger.info(f"Database backup created: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        raise

if __name__ == "__main__":
    init_database()