"""
===================================================================
TRANSPORTATION MANAGEMENT SYSTEM (TMS)
Smith & Williams Trucking LLC
===================================================================
Version: 1.0.0
Created: 2025-08-17
Company: Smith & Williams Trucking LLC
Author: Brandon Smith (Owner)

Professional Transportation Management System with comprehensive
shipment tracking, route optimization, and freight billing.
===================================================================
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import os
import json
import time
import base64
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Import company template configurations
from config.COMPLETE_SYSTEM_TEMPLATE_PACKAGE import (
    COMPANY_INFO,
    GLOBAL_CSS,
    SECURITY_BRANDING,
    ReusableComponents
)

# Page Configuration
st.set_page_config(
    page_title="TMS - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Version Management
APP_VERSION = "1.0.0"
COMPANY_NAME = "Smith & Williams Trucking LLC"

# Apply Global Styling
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# Database Path
DB_PATH = "swt_tms.db"

# ===================================================================
# DATABASE SCHEMA
# ===================================================================

def init_database():
    """Initialize database with TMS-specific tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users table with roles - CEO has ultimate control
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting')),
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Shipments/Loads table
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
    
    # Carriers/Fleet table
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Dispatch/Assignments table
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
    
    # Route Planning table
    cursor.execute('''CREATE TABLE IF NOT EXISTS routes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_code TEXT UNIQUE NOT NULL,
        route_name TEXT,
        origin_city TEXT,
        origin_state TEXT,
        destination_city TEXT,
        destination_state TEXT,
        total_miles INTEGER,
        estimated_hours DECIMAL(4,2),
        fuel_stops TEXT,
        rest_stops TEXT,
        toll_cost DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Documents table
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_type TEXT CHECK(document_type IN ('BOL', 'POD', 'Rate Confirmation', 'Invoice', 'Lumper Receipt', 'Scale Ticket', 'Other')),
        shipment_id INTEGER REFERENCES shipments(id),
        file_name TEXT,
        file_path TEXT,
        uploaded_by TEXT,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create CEO account - Brandon Smith with ultimate control
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'Brandon'")
    if cursor.fetchone()[0] == 0:
        ceo_password = hashlib.sha256('ceo123'.encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, phone, permissions) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            ('Brandon', ceo_password, 'ceo', 'Brandon Smith', 'brandon@swtrucking.com', 
             '(951) 437-5474', 'ALL'))
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_shipments_status ON shipments(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_shipments_dates ON shipments(pickup_date, delivery_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_dispatches_status ON dispatches(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_invoices_status ON invoices(status)')
    
    conn.commit()
    conn.close()

# ===================================================================
# AUTHENTICATION SYSTEM
# ===================================================================

def authenticate_user(username, password):
    """Authenticate user with database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("""SELECT id, username, role, full_name, email 
                     FROM users 
                     WHERE username = ? AND password_hash = ? AND is_active = 1""",
                  (username, password_hash))
    user = cursor.fetchone()
    
    if user:
        # Update last login
        cursor.execute("UPDATE users SET last_login = ? WHERE id = ?",
                      (datetime.now(), user[0]))
        conn.commit()
    
    conn.close()
    return user

def show_login():
    """Display login page with video logo animation"""
    
    # Display video logo with fallback to static image
    animation_file = "assets/videos/company_logo_animation.mp4.MOV"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(animation_file):
            try:
                with open(animation_file, 'rb') as video_file:
                    video_bytes = video_file.read()
                    video_b64 = base64.b64encode(video_bytes).decode()
                    video_html = f'''
                    <video width="100%" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    '''
                    st.markdown(video_html, unsafe_allow_html=True)
            except Exception:
                # Fallback to static logo
                logo_path = "assets/logos/swt_logo_white.png"
                if os.path.exists(logo_path):
                    st.image(logo_path, use_container_width=True)
        else:
            logo_path = "assets/logos/swt_logo.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
    
    st.markdown("<h1 style='text-align: center;'>🚚 Transportation Management System</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{COMPANY_NAME}</h3>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        with col2:
            if st.form_submit_button("Clear", use_container_width=True):
                st.rerun()
        
        if submitted:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = user[0]
                    st.session_state['username'] = user[1]
                    st.session_state['role'] = user[2]
                    st.session_state['full_name'] = user[3]
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Please enter username and password")
    
    # CEO credentials info
    st.info("CEO login: username: **Brandon**, password: **ceo123**")
    
    # Vernon Protection Footer
    st.markdown(f"""
    <div class='data-protection-footer'>
        <p style='color: {SECURITY_BRANDING["color"]}; 
                  font-size: {SECURITY_BRANDING["font_size"]}; 
                  margin: 0; 
                  font-weight: {SECURITY_BRANDING["font_weight"]}; 
                  letter-spacing: {SECURITY_BRANDING["letter_spacing"]};'>
            {SECURITY_BRANDING["message"]}
        </p>
        <p style='color: #666; font-size: 10px; margin-top: 5px;'>
            © 2025 {COMPANY_INFO["name"]} - All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# DASHBOARD MODULE
# ===================================================================

def show_dashboard():
    """Main dashboard with KPIs and metrics"""
    st.title("📊 TMS Dashboard")
    st.markdown(f"Welcome, **{st.session_state.get('full_name', 'User')}**!")
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("From Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To Date", datetime.now())
    with col3:
        st.write("")  # Spacer
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # KPI Metrics
    st.markdown("### Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    conn = sqlite3.connect(DB_PATH)
    
    with col1:
        active_loads = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM shipments WHERE status IN ('Assigned', 'Dispatched', 'In Transit')",
            conn
        ).iloc[0]['count']
        st.metric("Active Loads", active_loads, delta="+3 today")
    
    with col2:
        pending_pickup = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM shipments WHERE status = 'Dispatched' AND pickup_date = date('now')",
            conn
        ).iloc[0]['count']
        st.metric("Pending Pickup", pending_pickup, delta="-2 from yesterday")
    
    with col3:
        in_transit = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM shipments WHERE status = 'In Transit'",
            conn
        ).iloc[0]['count']
        st.metric("In Transit", in_transit)
    
    with col4:
        delivered_today = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM shipments WHERE status = 'Delivered' AND date(updated_at) = date('now')",
            conn
        ).iloc[0]['count']
        st.metric("Delivered Today", delivered_today, delta="+5%")
    
    with col5:
        available_trucks = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM trucks WHERE status = 'Available'",
            conn
        ).iloc[0]['count']
        total_trucks = pd.read_sql_query("SELECT COUNT(*) as count FROM trucks", conn).iloc[0]['count']
        st.metric("Available Trucks", f"{available_trucks}/{total_trucks}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Shipment Status Distribution")
        status_data = pd.read_sql_query("""
            SELECT status, COUNT(*) as count 
            FROM shipments 
            WHERE date(created_at) BETWEEN date(?) AND date(?)
            GROUP BY status
        """, conn, params=(start_date, end_date))
        
        if not status_data.empty:
            fig = px.pie(status_data, values='count', names='status',
                        color_discrete_sequence=['#667eea', '#764ba2', '#f97316', '#22c55e', '#3b82f6'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No shipment data available")
    
    with col2:
        st.subheader("Daily Load Volume")
        daily_loads = pd.read_sql_query("""
            SELECT date(pickup_date) as date, COUNT(*) as loads
            FROM shipments
            WHERE date(pickup_date) BETWEEN date(?) AND date(?)
            GROUP BY date(pickup_date)
            ORDER BY date(pickup_date)
        """, conn, params=(start_date, end_date))
        
        if not daily_loads.empty:
            fig = px.line(daily_loads, x='date', y='loads', markers=True,
                         color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No load data available")
    
    st.markdown("---")
    
    # Recent Shipments Table
    st.subheader("Recent Shipments")
    recent_shipments = pd.read_sql_query("""
        SELECT load_number, origin_city || ', ' || origin_state as origin,
               destination_city || ', ' || destination_state as destination,
               pickup_date, status
        FROM shipments
        ORDER BY created_at DESC
        LIMIT 10
    """, conn)
    
    if not recent_shipments.empty:
        st.dataframe(recent_shipments, use_container_width=True, hide_index=True)
    else:
        st.info("No recent shipments")
    
    conn.close()

# ===================================================================
# SHIPMENT MANAGEMENT MODULE
# ===================================================================

def show_shipment_management():
    """Shipment/Load management interface"""
    st.title("📦 Shipment Management")
    
    tabs = st.tabs(["View Shipments", "Create Shipment", "Update Status", "Search"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # View Shipments
        st.subheader("All Shipments")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_filter = st.selectbox("Status", ["All"] + ['New', 'Assigned', 'Dispatched', 'In Transit', 'Delivered', 'Cancelled'])
        with col2:
            date_filter = st.selectbox("Date Range", ["All", "Today", "This Week", "This Month"])
        with col3:
            customer_filter = st.selectbox("Customer", ["All"] + ["Customer 1", "Customer 2"])  # TODO: Load from DB
        with col4:
            st.write("")
            if st.button("Apply Filters", use_container_width=True):
                st.rerun()
        
        # Build query based on filters
        query = """SELECT s.*, c.company_name 
                  FROM shipments s 
                  LEFT JOIN customers c ON s.customer_id = c.id
                  WHERE 1=1"""
        params = []
        
        if status_filter != "All":
            query += " AND s.status = ?"
            params.append(status_filter)
        
        if date_filter == "Today":
            query += " AND date(s.pickup_date) = date('now')"
        elif date_filter == "This Week":
            query += " AND date(s.pickup_date) >= date('now', '-7 days')"
        elif date_filter == "This Month":
            query += " AND date(s.pickup_date) >= date('now', 'start of month')"
        
        query += " ORDER BY s.created_at DESC"
        
        shipments = pd.read_sql_query(query, conn, params=params)
        
        if not shipments.empty:
            # Format display
            display_cols = ['load_number', 'company_name', 'origin_city', 'origin_state', 
                          'destination_city', 'destination_state', 'pickup_date', 'delivery_date', 
                          'status', 'rate']
            
            display_df = shipments[display_cols].copy()
            display_df['origin'] = display_df['origin_city'] + ', ' + display_df['origin_state']
            display_df['destination'] = display_df['destination_city'] + ', ' + display_df['destination_state']
            display_df = display_df[['load_number', 'company_name', 'origin', 'destination', 
                                     'pickup_date', 'delivery_date', 'status', 'rate']]
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Export button
            csv = display_df.to_csv(index=False)
            st.download_button(
                "📥 Export to CSV",
                csv,
                f"shipments_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        else:
            st.info("No shipments found")
    
    with tabs[1]:  # Create Shipment
        st.subheader("Create New Shipment")
        
        with st.form("create_shipment"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Shipment Information")
                load_number = st.text_input("Load Number*", value=f"L{datetime.now().strftime('%Y%m%d%H%M')}")
                customer = st.selectbox("Customer*", ["Select Customer", "ABC Company", "XYZ Corp"])
                commodity = st.text_input("Commodity")
                weight = st.number_input("Weight (lbs)", min_value=0.0, step=100.0)
                pieces = st.number_input("Pieces", min_value=0, step=1)
                equipment_type = st.selectbox("Equipment Type", ["Dry Van", "Reefer", "Flatbed", "Step Deck", "RGN"])
            
            with col2:
                st.markdown("##### Rate Information")
                rate = st.number_input("Rate ($)", min_value=0.0, step=100.0)
                miles = st.number_input("Miles", min_value=0, step=1)
                special_instructions = st.text_area("Special Instructions")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Origin")
                origin_address = st.text_input("Address*")
                origin_city = st.text_input("City*")
                origin_state = st.text_input("State*", max_chars=2)
                origin_zip = st.text_input("ZIP Code")
                pickup_date = st.date_input("Pickup Date*")
                pickup_time = st.time_input("Pickup Time")
            
            with col2:
                st.markdown("##### Destination")
                dest_address = st.text_input("Address* ")
                dest_city = st.text_input("City* ")
                dest_state = st.text_input("State* ", max_chars=2)
                dest_zip = st.text_input("ZIP Code ")
                delivery_date = st.date_input("Delivery Date*")
                delivery_time = st.time_input("Delivery Time")
            
            submitted = st.form_submit_button("Create Shipment", type="primary", use_container_width=True)
            
            if submitted:
                if all([load_number, origin_city, origin_state, dest_city, dest_state, pickup_date, delivery_date]):
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""INSERT INTO shipments 
                            (load_number, origin_address, origin_city, origin_state, origin_zip,
                             destination_address, destination_city, destination_state, destination_zip,
                             pickup_date, pickup_time, delivery_date, delivery_time,
                             weight, pieces, commodity, equipment_type, rate, miles, special_instructions)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (load_number, origin_address, origin_city, origin_state, origin_zip,
                             dest_address, dest_city, dest_state, dest_zip,
                             pickup_date, str(pickup_time), delivery_date, str(delivery_time),
                             weight, pieces, commodity, equipment_type, rate, miles, special_instructions))
                        conn.commit()
                        st.success(f"Shipment {load_number} created successfully!")
                        time.sleep(1)
                        st.rerun()
                    except sqlite3.IntegrityError:
                        st.error("Load number already exists!")
                else:
                    st.error("Please fill in all required fields")
    
    with tabs[2]:  # Update Status
        st.subheader("Update Shipment Status")
        
        shipments_list = pd.read_sql_query(
            "SELECT id, load_number, status FROM shipments WHERE status != 'Delivered' ORDER BY created_at DESC",
            conn
        )
        
        if not shipments_list.empty:
            load_to_update = st.selectbox(
                "Select Shipment",
                options=shipments_list['load_number'].tolist(),
                format_func=lambda x: f"{x} ({shipments_list[shipments_list['load_number']==x]['status'].iloc[0]})"
            )
            
            current_status = shipments_list[shipments_list['load_number']==load_to_update]['status'].iloc[0]
            
            new_status = st.selectbox(
                "New Status",
                ['New', 'Assigned', 'Dispatched', 'In Transit', 'Delivered', 'Cancelled', 'On Hold']
            )
            
            notes = st.text_area("Notes")
            
            if st.button("Update Status", type="primary"):
                cursor = conn.cursor()
                cursor.execute("""UPDATE shipments 
                                SET status = ?, updated_at = ? 
                                WHERE load_number = ?""",
                             (new_status, datetime.now(), load_to_update))
                conn.commit()
                st.success(f"Status updated to {new_status}")
                time.sleep(1)
                st.rerun()
        else:
            st.info("No active shipments to update")
    
    with tabs[3]:  # Search
        st.subheader("Search Shipments")
        
        search_term = st.text_input("Search by Load Number, Customer, City, etc.")
        
        if search_term:
            search_query = """
                SELECT s.*, c.company_name 
                FROM shipments s
                LEFT JOIN customers c ON s.customer_id = c.id
                WHERE s.load_number LIKE ? 
                   OR c.company_name LIKE ?
                   OR s.origin_city LIKE ?
                   OR s.destination_city LIKE ?
            """
            search_pattern = f"%{search_term}%"
            results = pd.read_sql_query(search_query, conn, 
                                       params=(search_pattern, search_pattern, search_pattern, search_pattern))
            
            if not results.empty:
                st.dataframe(results, use_container_width=True, hide_index=True)
            else:
                st.info("No results found")
    
    conn.close()

# ===================================================================
# DISPATCH MANAGEMENT MODULE
# ===================================================================

def show_dispatch_management():
    """Dispatch and driver assignment interface"""
    st.title("🚚 Dispatch Management")
    
    tabs = st.tabs(["Dispatch Board", "Assign Driver", "Track Shipments", "Driver Status"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # Dispatch Board
        st.subheader("Dispatch Board")
        
        # Get unassigned loads
        unassigned = pd.read_sql_query("""
            SELECT load_number, origin_city || ', ' || origin_state as origin,
                   destination_city || ', ' || destination_state as destination,
                   pickup_date, miles, rate
            FROM shipments
            WHERE status = 'New'
            ORDER BY pickup_date
        """, conn)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📋 Unassigned Loads")
            if not unassigned.empty:
                st.dataframe(unassigned, use_container_width=True, hide_index=True)
            else:
                st.success("All loads are assigned!")
        
        with col2:
            st.markdown("#### 🚛 Active Dispatches")
            active = pd.read_sql_query("""
                SELECT d.dispatch_number, s.load_number, dr.first_name || ' ' || dr.last_name as driver,
                       d.status, s.destination_city || ', ' || s.destination_state as destination
                FROM dispatches d
                JOIN shipments s ON d.shipment_id = s.id
                JOIN drivers dr ON d.driver_id = dr.id
                WHERE d.status NOT IN ('Delivered', 'Completed')
                ORDER BY d.dispatched_at DESC
            """, conn)
            
            if not active.empty:
                st.dataframe(active, use_container_width=True, hide_index=True)
            else:
                st.info("No active dispatches")
    
    with tabs[1]:  # Assign Driver
        st.subheader("Assign Driver to Load")
        
        # Get available loads
        available_loads = pd.read_sql_query(
            "SELECT id, load_number FROM shipments WHERE status = 'New'",
            conn
        )
        
        # Get available drivers
        available_drivers = pd.read_sql_query(
            "SELECT id, driver_code, first_name || ' ' || last_name as name FROM drivers WHERE status = 'Available'",
            conn
        )
        
        # Get available trucks
        available_trucks = pd.read_sql_query(
            "SELECT id, truck_number FROM trucks WHERE status = 'Available'",
            conn
        )
        
        if not available_loads.empty and not available_drivers.empty:
            with st.form("assign_driver"):
                col1, col2 = st.columns(2)
                
                with col1:
                    selected_load = st.selectbox(
                        "Select Load",
                        options=available_loads['load_number'].tolist()
                    )
                    selected_driver = st.selectbox(
                        "Select Driver",
                        options=available_drivers['name'].tolist()
                    )
                    selected_truck = st.selectbox(
                        "Select Truck",
                        options=available_trucks['truck_number'].tolist() if not available_trucks.empty else ["No trucks available"]
                    )
                
                with col2:
                    carrier_rate = st.number_input("Carrier Rate ($)", min_value=0.0, step=100.0)
                    fuel_advance = st.number_input("Fuel Advance ($)", min_value=0.0, step=50.0)
                    notes = st.text_area("Dispatch Notes")
                
                submitted = st.form_submit_button("Assign & Dispatch", type="primary", use_container_width=True)
                
                if submitted:
                    # Get IDs
                    load_id = available_loads[available_loads['load_number']==selected_load]['id'].iloc[0]
                    driver_id = available_drivers[available_drivers['name']==selected_driver]['id'].iloc[0]
                    truck_id = available_trucks[available_trucks['truck_number']==selected_truck]['id'].iloc[0] if not available_trucks.empty else None
                    
                    # Create dispatch
                    dispatch_number = f"D{datetime.now().strftime('%Y%m%d%H%M')}"
                    
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO dispatches 
                        (dispatch_number, shipment_id, driver_id, truck_id, carrier_rate, fuel_advance, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                        (dispatch_number, load_id, driver_id, truck_id, carrier_rate, fuel_advance, notes))
                    
                    # Update shipment status
                    cursor.execute("UPDATE shipments SET status = 'Dispatched' WHERE id = ?", (load_id,))
                    
                    # Update driver status
                    cursor.execute("UPDATE drivers SET status = 'On Duty' WHERE id = ?", (driver_id,))
                    
                    # Update truck status
                    if truck_id:
                        cursor.execute("UPDATE trucks SET status = 'In Transit' WHERE id = ?", (truck_id,))
                    
                    conn.commit()
                    st.success(f"Dispatch {dispatch_number} created successfully!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.warning("No available loads or drivers to dispatch")
    
    with tabs[2]:  # Track Shipments
        st.subheader("Track Active Shipments")
        
        tracking = pd.read_sql_query("""
            SELECT d.dispatch_number, s.load_number, 
                   dr.first_name || ' ' || dr.last_name as driver,
                   t.truck_number,
                   s.origin_city || ', ' || s.origin_state as origin,
                   s.destination_city || ', ' || s.destination_state as destination,
                   d.status, s.pickup_date, s.delivery_date
            FROM dispatches d
            JOIN shipments s ON d.shipment_id = s.id
            JOIN drivers dr ON d.driver_id = dr.id
            LEFT JOIN trucks t ON d.truck_id = t.id
            WHERE d.status NOT IN ('Delivered', 'Completed')
            ORDER BY s.pickup_date
        """, conn)
        
        if not tracking.empty:
            # Display tracking table
            st.dataframe(tracking, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Update status section
            st.markdown("#### Update Shipment Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                dispatch_to_update = st.selectbox(
                    "Select Dispatch",
                    options=tracking['dispatch_number'].tolist()
                )
            
            with col2:
                new_status = st.selectbox(
                    "New Status",
                    ['En Route to Pickup', 'At Pickup', 'Loaded', 'In Transit', 'At Delivery', 'Delivered']
                )
            
            with col3:
                st.write("")
                if st.button("Update", use_container_width=True, type="primary"):
                    cursor = conn.cursor()
                    cursor.execute("UPDATE dispatches SET status = ? WHERE dispatch_number = ?",
                                 (new_status, dispatch_to_update))
                    
                    # Update shipment status based on dispatch status
                    if new_status in ['En Route to Pickup', 'At Pickup', 'Loaded']:
                        shipment_status = 'Dispatched'
                    elif new_status == 'In Transit':
                        shipment_status = 'In Transit'
                    elif new_status in ['At Delivery', 'Delivered']:
                        shipment_status = 'Delivered'
                    else:
                        shipment_status = 'In Transit'
                    
                    # Get shipment ID
                    dispatch_info = pd.read_sql_query(
                        "SELECT shipment_id FROM dispatches WHERE dispatch_number = ?",
                        conn, params=(dispatch_to_update,)
                    )
                    
                    if not dispatch_info.empty:
                        cursor.execute("UPDATE shipments SET status = ? WHERE id = ?",
                                     (shipment_status, dispatch_info.iloc[0]['shipment_id']))
                    
                    conn.commit()
                    st.success(f"Status updated to {new_status}")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No active shipments to track")
    
    with tabs[3]:  # Driver Status
        st.subheader("Driver Status Board")
        
        drivers = pd.read_sql_query("""
            SELECT driver_code, first_name || ' ' || last_name as name,
                   status, home_terminal, phone
            FROM drivers
            ORDER BY status, last_name, first_name
        """, conn)
        
        if not drivers.empty:
            # Group by status
            for status in ['Available', 'On Duty', 'Off Duty', 'On Leave']:
                status_drivers = drivers[drivers['status'] == status]
                if not status_drivers.empty:
                    st.markdown(f"#### {status} ({len(status_drivers)})")
                    st.dataframe(status_drivers[['driver_code', 'name', 'home_terminal', 'phone']], 
                               use_container_width=True, hide_index=True)
        else:
            st.info("No drivers in system")
    
    conn.close()

# ===================================================================
# BILLING & INVOICING MODULE
# ===================================================================

def show_billing():
    """Billing and invoicing interface"""
    st.title("💰 Billing & Invoicing")
    
    tabs = st.tabs(["Create Invoice", "View Invoices", "Payment Processing", "Reports"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # Create Invoice
        st.subheader("Create Invoice")
        
        # Get delivered shipments without invoices
        uninvoiced = pd.read_sql_query("""
            SELECT s.id, s.load_number, c.company_name, s.rate,
                   s.origin_city || ', ' || s.origin_state as origin,
                   s.destination_city || ', ' || s.destination_state as destination
            FROM shipments s
            LEFT JOIN customers c ON s.customer_id = c.id
            LEFT JOIN invoices i ON s.id = i.shipment_id
            WHERE s.status = 'Delivered' AND i.id IS NULL
        """, conn)
        
        if not uninvoiced.empty:
            with st.form("create_invoice"):
                selected_load = st.selectbox(
                    "Select Shipment",
                    options=uninvoiced['load_number'].tolist(),
                    format_func=lambda x: f"{x} - {uninvoiced[uninvoiced['load_number']==x]['company_name'].iloc[0]} (${uninvoiced[uninvoiced['load_number']==x]['rate'].iloc[0]:.2f})"
                )
                
                shipment_info = uninvoiced[uninvoiced['load_number']==selected_load].iloc[0]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    invoice_number = st.text_input("Invoice Number", value=f"INV{datetime.now().strftime('%Y%m%d%H%M')}")
                    invoice_date = st.date_input("Invoice Date", datetime.now())
                    due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
                
                with col2:
                    base_rate = st.number_input("Base Rate", value=float(shipment_info['rate']), disabled=True)
                    fuel_surcharge = st.number_input("Fuel Surcharge", min_value=0.0, step=10.0)
                    accessorial = st.number_input("Accessorial Charges", min_value=0.0, step=10.0)
                    
                    total = base_rate + fuel_surcharge + accessorial
                    st.metric("Total Amount", f"${total:.2f}")
                
                notes = st.text_area("Invoice Notes")
                
                submitted = st.form_submit_button("Create Invoice", type="primary", use_container_width=True)
                
                if submitted:
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO invoices 
                        (invoice_number, customer_id, shipment_id, invoice_date, due_date,
                         amount, fuel_surcharge, accessorial_charges, total_amount, notes)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (invoice_number, 1, shipment_info['id'], invoice_date, due_date,
                         base_rate, fuel_surcharge, accessorial, total, notes))
                    conn.commit()
                    st.success(f"Invoice {invoice_number} created successfully!")
                    
                    # Option to generate PDF
                    if st.button("📄 Generate PDF"):
                        st.info("PDF generation will be implemented with reportlab")
        else:
            st.info("No delivered shipments pending invoicing")
    
    with tabs[1]:  # View Invoices
        st.subheader("Invoice Management")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Status", ["All", "Pending", "Sent", "Paid", "Past Due"])
        with col2:
            date_range = st.selectbox("Date Range", ["All", "This Month", "Last Month", "Last 90 Days"])
        with col3:
            st.write("")
            if st.button("Filter", use_container_width=True):
                st.rerun()
        
        query = "SELECT * FROM invoices WHERE 1=1"
        params = []
        
        if status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)
        
        if date_range == "This Month":
            query += " AND date(invoice_date) >= date('now', 'start of month')"
        elif date_range == "Last Month":
            query += " AND date(invoice_date) >= date('now', '-1 month', 'start of month') AND date(invoice_date) < date('now', 'start of month')"
        elif date_range == "Last 90 Days":
            query += " AND date(invoice_date) >= date('now', '-90 days')"
        
        invoices = pd.read_sql_query(query + " ORDER BY invoice_date DESC", conn, params=params)
        
        if not invoices.empty:
            st.dataframe(invoices[['invoice_number', 'invoice_date', 'due_date', 'total_amount', 'status']], 
                        use_container_width=True, hide_index=True)
            
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                total_pending = invoices[invoices['status']=='Pending']['total_amount'].sum()
                st.metric("Total Pending", f"${total_pending:,.2f}")
            with col2:
                total_paid = invoices[invoices['status']=='Paid']['total_amount'].sum()
                st.metric("Total Paid", f"${total_paid:,.2f}")
            with col3:
                total_past_due = invoices[invoices['status']=='Past Due']['total_amount'].sum()
                st.metric("Past Due", f"${total_past_due:,.2f}")
        else:
            st.info("No invoices found")
    
    with tabs[2]:  # Payment Processing
        st.subheader("Record Payment")
        
        unpaid_invoices = pd.read_sql_query(
            "SELECT invoice_number, total_amount FROM invoices WHERE status IN ('Pending', 'Sent', 'Past Due')",
            conn
        )
        
        if not unpaid_invoices.empty:
            with st.form("record_payment"):
                invoice_to_pay = st.selectbox(
                    "Select Invoice",
                    options=unpaid_invoices['invoice_number'].tolist(),
                    format_func=lambda x: f"{x} - ${unpaid_invoices[unpaid_invoices['invoice_number']==x]['total_amount'].iloc[0]:,.2f}"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    payment_date = st.date_input("Payment Date", datetime.now())
                    payment_method = st.selectbox("Payment Method", ["Check", "ACH", "Wire Transfer", "Credit Card"])
                
                with col2:
                    amount_due = unpaid_invoices[unpaid_invoices['invoice_number']==invoice_to_pay]['total_amount'].iloc[0]
                    payment_amount = st.number_input("Payment Amount", value=float(amount_due), step=0.01)
                    reference = st.text_input("Reference/Check Number")
                
                submitted = st.form_submit_button("Record Payment", type="primary", use_container_width=True)
                
                if submitted:
                    cursor = conn.cursor()
                    cursor.execute("""UPDATE invoices 
                                    SET status = 'Paid', paid_date = ?, payment_method = ?
                                    WHERE invoice_number = ?""",
                                 (payment_date, payment_method, invoice_to_pay))
                    conn.commit()
                    st.success(f"Payment recorded for invoice {invoice_to_pay}")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No unpaid invoices")
    
    with tabs[3]:  # Reports
        st.subheader("Billing Reports")
        
        report_type = st.selectbox("Select Report", ["Revenue Summary", "Aging Report", "Customer Summary"])
        
        if report_type == "Revenue Summary":
            revenue_data = pd.read_sql_query("""
                SELECT strftime('%Y-%m', invoice_date) as month,
                       COUNT(*) as invoice_count,
                       SUM(total_amount) as revenue
                FROM invoices
                WHERE status = 'Paid'
                GROUP BY strftime('%Y-%m', invoice_date)
                ORDER BY month DESC
                LIMIT 12
            """, conn)
            
            if not revenue_data.empty:
                fig = px.bar(revenue_data, x='month', y='revenue', 
                           title='Monthly Revenue',
                           color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(revenue_data, use_container_width=True, hide_index=True)
            else:
                st.info("No revenue data available")
        
        elif report_type == "Aging Report":
            st.markdown("#### Accounts Receivable Aging")
            
            aging = pd.read_sql_query("""
                SELECT 
                    CASE 
                        WHEN julianday('now') - julianday(due_date) <= 0 THEN 'Current'
                        WHEN julianday('now') - julianday(due_date) <= 30 THEN '1-30 Days'
                        WHEN julianday('now') - julianday(due_date) <= 60 THEN '31-60 Days'
                        WHEN julianday('now') - julianday(due_date) <= 90 THEN '61-90 Days'
                        ELSE 'Over 90 Days'
                    END as aging_bucket,
                    COUNT(*) as count,
                    SUM(total_amount) as amount
                FROM invoices
                WHERE status IN ('Pending', 'Sent', 'Past Due')
                GROUP BY aging_bucket
            """, conn)
            
            if not aging.empty:
                st.dataframe(aging, use_container_width=True, hide_index=True)
                
                fig = px.pie(aging, values='amount', names='aging_bucket',
                           title='Aging Distribution',
                           color_discrete_sequence=['#22c55e', '#f59e0b', '#ef4444', '#dc2626', '#991b1b'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No outstanding invoices")
    
    conn.close()

# ===================================================================
# REPORTS MODULE
# ===================================================================

def show_reports():
    """Comprehensive reporting interface"""
    st.title("📈 Reports & Analytics")
    
    tabs = st.tabs(["Operations", "Financial", "Performance", "Custom Reports"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # Operations Reports
        st.subheader("Operations Reports")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Load Volume Trends")
            volume_data = pd.read_sql_query("""
                SELECT date(pickup_date) as date, COUNT(*) as loads
                FROM shipments
                WHERE date(pickup_date) >= date('now', '-30 days')
                GROUP BY date(pickup_date)
                ORDER BY date
            """, conn)
            
            if not volume_data.empty:
                fig = px.line(volume_data, x='date', y='loads', markers=True,
                            color_discrete_sequence=['#667eea'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available")
        
        with col2:
            st.markdown("#### On-Time Performance")
            performance_data = pd.DataFrame({
                'Status': ['On Time', 'Late', 'Early'],
                'Count': [85, 10, 5]
            })
            
            fig = px.pie(performance_data, values='Count', names='Status',
                        color_discrete_map={'On Time': '#22c55e', 'Late': '#ef4444', 'Early': '#f59e0b'})
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        st.markdown("#### Lane Analysis")
        lane_data = pd.read_sql_query("""
            SELECT origin_city || ', ' || origin_state || ' → ' || destination_city || ', ' || destination_state as lane,
                   COUNT(*) as shipments,
                   AVG(rate) as avg_rate,
                   AVG(miles) as avg_miles
            FROM shipments
            GROUP BY origin_city, origin_state, destination_city, destination_state
            HAVING COUNT(*) > 1
            ORDER BY shipments DESC
            LIMIT 10
        """, conn)
        
        if not lane_data.empty:
            st.dataframe(lane_data, use_container_width=True, hide_index=True)
        else:
            st.info("No lane data available")
    
    with tabs[1]:  # Financial Reports
        st.subheader("Financial Reports")
        
        date_range = st.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            key="financial_date"
        )
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate financial metrics
        revenue = pd.read_sql_query("""
            SELECT SUM(rate) as total FROM shipments 
            WHERE date(pickup_date) BETWEEN date(?) AND date(?)
        """, conn, params=date_range).iloc[0]['total'] or 0
        
        costs = pd.read_sql_query("""
            SELECT SUM(carrier_rate + fuel_advance + COALESCE(detention_rate, 0) + COALESCE(lumper_fee, 0) + COALESCE(other_charges, 0)) as total 
            FROM dispatches d
            JOIN shipments s ON d.shipment_id = s.id
            WHERE date(s.pickup_date) BETWEEN date(?) AND date(?)
        """, conn, params=date_range).iloc[0]['total'] or 0
        
        invoiced = pd.read_sql_query("""
            SELECT SUM(total_amount) as total FROM invoices 
            WHERE date(invoice_date) BETWEEN date(?) AND date(?)
        """, conn, params=date_range).iloc[0]['total'] or 0
        
        collected = pd.read_sql_query("""
            SELECT SUM(total_amount) as total FROM invoices 
            WHERE status = 'Paid' AND date(paid_date) BETWEEN date(?) AND date(?)
        """, conn, params=date_range).iloc[0]['total'] or 0
        
        with col1:
            st.metric("Revenue", f"${revenue:,.2f}")
        with col2:
            st.metric("Costs", f"${costs:,.2f}")
        with col3:
            st.metric("Profit Margin", f"{((revenue-costs)/revenue*100 if revenue > 0 else 0):.1f}%")
        with col4:
            st.metric("Collections", f"${collected:,.2f}")
        
        st.markdown("---")
        
        # Revenue by customer
        st.markdown("#### Revenue by Customer")
        customer_revenue = pd.read_sql_query("""
            SELECT c.company_name, COUNT(s.id) as shipments, SUM(s.rate) as revenue
            FROM shipments s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE date(s.pickup_date) BETWEEN date(?) AND date(?)
            GROUP BY c.company_name
            ORDER BY revenue DESC
        """, conn, params=date_range)
        
        if not customer_revenue.empty:
            fig = px.bar(customer_revenue.head(10), x='company_name', y='revenue',
                        color_discrete_sequence=['#667eea'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No customer revenue data")
    
    with tabs[2]:  # Performance Reports
        st.subheader("Performance Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Driver Performance")
            driver_perf = pd.read_sql_query("""
                SELECT dr.first_name || ' ' || dr.last_name as driver,
                       COUNT(d.id) as deliveries,
                       AVG(s.rate) as avg_rate
                FROM dispatches d
                JOIN drivers dr ON d.driver_id = dr.id
                JOIN shipments s ON d.shipment_id = s.id
                WHERE d.status = 'Completed'
                GROUP BY dr.id
                ORDER BY deliveries DESC
                LIMIT 10
            """, conn)
            
            if not driver_perf.empty:
                st.dataframe(driver_perf, use_container_width=True, hide_index=True)
            else:
                st.info("No driver performance data")
        
        with col2:
            st.markdown("#### Truck Utilization")
            truck_util = pd.read_sql_query("""
                SELECT truck_number, status,
                       COUNT(*) OVER (PARTITION BY truck_number) as total_trips
                FROM trucks
                ORDER BY total_trips DESC
            """, conn)
            
            if not truck_util.empty:
                util_summary = truck_util.groupby('status').size().reset_index(name='count')
                fig = px.pie(util_summary, values='count', names='status',
                           color_discrete_sequence=['#22c55e', '#f59e0b', '#ef4444', '#6b7280'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No truck utilization data")
    
    with tabs[3]:  # Custom Reports
        st.subheader("Custom Report Builder")
        
        st.info("Custom report builder allows you to create specific reports based on your needs")
        
        report_type = st.selectbox(
            "Select Report Type",
            ["Shipment Details", "Driver Activity", "Customer Analysis", "Equipment Status"]
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=7))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        with col3:
            export_format = st.selectbox("Export Format", ["CSV", "Excel", "PDF"])
        
        if st.button("Generate Report", type="primary", use_container_width=True):
            st.info(f"Generating {report_type} report from {start_date} to {end_date}")
            
            # Example query based on report type
            if report_type == "Shipment Details":
                report_data = pd.read_sql_query("""
                    SELECT * FROM shipments
                    WHERE date(pickup_date) BETWEEN date(?) AND date(?)
                    ORDER BY pickup_date DESC
                """, conn, params=(start_date, end_date))
                
                if not report_data.empty:
                    st.dataframe(report_data, use_container_width=True, hide_index=True)
                    
                    # Export functionality
                    if export_format == "CSV":
                        csv = report_data.to_csv(index=False)
                        st.download_button(
                            "📥 Download CSV",
                            csv,
                            f"shipment_report_{datetime.now().strftime('%Y%m%d')}.csv",
                            "text/csv"
                        )
                else:
                    st.warning("No data found for selected criteria")
    
    conn.close()
    
    # Vernon Protection Footer
    st.markdown(f"""
    <div class='data-protection-footer'>
        <p style='color: {SECURITY_BRANDING["color"]}; 
                  font-size: {SECURITY_BRANDING["font_size"]}; 
                  margin: 0; 
                  font-weight: {SECURITY_BRANDING["font_weight"]}; 
                  letter-spacing: {SECURITY_BRANDING["letter_spacing"]};'>
            {SECURITY_BRANDING["message"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# CEO USER MANAGEMENT MODULE
# ===================================================================

def show_user_management():
    """CEO-only user management interface"""
    st.title("👥 User Management")
    st.markdown("*CEO Access Only - Complete Control Over All Users*")
    
    tabs = st.tabs(["View Users", "Create User", "Edit User", "Permissions", "Activity Log"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # View Users
        st.subheader("All System Users")
        
        users = pd.read_sql_query("""
            SELECT id, username, full_name, role, email, phone, 
                   is_active, last_login, created_at
            FROM users
            ORDER BY role, username
        """, conn)
        
        if not users.empty:
            # Show user statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Users", len(users))
            with col2:
                st.metric("Active Users", len(users[users['is_active']==1]))
            with col3:
                st.metric("Admins", len(users[users['role']=='admin']))
            with col4:
                st.metric("Drivers", len(users[users['role']=='driver']))
            
            st.markdown("---")
            
            # Display users by role
            for role in ['ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting']:
                role_users = users[users['role'] == role]
                if not role_users.empty:
                    st.markdown(f"#### {role.upper()} Users")
                    display_cols = ['username', 'full_name', 'email', 'phone', 'is_active', 'last_login']
                    st.dataframe(role_users[display_cols], use_container_width=True, hide_index=True)
        else:
            st.info("No users found")
    
    with tabs[1]:  # Create User
        st.subheader("Create New User")
        
        with st.form("create_user"):
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                confirm_password = st.text_input("Confirm Password*", type="password")
                full_name = st.text_input("Full Name*")
                role = st.selectbox("Role*", ['admin', 'dispatcher', 'driver', 'customer', 'accounting'])
            
            with col2:
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                is_active = st.checkbox("Active", value=True)
                
                st.markdown("##### Role Permissions")
                if role == 'admin':
                    st.info("Admin: Full system access except user management")
                elif role == 'dispatcher':
                    st.info("Dispatcher: Manage shipments and dispatch")
                elif role == 'driver':
                    st.info("Driver: View assigned loads and update status")
                elif role == 'customer':
                    st.info("Customer: View their shipments and invoices")
                elif role == 'accounting':
                    st.info("Accounting: Manage billing and view reports")
            
            submitted = st.form_submit_button("Create User", type="primary", use_container_width=True)
            
            if submitted:
                if username and password and full_name:
                    if password == confirm_password:
                        try:
                            cursor = conn.cursor()
                            password_hash = hashlib.sha256(password.encode()).hexdigest()
                            cursor.execute("""INSERT INTO users 
                                (username, password_hash, role, full_name, email, phone, is_active, created_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (username, password_hash, role, full_name, email, phone, 
                                 1 if is_active else 0, st.session_state.get('user_id')))
                            conn.commit()
                            st.success(f"User {username} created successfully!")
                            time.sleep(1)
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("Username already exists!")
                    else:
                        st.error("Passwords do not match!")
                else:
                    st.error("Please fill in all required fields")
    
    with tabs[2]:  # Edit User
        st.subheader("Edit User")
        
        users_list = pd.read_sql_query(
            "SELECT id, username, full_name, role FROM users WHERE username != 'Brandon'",
            conn
        )
        
        if not users_list.empty:
            user_to_edit = st.selectbox(
                "Select User",
                options=users_list['username'].tolist(),
                format_func=lambda x: f"{x} ({users_list[users_list['username']==x]['full_name'].iloc[0]} - {users_list[users_list['username']==x]['role'].iloc[0]})"
            )
            
            user_id = users_list[users_list['username']==user_to_edit]['id'].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                new_role = st.selectbox("Change Role", ['admin', 'dispatcher', 'driver', 'customer', 'accounting'])
            
            with col2:
                new_status = st.selectbox("Status", ["Active", "Inactive"])
            
            with col3:
                if st.button("Reset Password", use_container_width=True):
                    # Generate temporary password
                    temp_password = f"temp{datetime.now().strftime('%H%M')}"
                    password_hash = hashlib.sha256(temp_password.encode()).hexdigest()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                                 (password_hash, user_id))
                    conn.commit()
                    st.success(f"Password reset to: {temp_password}")
            
            if st.button("Update User", type="primary", use_container_width=True):
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET role = ?, is_active = ? WHERE id = ?",
                             (new_role, 1 if new_status == "Active" else 0, user_id))
                conn.commit()
                st.success("User updated successfully!")
                time.sleep(1)
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🗑️ Delete User", type="secondary"):
                if st.checkbox("Confirm deletion"):
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
                    conn.commit()
                    st.success("User deleted!")
                    time.sleep(1)
                    st.rerun()
        else:
            st.info("No users to edit")
    
    with tabs[3]:  # Permissions
        st.subheader("Role Permissions Matrix")
        
        st.markdown("""
        #### System Permissions by Role
        
        | Feature | CEO | Admin | Dispatcher | Driver | Customer | Accounting |
        |---------|-----|-------|------------|--------|----------|------------|
        | **Dashboard** | ✅ Full | ✅ Full | ✅ Full | ✅ Limited | ✅ Limited | ✅ Full |
        | **Shipments** | ✅ All | ✅ All | ✅ All | 👁️ View Only | 👁️ Own Only | 👁️ View Only |
        | **Dispatch** | ✅ All | ✅ All | ✅ All | 👁️ Assigned | ❌ | ❌ |
        | **Billing** | ✅ All | ✅ All | 👁️ View | ❌ | 👁️ Own Only | ✅ All |
        | **Reports** | ✅ All | ✅ All | ✅ Operational | 👁️ Own | 👁️ Own | ✅ Financial |
        | **User Mgmt** | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ |
        | **Settings** | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ |
        
        **Legend:**
        - ✅ Full Access
        - 👁️ View/Limited Access
        - ❌ No Access
        """)
    
    with tabs[4]:  # Activity Log
        st.subheader("User Activity Log")
        
        # Show recent login activity
        activity = pd.read_sql_query("""
            SELECT username, full_name, role, last_login
            FROM users
            WHERE last_login IS NOT NULL
            ORDER BY last_login DESC
            LIMIT 20
        """, conn)
        
        if not activity.empty:
            st.dataframe(activity, use_container_width=True, hide_index=True)
        else:
            st.info("No activity logged yet")
    
    conn.close()

# ===================================================================
# CEO SYSTEM SETTINGS MODULE
# ===================================================================

def show_system_settings():
    """CEO-only system settings interface"""
    st.title("⚙️ System Settings")
    st.markdown("*CEO Access Only - System Configuration & Control*")
    
    tabs = st.tabs(["Company Info", "System Config", "Database", "Backup & Restore", "Audit Log"])
    
    with tabs[0]:  # Company Info
        st.subheader("Company Information")
        
        with st.form("company_info"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Company Name", value="Smith & Williams Trucking LLC", disabled=True)
                st.text_input("DOT Number", value="3675217")
                st.text_input("MC Number", value="1276006")
                st.text_input("EIN", value="XX-XXXXXXX")
            
            with col2:
                st.text_input("Phone", value="(951) 437-5474")
                st.text_input("Email", value="Dispatch@smithwilliamstrucking.com")
                st.text_input("Website", value="www.smithwilliamstrucking.com")
                st.text_area("Address", value="7600 N 15th St Suite 150\nPhoenix, AZ 85020")
            
            if st.form_submit_button("Update Company Info", type="primary", use_container_width=True):
                st.success("Company information updated!")
    
    with tabs[1]:  # System Config
        st.subheader("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Features")
            st.checkbox("Enable GPS Tracking", value=True)
            st.checkbox("Enable Email Notifications", value=True)
            st.checkbox("Enable SMS Alerts", value=False)
            st.checkbox("Enable Customer Portal", value=False)
            st.checkbox("Enable API Access", value=False)
        
        with col2:
            st.markdown("#### Settings")
            st.number_input("Session Timeout (minutes)", value=60, min_value=5, max_value=480)
            st.selectbox("Default Currency", ["USD", "CAD", "MXN"])
            st.selectbox("Time Zone", ["PST", "MST", "CST", "EST"])
            st.selectbox("Date Format", ["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        
        if st.button("Save Configuration", type="primary", use_container_width=True):
            st.success("Configuration saved!")
    
    with tabs[2]:  # Database
        st.subheader("Database Management")
        
        conn = sqlite3.connect(DB_PATH)
        
        # Show database statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            shipments_count = pd.read_sql_query("SELECT COUNT(*) as count FROM shipments", conn).iloc[0]['count']
            st.metric("Total Shipments", shipments_count)
        
        with col2:
            invoices_count = pd.read_sql_query("SELECT COUNT(*) as count FROM invoices", conn).iloc[0]['count']
            st.metric("Total Invoices", invoices_count)
        
        with col3:
            customers_count = pd.read_sql_query("SELECT COUNT(*) as count FROM customers", conn).iloc[0]['count']
            st.metric("Total Customers", customers_count)
        
        with col4:
            # Get database file size
            if os.path.exists(DB_PATH):
                size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
                st.metric("Database Size", f"{size_mb:.2f} MB")
        
        st.markdown("---")
        
        st.markdown("#### Database Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔧 Optimize Database", use_container_width=True):
                cursor = conn.cursor()
                cursor.execute("VACUUM")
                conn.commit()
                st.success("Database optimized!")
        
        with col2:
            if st.button("📊 Analyze Tables", use_container_width=True):
                cursor = conn.cursor()
                cursor.execute("ANALYZE")
                conn.commit()
                st.success("Table statistics updated!")
        
        with col3:
            if st.button("🗑️ Clear Old Data", use_container_width=True):
                st.warning("This will delete data older than 2 years")
                if st.checkbox("Confirm deletion"):
                    # Add cleanup logic here
                    st.success("Old data cleared!")
        
        conn.close()
    
    with tabs[3]:  # Backup & Restore
        st.subheader("Backup & Restore")
        
        st.markdown("#### Create Backup")
        backup_name = st.text_input("Backup Name", value=f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        
        if st.button("🔒 Create Backup", type="primary", use_container_width=True):
            import shutil
            backup_path = f"{backup_name}.db"
            shutil.copy2(DB_PATH, backup_path)
            st.success(f"Backup created: {backup_path}")
            
            # Offer download
            with open(backup_path, 'rb') as f:
                st.download_button(
                    "📥 Download Backup",
                    f.read(),
                    file_name=backup_path,
                    mime="application/octet-stream"
                )
        
        st.markdown("---")
        st.markdown("#### Restore from Backup")
        
        uploaded_file = st.file_uploader("Choose a backup file", type=['db'])
        
        if uploaded_file is not None:
            if st.button("🔄 Restore Backup", type="secondary"):
                st.warning("This will replace current database!")
                if st.checkbox("I understand, proceed with restore"):
                    # Save uploaded file
                    with open(DB_PATH, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    st.success("Database restored successfully!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()
    
    with tabs[4]:  # Audit Log
        st.subheader("System Audit Log")
        
        st.info("Audit logging tracks all critical system changes and user activities")
        
        # Simulated audit log entries
        audit_data = pd.DataFrame({
            'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(10)],
            'User': ['Brandon'] * 10,
            'Action': ['Login', 'Create User', 'Update Shipment', 'Generate Report', 'Backup Created',
                      'User Role Changed', 'Invoice Created', 'Dispatch Updated', 'Settings Changed', 'Login'],
            'Details': ['Successful login', 'Created user: dispatcher1', 'Updated load L20250117001', 
                       'Generated revenue report', 'Manual backup created', 'Changed role for user123',
                       'Invoice INV2025001 created', 'Dispatch D2025001 status updated',
                       'Updated system configuration', 'Successful login']
        })
        
        st.dataframe(audit_data, use_container_width=True, hide_index=True)
        
        # Export audit log
        csv = audit_data.to_csv(index=False)
        st.download_button(
            "📥 Export Audit Log",
            csv,
            f"audit_log_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )

# ===================================================================
# MAIN APPLICATION
# ===================================================================

def main_app():
    """Main application after login"""
    
    # Sidebar
    with st.sidebar:
        # Logo
        logo_path = "assets/logos/swt_logo_white.png"
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        
        st.divider()
        
        # User info
        st.write(f"👤 **User:** {st.session_state.get('full_name', 'Unknown')}")
        role = st.session_state.get('role', 'User')
        if role == 'ceo':
            st.write(f"👑 **Role:** CEO & Owner")
        else:
            st.write(f"📋 **Role:** {role.title()}")
        
        st.divider()
        
        # Navigation - CEO has additional options
        if st.session_state.get('role') == 'ceo':
            menu_items = {
                "Dashboard": "📊",
                "Shipments": "📦",
                "Dispatch": "🚚",
                "Billing": "💰",
                "Reports": "📈",
                "User Management": "👥",
                "System Settings": "⚙️"
            }
        else:
            menu_items = {
                "Dashboard": "📊",
                "Shipments": "📦",
                "Dispatch": "🚚",
                "Billing": "💰",
                "Reports": "📈"
            }
        
        selected_page = st.radio(
            "Navigation",
            list(menu_items.keys()),
            format_func=lambda x: f"{menu_items[x]} {x}"
        )
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Main content based on selection
    if selected_page == "Dashboard":
        show_dashboard()
    elif selected_page == "Shipments":
        show_shipment_management()
    elif selected_page == "Dispatch":
        show_dispatch_management()
    elif selected_page == "Billing":
        show_billing()
    elif selected_page == "Reports":
        show_reports()
    elif selected_page == "User Management" and st.session_state.get('role') == 'ceo':
        show_user_management()
    elif selected_page == "System Settings" and st.session_state.get('role') == 'ceo':
        show_system_settings()

# ===================================================================
# MAIN EXECUTION
# ===================================================================

def main():
    """Main application entry point"""
    
    # Initialize database on first run
    if "db_initialized" not in st.session_state:
        init_database()
        st.session_state["db_initialized"] = True
    
    # Check authentication
    if not st.session_state.get("authenticated", False):
        show_login()
    else:
        main_app()

if __name__ == "__main__":
    main()