"""
Enhanced Database Module for Smith & Williams Trucking TMS
Includes all fields for intelligent payment reconciliation, GPS tracking, and API integrations
"""
import sqlite3
import os
from datetime import datetime
import hashlib
from pathlib import Path

DB_PATH = "swt_tms.db"

def init_enhanced_database():
    """Initialize enhanced database with all required tables and fields"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enhanced Users table with more fields
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        driver_license TEXT,
        cdl_expiry DATE,
        medical_cert_expiry DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        motive_driver_id TEXT,
        vector_user_id TEXT
    )''')
    
    # Enhanced Loads table with all financial and tracking fields
    cursor.execute('''CREATE TABLE IF NOT EXISTS loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id TEXT UNIQUE NOT NULL,
        customer TEXT NOT NULL,
        carrier TEXT NOT NULL,
        pickup_date DATE NOT NULL,
        delivery_date DATE,
        pickup_address TEXT NOT NULL,
        pickup_city TEXT,
        pickup_state TEXT,
        pickup_zip TEXT,
        pickup_lat REAL,
        pickup_lng REAL,
        delivery_address TEXT NOT NULL,
        delivery_city TEXT,
        delivery_state TEXT,
        delivery_zip TEXT,
        delivery_lat REAL,
        delivery_lng REAL,
        distance_miles REAL,
        gross_amount REAL NOT NULL,
        net_amount REAL NOT NULL,
        payment_method TEXT NOT NULL, -- 'Direct Pay' or 'Factored'
        factoring_fee_percent REAL,
        gross_rate_per_mile REAL,
        net_rate_per_mile REAL,
        driver_id INTEGER,
        truck_id INTEGER,
        trailer_id INTEGER,
        status TEXT DEFAULT 'pending',
        pickup_arrival_time TIMESTAMP,
        pickup_departure_time TIMESTAMP,
        delivery_arrival_time TIMESTAMP,
        delivery_departure_time TIMESTAMP,
        bol_number TEXT,
        bol_signed BOOLEAN DEFAULT 0,
        bol_document_url TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP,
        created_by INTEGER,
        motive_trip_id TEXT,
        vector_load_id TEXT,
        FOREIGN KEY (driver_id) REFERENCES users(id),
        FOREIGN KEY (created_by) REFERENCES users(id)
    )''')
    
    # Payments table for reconciliation
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_amount REAL NOT NULL,
        payment_date DATE NOT NULL,
        paying_entity TEXT NOT NULL,
        payment_type TEXT, -- 'Weekly', 'Daily', 'Quick Pay'
        reference_number TEXT,
        bank_account TEXT,
        reconciled BOOLEAN DEFAULT 0,
        reconciled_date TIMESTAMP,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by INTEGER,
        FOREIGN KEY (created_by) REFERENCES users(id)
    )''')
    
    # Payment-Load Reconciliation junction table
    cursor.execute('''CREATE TABLE IF NOT EXISTS payment_load_reconciliation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_id INTEGER NOT NULL,
        load_id INTEGER NOT NULL,
        reconciled_amount REAL NOT NULL,
        reconciled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reconciled_by INTEGER,
        FOREIGN KEY (payment_id) REFERENCES payments(id),
        FOREIGN KEY (load_id) REFERENCES loads(id),
        FOREIGN KEY (reconciled_by) REFERENCES users(id)
    )''')
    
    # Equipment/Trucks table
    cursor.execute('''CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_number TEXT UNIQUE NOT NULL,
        equipment_type TEXT NOT NULL, -- 'Truck' or 'Trailer'
        make TEXT,
        model TEXT,
        year INTEGER,
        vin TEXT,
        license_plate TEXT,
        state_registered TEXT,
        insurance_expiry DATE,
        registration_expiry DATE,
        last_inspection DATE,
        mileage INTEGER,
        status TEXT DEFAULT 'active',
        motive_vehicle_id TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Geofences for automated check-ins
    cursor.execute('''CREATE TABLE IF NOT EXISTS geofences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_name TEXT NOT NULL,
        address TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL,
        radius_meters INTEGER DEFAULT 500,
        location_type TEXT, -- 'pickup', 'delivery', 'yard', 'fuel'
        auto_checkin BOOLEAN DEFAULT 1,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Chat History for AI Conversations
    cursor.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        session_id TEXT NOT NULL,
        role TEXT NOT NULL, -- 'user' or 'assistant'
        message TEXT NOT NULL,
        view_type TEXT, -- 'data_feeder', 'driver', 'executive'
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Delays and Issues tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS delays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id INTEGER NOT NULL,
        delay_type TEXT NOT NULL,
        delay_reason TEXT NOT NULL,
        delay_duration_minutes INTEGER,
        reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reported_by INTEGER,
        resolved BOOLEAN DEFAULT 0,
        resolution_notes TEXT,
        FOREIGN KEY (load_id) REFERENCES loads(id),
        FOREIGN KEY (reported_by) REFERENCES users(id)
    )''')
    
    # System Settings for API configurations
    cursor.execute('''CREATE TABLE IF NOT EXISTS system_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_key TEXT UNIQUE NOT NULL,
        setting_value TEXT,
        setting_type TEXT, -- 'api_key', 'config', 'preference'
        encrypted BOOLEAN DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_by INTEGER,
        FOREIGN KEY (updated_by) REFERENCES users(id)
    )''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_status ON loads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_dates ON loads(pickup_date, delivery_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_carrier ON loads(carrier)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_date ON payments(payment_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_payments_entity ON payments(paying_entity)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_history(session_id)')
    
    # Check if brandon user exists, if not create it
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'brandon'")
    if cursor.fetchone()[0] == 0:
        brandon_hash = hashlib.sha256("ceo123".encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, phone, is_active) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            ("brandon", brandon_hash, "super_user", "Brandon Smith", "brandon@swtrucking.com", "(951) 437-5474", 1))
    
    conn.commit()
    conn.close()
    return True

def get_db_connection():
    """Get database connection with proper settings"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    """Execute a query and return results"""
    conn = get_db_connection()
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    if query.strip().upper().startswith('SELECT'):
        results = cursor.fetchall()
        conn.close()
        return results
    else:
        conn.commit()
        lastrowid = cursor.lastrowid
        conn.close()
        return lastrowid

def get_carrier_payment_schedule(carrier_name):
    """Get payment schedule for a specific carrier"""
    schedules = {
        "CanAmex": {
            "type": "weekly",
            "cycle": "Sunday-Saturday",
            "payment_day": "following_week",
            "fee_percent": 12.0,
            "method": "Direct Pay"
        },
        "Factoring Company": {
            "type": "daily",
            "cycle": "next-day",
            "payment_day": "next_business_day",
            "fee_percent": 3.0,
            "method": "Factored"
        }
    }
    return schedules.get(carrier_name, None)

def calculate_payment_amounts(gross_amount, payment_method):
    """Calculate net amount based on payment method"""
    if payment_method == "Direct Pay":
        fee_percent = 12.0
    elif payment_method == "Factored":
        fee_percent = 3.0
    else:
        fee_percent = 0.0
    
    fee_amount = gross_amount * (fee_percent / 100)
    net_amount = gross_amount - fee_amount
    
    return {
        "gross_amount": gross_amount,
        "fee_percent": fee_percent,
        "fee_amount": fee_amount,
        "net_amount": net_amount
    }

def get_loads_for_reconciliation(paying_entity, payment_date, amount):
    """Get potential loads for payment reconciliation"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get carrier payment schedule
    schedule = get_carrier_payment_schedule(paying_entity)
    
    if schedule:
        if schedule["type"] == "weekly":
            # For weekly payments, get loads from the previous week
            query = """
                SELECT * FROM loads 
                WHERE carrier = ? 
                AND delivery_date BETWEEN date(?, '-7 days') AND ?
                AND load_id NOT IN (
                    SELECT l.load_id FROM loads l
                    JOIN payment_load_reconciliation plr ON l.id = plr.load_id
                )
                ORDER BY delivery_date
            """
            cursor.execute(query, (paying_entity, payment_date, payment_date))
        else:
            # For daily payments, get loads from previous day
            query = """
                SELECT * FROM loads 
                WHERE carrier = ? 
                AND delivery_date = date(?, '-1 day')
                AND load_id NOT IN (
                    SELECT l.load_id FROM loads l
                    JOIN payment_load_reconciliation plr ON l.id = plr.load_id
                )
                ORDER BY delivery_date
            """
            cursor.execute(query, (paying_entity, payment_date))
    else:
        # Generic search for any unreconciled loads
        query = """
            SELECT * FROM loads 
            WHERE (carrier = ? OR customer = ?)
            AND delivery_date <= ?
            AND load_id NOT IN (
                SELECT l.load_id FROM loads l
                JOIN payment_load_reconciliation plr ON l.id = plr.load_id
            )
            ORDER BY delivery_date DESC
            LIMIT 20
        """
        cursor.execute(query, (paying_entity, paying_entity, payment_date))
    
    results = cursor.fetchall()
    conn.close()
    return results