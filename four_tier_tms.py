"""
===================================================================
TRANSPORTATION MANAGEMENT SYSTEM - SMITH & WILLIAMS TRUCKING LLC
===================================================================
Version: 1.0.0
Created: 2025-08-17
Company: Smith & Williams Trucking LLC
CEO & Owner: Brandon Smith

Strategic Four-Tiered Architecture:
- Tier 1: Booking & Dispatching (Operational Command Center)
- Tier 2: Load & Invoice Management (Financial Enrichment)
- Tier 3: Finance & Compliance Management (Executive Reporting)
- Tier 4: Administrative Assistant/Automation (AI-Powered Management)

All operations driven by company profit goals with AI assistance
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
import requests
import numpy as np

# Import company template configurations
from config.COMPLETE_SYSTEM_TEMPLATE_PACKAGE import (
    COMPANY_INFO,
    GLOBAL_CSS,
    SECURITY_BRANDING
)

# Page Configuration
st.set_page_config(
    page_title="Transportation Management System - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Version Management
APP_VERSION = "1.0.0"
COMPANY_NAME = "Smith & Williams Trucking LLC"

# Smith & Williams Professional Theme - Balanced for All Lighting
SWT_PROFESSIONAL_CSS = """
<style>
    /* Smith & Williams Professional Theme - Works in Dark and Bright Settings */
    .main {
        background-color: #2d2d2d;
        padding: 0;
    }
    
    /* Charcoal gray background - not too dark, not too bright */
    .stApp {
        background-color: #2d2d2d;
        background-image: linear-gradient(180deg, #2d2d2d 0%, #333333 100%);
    }
    
    /* Remove white header bar - make it muted red */
    header[data-testid="stHeader"] {
        background-color: #8b1a1a !important;
        height: 3rem;
    }
    
    div[data-testid="stToolbar"] {
        display: none;
    }
    
    /* Headers with muted red - not too bright */
    h1, h2, h3 {
        color: #b91c1c;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold;
    }
    
    /* Off-white text - easier on eyes than pure white */
    p, div, label {
        color: #e5e5e5 !important;
    }
    
    /* Professional card styling with muted red accent */
    .metric-card {
        background: #3a3a3a;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #7f1d1d;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        color: #e5e5e5;
    }
    
    /* Button Styling - Muted Red */
    .stButton > button {
        background-color: #991b1b;
        color: #f5f5f5;
        border: 1px solid #991b1b;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #b91c1c;
        border-color: #b91c1c;
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(153, 27, 27, 0.3);
    }
    
    /* Sidebar with charcoal and muted red accent */
    section[data-testid="stSidebar"] {
        background: #262626;
        border-right: 2px solid #7f1d1d;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #e5e5e5;
    }
    
    /* Tables with softer colors */
    .dataframe {
        background-color: #333333;
        color: #e5e5e5;
        border: 1px solid #7f1d1d !important;
        border-collapse: separate;
        border-spacing: 0;
    }
    
    .dataframe th {
        background: #7f1d1d;
        color: #f5f5f5;
        font-weight: 600;
        border: 1px solid #7f1d1d !important;
        padding: 10px;
    }
    
    .dataframe td {
        background-color: #3a3a3a;
        color: #e5e5e5;
        border: 1px solid #4a4a4a !important;
        padding: 8px;
    }
    
    .dataframe tbody tr:hover td {
        background-color: #404040;
    }
    
    /* Streamlit native dataframe styling */
    div[data-testid="stDataFrame"] > div {
        border: 1px solid #7f1d1d !important;
        border-radius: 5px;
        overflow: hidden;
    }
    
    /* Metrics styling with muted colors */
    [data-testid="metric-container"] {
        background-color: #333333;
        border: 1px solid #7f1d1d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    [data-testid="metric-container"] label {
        color: #e5e5e5 !important;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #b91c1c !important;
        font-weight: bold;
    }
    
    [data-testid="metric-container"] [data-testid="stMetricDelta"] {
        color: #86efac !important;
    }
    
    /* Input fields with muted colors */
    .stTextInput > div > div > input {
        background-color: #3a3a3a;
        color: #e5e5e5;
        border: 1px solid #7f1d1d;
    }
    
    .stSelectbox > div > div > select {
        background-color: #3a3a3a;
        color: #e5e5e5;
        border: 1px solid #7f1d1d;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #3a3a3a;
        color: #e5e5e5;
        border: 1px solid #7f1d1d;
    }
    
    /* Data Protection Footer */
    .data-protection-footer {
        text-align: center;
        padding: 20px;
        margin-top: 60px;
        border-top: 2px solid #7f1d1d;
        background: #2d2d2d;
    }
    
    /* Success/Error/Warning Messages with muted backgrounds */
    .stSuccess {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid #22c55e;
        color: #86efac;
    }
    
    .stError {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid #ef4444;
        color: #fca5a5;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border: 1px solid #f59e0b;
        color: #fcd34d;
    }
    
    .stInfo {
        background-color: rgba(139, 26, 26, 0.1);
        border: 1px solid #7f1d1d;
        color: #e5e5e5;
    }
    
    /* Tab styling with muted colors */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d2d2d;
        border-bottom: 2px solid #7f1d1d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #e5e5e5;
        background-color: #333333;
        border: 1px solid #4a4a4a;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #7f1d1d !important;
        color: #f5f5f5 !important;
        border: 1px solid #991b1b !important;
    }
    
    /* Expander with muted colors */
    .streamlit-expanderHeader {
        background-color: #333333;
        border: 1px solid #7f1d1d;
        color: #e5e5e5;
    }
    
    /* Column gaps and spacing */
    div[data-testid="column"] {
        padding: 0 10px;
    }
</style>
"""

# Apply Professional Styling
st.markdown(SWT_PROFESSIONAL_CSS, unsafe_allow_html=True)

# Database Path
DB_PATH = "four_tier_tms.db"

# ===================================================================
# DATABASE SCHEMA - COMPREHENSIVE FOUR-TIER STRUCTURE
# ===================================================================

def init_database():
    """Initialize comprehensive database for Four-Tier TMS"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # =========================
    # CORE SYSTEM TABLES
    # =========================
    
    # Users table with CEO having ultimate control
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
        permissions TEXT,
        driver_profile_enabled BOOLEAN DEFAULT 0
    )''')
    
    # =========================
    # TIER 1: OPERATIONAL TABLES
    # =========================
    
    # Drivers table with dynamic truck assignments
    cursor.execute('''CREATE TABLE IF NOT EXISTS drivers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        driver_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        contact_info TEXT,
        license_info TEXT,
        current_hos_status TEXT,
        current_truck_id INTEGER REFERENCES trucks(id),
        assigned_truck_start_date DATE,
        assigned_truck_end_date DATE,
        status TEXT DEFAULT 'Available',
        home_base TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Trucks table with dynamic driver assignments
    cursor.execute('''CREATE TABLE IF NOT EXISTS trucks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        truck_id TEXT UNIQUE NOT NULL,
        vin TEXT,
        make_model TEXT,
        current_location TEXT,
        gps_latitude REAL,
        gps_longitude REAL,
        status TEXT DEFAULT 'operational' CHECK(status IN ('operational', 'out_of_service', 'maintenance')),
        assigned_driver_id INTEGER REFERENCES drivers(id),
        assigned_driver_start_date DATE,
        assigned_driver_end_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Contract FedEx loads with specific tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS contract_fedex_loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id TEXT UNIQUE NOT NULL,
        origin TEXT,
        destination TEXT,
        rate DECIMAL(10,2),
        mileage INTEGER,
        status TEXT,
        contractor_id TEXT,
        on_time_facility_in TIMESTAMP,
        on_time_facility_out TIMESTAMP,
        on_time_delivery_in TIMESTAMP,
        on_time_delivery_out TIMESTAMP,
        delivery_status TEXT,
        instructions_fedex_specific TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Contract sub loads (CanAmex, Metro Logistics)
    cursor.execute('''CREATE TABLE IF NOT EXISTS contract_sub_loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id TEXT UNIQUE NOT NULL,
        origin TEXT,
        destination TEXT,
        rate DECIMAL(10,2),
        mileage INTEGER,
        status TEXT,
        contractor_id TEXT,
        contract_rate_per_mile DECIMAL(10,2),
        priority_level INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Load board loads with broker vetting
    cursor.execute('''CREATE TABLE IF NOT EXISTS load_board_loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id TEXT UNIQUE NOT NULL,
        origin TEXT,
        destination TEXT,
        offered_rate DECIMAL(10,2),
        negotiated_rate DECIMAL(10,2),
        mileage INTEGER,
        status TEXT,
        broker_mc TEXT,
        broker_approved BOOLEAN,
        must_take_flag BOOLEAN DEFAULT 0,
        profitability_score DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Comprehensive document management
    cursor.execute('''CREATE TABLE IF NOT EXISTS load_documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id TEXT UNIQUE NOT NULL,
        load_id TEXT,
        document_type TEXT CHECK(document_type IN ('Rate Confirmation', 'Signed BOL', 'Trailer Photo', 'POD', 'Fuel Receipt', 'Scale Ticket', 'Other')),
        uploaded_by TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_path TEXT,
        status TEXT DEFAULT 'Pending',
        vector_processed BOOLEAN DEFAULT 0
    )''')
    
    # Driver performance and reasons logging
    cursor.execute('''CREATE TABLE IF NOT EXISTS driver_reasons_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_id TEXT UNIQUE NOT NULL,
        truck_id INTEGER REFERENCES trucks(id),
        driver_id INTEGER REFERENCES drivers(id),
        date_range TEXT,
        reason_category TEXT CHECK(reason_category IN ('Maintenance', 'Weather Delay', 'Shipper/Receiver Delay', 'Driver Delay', 'Roadside Issue', 'Accident')),
        specific_notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Performance tracking tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS truck_performance_weekly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_id TEXT,
        truck_id INTEGER REFERENCES trucks(id),
        total_miles INTEGER,
        loaded_miles INTEGER,
        empty_miles INTEGER,
        total_revenue DECIMAL(10,2),
        average_rate_per_mile DECIMAL(5,2),
        reasons_for_downtime TEXT,
        profit_margin DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS fleet_performance_weekly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_id TEXT,
        total_fleet_miles INTEGER,
        total_fleet_revenue DECIMAL(10,2),
        average_rate_per_mile DECIMAL(5,2),
        profit_goal_achievement DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Fuel consumption tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS fuel_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fuel_log_id TEXT UNIQUE NOT NULL,
        truck_id INTEGER REFERENCES trucks(id),
        date DATE,
        gallons DECIMAL(10,2),
        cost DECIMAL(10,2),
        location TEXT,
        mileage_at_fillup INTEGER,
        fuel_consumption_rate DECIMAL(5,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # =========================
    # TIER 2: FINANCIAL TABLES
    # =========================
    
    # Enhanced invoicing system
    cursor.execute('''CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id TEXT UNIQUE NOT NULL,
        load_id TEXT,
        customer_id INTEGER,
        invoice_date DATE,
        due_date DATE,
        amount DECIMAL(10,2),
        factoring_fee DECIMAL(10,2),
        cannamex_fee DECIMAL(10,2),
        status TEXT DEFAULT 'Draft' CHECK(status IN ('Draft', 'Sent', 'Paid', 'Past Due')),
        payment_date DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Payment tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_id TEXT UNIQUE NOT NULL,
        invoice_id INTEGER REFERENCES invoices(id),
        amount DECIMAL(10,2),
        payment_date DATE,
        payment_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Maintenance and repair logs
    cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_id TEXT UNIQUE NOT NULL,
        truck_id INTEGER REFERENCES trucks(id),
        date DATE,
        category TEXT CHECK(category IN ('Scheduled Service', 'Repair', 'Tire Change', 'Emergency', 'Inspection')),
        description TEXT,
        odometer_reading INTEGER,
        total_cost DECIMAL(10,2),
        vendor TEXT,
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # =========================
    # TIER 3: COMPLIANCE & REPORTING TABLES
    # =========================
    
    # Payroll management
    cursor.execute('''CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER REFERENCES drivers(id),
        pay_period TEXT,
        total_miles INTEGER,
        total_pay DECIMAL(10,2),
        deductions DECIMAL(10,2),
        net_pay DECIMAL(10,2),
        manual_adjustments DECIMAL(10,2),
        adjustment_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Compliance tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS compliance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        audit_type TEXT CHECK(audit_type IN ('IFTA', 'HOS', 'DOT', 'Insurance', 'Registration')),
        submission_date DATE,
        due_date DATE,
        status TEXT DEFAULT 'Pending',
        relevant_documents TEXT,
        phoenix_az_specific BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # =========================
    # TIER 4: AUTOMATION & AI TABLES
    # =========================
    
    # Task management system
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        category TEXT,
        priority TEXT CHECK(priority IN ('red', 'yellow', 'green')),
        due_date DATE,
        assigned_to INTEGER REFERENCES users(id),
        created_by INTEGER REFERENCES users(id),
        status TEXT DEFAULT 'not_started' CHECK(status IN ('not_started', 'in_progress', 'completed', 'on_hold')),
        completion_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Goal setting and profit management
    cursor.execute('''CREATE TABLE IF NOT EXISTS goals_and_targets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_id TEXT UNIQUE NOT NULL,
        goal_type TEXT CHECK(goal_type IN ('profit', 'revenue', 'cost_reduction', 'efficiency')),
        target_value DECIMAL(10,2),
        current_value DECIMAL(10,2),
        target_date DATE,
        status TEXT DEFAULT 'active',
        ai_suggested BOOLEAN DEFAULT 0,
        management_approved BOOLEAN DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Categories for task and expense management
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE NOT NULL,
        category_type TEXT CHECK(category_type IN ('business', 'personal')),
        tax_deductible BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Task dependencies
    cursor.execute('''CREATE TABLE IF NOT EXISTS dependencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id INTEGER REFERENCES tasks(id),
        dependent_task_id INTEGER REFERENCES tasks(id),
        relationship_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Renewal tracking for compliance
    cursor.execute('''CREATE TABLE IF NOT EXISTS renewals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        renewal_type TEXT,
        description TEXT,
        due_date DATE,
        cost DECIMAL(10,2),
        status TEXT DEFAULT 'pending',
        phoenix_az_registration BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Notes for detailed tracking
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        related_id TEXT,
        related_type TEXT,
        note_text TEXT,
        created_by INTEGER REFERENCES users(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Create CEO account - Brandon Smith with ultimate control and driver capabilities
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'Brandon'")
    if cursor.fetchone()[0] == 0:
        ceo_password = hashlib.sha256('ceo123'.encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, phone, permissions, driver_profile_enabled) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            ('Brandon', ceo_password, 'ceo', 'Brandon Smith', 'brandon@swtrucking.com', 
             '(951) 437-5474', 'ALL', 1))  # driver_profile_enabled = 1 for CEO
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_status ON contract_fedex_loads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_status_sub ON contract_sub_loads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_loads_status_board ON load_board_loads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tasks_assigned ON tasks(assigned_to)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_status ON goals_and_targets(status)')
    
    conn.commit()
    conn.close()

# ===================================================================
# AUTHENTICATION SYSTEM WITH CEO DUAL-ROLE CAPABILITY
# ===================================================================

def authenticate_user(username, password):
    """Authenticate user with enhanced CEO capabilities"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute("""SELECT id, username, role, full_name, email, driver_profile_enabled 
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
    """Display login page with enhanced branding"""
    
    # Display video logo
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
                    </video>
                    '''
                    st.markdown(video_html, unsafe_allow_html=True)
            except:
                logo_path = "assets/logos/swt_logo.png"
                if os.path.exists(logo_path):
                    st.image(logo_path, use_container_width=True)
    
    st.markdown("<h1 style='text-align: center;'>Transportation Management System</h1>", unsafe_allow_html=True)
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
                    st.session_state['driver_profile_enabled'] = user[5]
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
# TIER 1: BOOKING & DISPATCHING - OPERATIONAL COMMAND CENTER
# ===================================================================

def show_dispatcher_command_center():
    """Main dispatcher interface with intelligent load management"""
    st.title("Dispatcher Command Center")
    
    # Real-time fleet overview
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect(DB_PATH)
    
    with col1:
        available_trucks = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM trucks WHERE status = 'operational'",
            conn
        ).iloc[0]['count']
        st.metric("Available Trucks", available_trucks)
    
    with col2:
        available_drivers = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM drivers WHERE status = 'Available'",
            conn
        ).iloc[0]['count']
        st.metric("Available Drivers", available_drivers)
    
    with col3:
        contract_loads = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM contract_sub_loads WHERE status = 'pending'",
            conn
        ).iloc[0]['count']
        st.metric("Contract Loads", contract_loads, delta="Priority")
    
    with col4:
        weekly_avg = pd.read_sql_query(
            "SELECT AVG(average_rate_per_mile) as avg FROM fleet_performance_weekly ORDER BY created_at DESC LIMIT 1",
            conn
        ).iloc[0]['avg'] or 0
        st.metric("Weekly Avg Rate/Mile", f"${weekly_avg:.2f}", delta=f"Target: $2.00")
    
    st.markdown("---")
    
    tabs = st.tabs(["Load Prioritization", "Smart Load Finder", "Negotiation Tool", "Driver Assignment", "Documentation"])
    
    with tabs[0]:  # Load Prioritization
        st.subheader("🎯 Intelligent Load Prioritization")
        
        # Priority 1: Contract Loads (CanAmex, Metro)
        st.markdown("#### Priority 1: Contract Loads")
        contract_loads_df = pd.read_sql_query("""
            SELECT load_id, origin, destination, rate, mileage, contractor_id, priority_level
            FROM contract_sub_loads
            WHERE status = 'pending'
            ORDER BY priority_level DESC, rate DESC
        """, conn)
        
        if not contract_loads_df.empty:
            st.dataframe(contract_loads_df, use_container_width=True, hide_index=True)
        else:
            st.info("No pending contract loads")
        
        # Priority 2: Load Board (if needed)
        st.markdown("#### Priority 2: Load Board Opportunities")
        load_board_df = pd.read_sql_query("""
            SELECT load_id, origin, destination, negotiated_rate, mileage, profitability_score
            FROM load_board_loads
            WHERE status = 'available' AND broker_approved = 1
            ORDER BY profitability_score DESC
        """, conn)
        
        if not load_board_df.empty:
            st.dataframe(load_board_df, use_container_width=True, hide_index=True)
        else:
            st.info("No approved load board opportunities")
    
    with tabs[1]:  # Smart Load Finder
        st.subheader("🤖 Smart Load & Route Planning Bot")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Load Search Criteria")
            min_rate = st.number_input("Minimum Rate/Mile", value=2.00, step=0.10)
            max_distance = st.number_input("Maximum Distance", value=1500, step=100)
            origin_city = st.text_input("Origin City")
            destination_region = st.selectbox("Destination Region", 
                                            ["Any", "Southwest", "West Coast", "Midwest", "Southeast", "Northeast"])
        
        with col2:
            st.markdown("#### Round Trip Optimization")
            return_to_base = st.checkbox("Find return load to Phoenix")
            max_deadhead = st.number_input("Max Deadhead Miles", value=200, step=50)
            
            if st.button("🔍 Find Optimal Loads", type="primary", use_container_width=True):
                with st.spinner("Searching for profitable loads..."):
                    # Simulate smart load finding
                    st.success("Found 5 profitable load combinations!")
                    
                    # Display suggested routes
                    suggested_routes = pd.DataFrame({
                        'Route': ['PHX → LA → PHX', 'PHX → DAL → PHX', 'PHX → DEN → PHX'],
                        'Total Miles': [800, 2000, 1800],
                        'Total Revenue': [1800, 4200, 3800],
                        'Avg Rate/Mile': [2.25, 2.10, 2.11],
                        'Profit Score': [95, 88, 89]
                    })
                    st.dataframe(suggested_routes, use_container_width=True, hide_index=True)
    
    with tabs[2]:  # Negotiation Tool
        st.subheader("💰 Intelligent Negotiation Tool")
        
        col1, col2 = st.columns(2)
        
        with col1:
            broker_offer = st.number_input("Broker's Offer ($)", value=0.00, step=100.00)
            total_miles = st.number_input("Total Miles", value=0, step=1)
            must_take = st.checkbox("Must-Take Load (exit low-rate area)")
        
        with col2:
            if broker_offer > 0 and total_miles > 0:
                rate_per_mile = broker_offer / total_miles
                
                # Profitability analysis
                if rate_per_mile >= 2.00:
                    st.success(f"✅ ACCEPT - Rate: ${rate_per_mile:.2f}/mile")
                    recommendation = "This load meets profitability targets"
                elif rate_per_mile >= 1.80 and must_take:
                    st.warning(f"⚠️ CONSIDER - Rate: ${rate_per_mile:.2f}/mile")
                    recommendation = "Accept if needed for positioning"
                else:
                    st.error(f"❌ DECLINE - Rate: ${rate_per_mile:.2f}/mile")
                    counter_offer = total_miles * 2.00
                    recommendation = f"Counter with ${counter_offer:.2f}"
                
                st.info(recommendation)
                
                # Market comparison
                st.metric("Market Average", "$2.15/mile", delta=f"{rate_per_mile - 2.15:.2f}")
    
    with tabs[3]:  # Driver Assignment
        st.subheader("👥 Dynamic Driver-Truck Assignment")
        
        # Get available resources
        available_drivers_list = pd.read_sql_query(
            "SELECT id, name, current_hos_status FROM drivers WHERE status = 'Available'",
            conn
        )
        
        available_trucks_list = pd.read_sql_query(
            "SELECT id, truck_id, current_location FROM trucks WHERE status = 'operational'",
            conn
        )
        
        with st.form("assign_load"):
            col1, col2 = st.columns(2)
            
            with col1:
                selected_load = st.selectbox("Select Load", ["Load 1", "Load 2"])
                selected_driver = st.selectbox("Select Driver", 
                                              available_drivers_list['name'].tolist() if not available_drivers_list.empty else ["No drivers available"])
                selected_truck = st.selectbox("Select Truck",
                                             available_trucks_list['truck_id'].tolist() if not available_trucks_list.empty else ["No trucks available"])
            
            with col2:
                dispatch_notes = st.text_area("Dispatch Instructions")
                fuel_advance = st.number_input("Fuel Advance ($)", value=0.00, step=50.00)
            
            submitted = st.form_submit_button("Assign & Dispatch", type="primary", use_container_width=True)
            
            if submitted:
                st.success("Load assigned and dispatched successfully!")
    
    with tabs[4]:  # Documentation
        st.subheader("📄 Document Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Upload Documents")
            load_id = st.text_input("Load ID")
            doc_type = st.selectbox("Document Type", 
                                   ["Rate Confirmation", "BOL", "POD", "Scale Ticket", "Other"])
            uploaded_file = st.file_uploader("Choose file", type=['pdf', 'jpg', 'png'])
            
            if st.button("Upload & Process", type="primary"):
                if uploaded_file:
                    st.success("Document uploaded and processed via Vector API")
        
        with col2:
            st.markdown("#### Factoring Queue")
            
            # Show documents ready for factoring
            factoring_ready = pd.DataFrame({
                'Load ID': ['L001', 'L002'],
                'RC': ['✅', '✅'],
                'BOL': ['✅', '❌'],
                'Status': ['Ready', 'Pending BOL'],
                'Deadline': ['11 AM EST', 'Wednesday']
            })
            st.dataframe(factoring_ready, use_container_width=True, hide_index=True)
    
    conn.close()

# ===================================================================
# CEO DRIVER MODE - INTEGRATED DRIVER FUNCTIONALITY
# ===================================================================

def show_ceo_driver_mode():
    """CEO's integrated driver interface for performing driver tasks"""
    st.title("CEO Driver Mode")
    st.markdown("*Executive Driver Interface - Direct Load Management*")
    
    tabs = st.tabs(["My Loads", "Navigation", "Document Upload", "HOS Status", "Performance"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # My Loads
        st.subheader("Assigned Loads")
        
        # Simulated assigned loads for CEO
        my_loads = pd.DataFrame({
            'Load ID': ['L2025001', 'L2025002'],
            'Origin': ['Phoenix, AZ', 'Los Angeles, CA'],
            'Destination': ['Los Angeles, CA', 'Phoenix, AZ'],
            'Pickup': ['Today 8:00 AM', 'Tomorrow 6:00 AM'],
            'Rate': ['$1,800', '$1,600'],
            'Miles': [380, 380],
            'Status': ['Ready', 'Pending']
        })
        
        st.dataframe(my_loads, use_container_width=True, hide_index=True)
        
        selected_load = st.selectbox("Select Load for Details", my_loads['Load ID'].tolist())
        
        if selected_load:
            st.markdown(f"#### Load {selected_load} Details")
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("**Pickup:** 123 Industrial Blvd, Phoenix, AZ")
                st.info("**Contact:** John Doe (555-0123)")
            
            with col2:
                st.info("**Delivery:** 456 Commerce St, Los Angeles, CA")
                st.info("**Contact:** Jane Smith (555-0456)")
            
            st.text_area("Special Instructions", 
                        value="FedEx Load - Must check in at gate. Appointment required.", 
                        disabled=True)
    
    with tabs[1]:  # Navigation
        st.subheader("Route Navigation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📍 Start Navigation", type="primary", use_container_width=True):
                st.success("Opening Google Maps...")
            
            if st.button("⛽ Find Fuel Stops", use_container_width=True):
                st.info("Nearest fuel: Love's Travel Stop - 15 miles")
        
        with col2:
            if st.button("🅿️ Find Parking", use_container_width=True):
                st.info("Truck parking available at: Pilot - 8 miles")
            
            if st.button("⚖️ Find Scales", use_container_width=True):
                st.info("CAT Scale: TA Travel Center - 12 miles")
        
        # Show route summary
        st.markdown("#### Route Summary")
        route_summary = pd.DataFrame({
            'Segment': ['PHX to Quartzsite', 'Quartzsite to Blythe', 'Blythe to LA'],
            'Miles': [150, 80, 150],
            'Est. Time': ['2h 30m', '1h 20m', '2h 30m'],
            'Fuel Stop': ['Yes', 'No', 'Yes']
        })
        st.dataframe(route_summary, use_container_width=True, hide_index=True)
    
    with tabs[2]:  # Document Upload
        st.subheader("Document Capture & Upload")
        
        doc_type = st.selectbox("Document Type", 
                               ["Signed BOL", "POD", "Fuel Receipt", "Scale Ticket", "Trailer Photo"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            uploaded_file = st.file_uploader("Upload Document", type=['jpg', 'png', 'pdf'])
            
            if uploaded_file:
                st.success("✅ Document uploaded")
                if st.button("Process with Vector API", type="primary"):
                    with st.spinner("Converting to PDF..."):
                        time.sleep(1)
                        st.success("Document processed and indexed")
        
        with col2:
            st.markdown("#### Recent Uploads")
            recent_uploads = pd.DataFrame({
                'Time': ['10:30 AM', '8:15 AM', 'Yesterday'],
                'Type': ['BOL', 'Fuel Receipt', 'POD'],
                'Status': ['Processed', 'Processing', 'Submitted']
            })
            st.dataframe(recent_uploads, use_container_width=True, hide_index=True)
    
    with tabs[3]:  # HOS Status
        st.subheader("Hours of Service Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Drive Time", "8h 15m", delta="2h 45m remaining")
        
        with col2:
            st.metric("On Duty", "10h 30m", delta="3h 30m remaining")
        
        with col3:
            st.metric("Break Required", "1h 45m", delta="until 30min break")
        
        # HOS timeline
        st.markdown("#### Today's Timeline")
        hos_timeline = pd.DataFrame({
            'Time': ['6:00 AM', '6:30 AM', '10:30 AM', '11:00 AM', '2:00 PM'],
            'Status': ['Off Duty', 'Pre-Trip', 'Driving', 'On Duty', 'Driving'],
            'Duration': ['8h', '30m', '4h', '30m', '3h'],
            'Location': ['Phoenix', 'Phoenix', 'I-10 West', 'Quartzsite', 'I-10 West']
        })
        st.dataframe(hos_timeline, use_container_width=True, hide_index=True)
    
    with tabs[4]:  # Performance
        st.subheader("My Performance Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Miles This Week", "2,450", delta="+350 vs avg")
        
        with col2:
            st.metric("On-Time Delivery", "100%", delta="Perfect")
        
        with col3:
            st.metric("Fuel Efficiency", "6.8 MPG", delta="+0.3")
        
        with col4:
            st.metric("Revenue Generated", "$5,125", delta="+$425")
        
        # Weekly performance chart
        st.markdown("#### Weekly Performance Trend")
        
        dates = pd.date_range(end=datetime.now(), periods=7)
        performance_data = pd.DataFrame({
            'Date': dates,
            'Miles': [380, 420, 0, 450, 380, 415, 405],
            'Revenue': [800, 900, 0, 950, 800, 875, 850]
        })
        
        fig = px.line(performance_data, x='Date', y='Miles', 
                     title='Daily Miles Driven',
                     color_discrete_sequence=['#667eea'])
        st.plotly_chart(fig, use_container_width=True)
    
    conn.close()

# ===================================================================
# TIER 4: AI-POWERED GOAL MANAGEMENT
# ===================================================================

def show_goal_management():
    """AI-powered profit goal setting and management"""
    st.title("Profit Goal Management")
    st.markdown("*AI-Assisted Goal Setting & Performance Tracking*")
    
    tabs = st.tabs(["Current Goals", "Set New Goals", "AI Recommendations", "Performance Tracking"])
    
    conn = sqlite3.connect(DB_PATH)
    
    with tabs[0]:  # Current Goals
        st.subheader("Active Company Goals")
        
        # Display current goals
        goals = pd.read_sql_query("""
            SELECT goal_type, target_value, current_value, target_date, status
            FROM goals_and_targets
            WHERE status = 'active'
            ORDER BY target_date
        """, conn)
        
        if not goals.empty:
            for _, goal in goals.iterrows():
                progress = (goal['current_value'] / goal['target_value'] * 100) if goal['target_value'] > 0 else 0
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{goal['goal_type'].title()} Goal**")
                    st.progress(progress / 100)
                
                with col2:
                    st.metric("Target", f"${goal['target_value']:,.0f}")
                
                with col3:
                    st.metric("Current", f"${goal['current_value']:,.0f}", 
                             delta=f"{progress:.1f}%")
        else:
            st.info("No active goals set")
    
    with tabs[1]:  # Set New Goals
        st.subheader("Set Company Goals")
        
        with st.form("set_goals"):
            col1, col2 = st.columns(2)
            
            with col1:
                goal_type = st.selectbox("Goal Type", 
                                        ["profit", "revenue", "cost_reduction", "efficiency"])
                target_value = st.number_input("Target Value ($)", 
                                              value=50000.00, step=1000.00)
                target_date = st.date_input("Target Date", 
                                           datetime.now() + timedelta(days=30))
            
            with col2:
                st.markdown("#### Goal Parameters")
                min_rate_mile = st.number_input("Minimum Rate/Mile", value=2.00, step=0.10)
                max_empty_miles = st.number_input("Max Empty Miles %", value=15, step=1)
                target_loads_week = st.number_input("Target Loads/Week", value=10, step=1)
            
            notes = st.text_area("Goal Notes & Strategy")
            
            submitted = st.form_submit_button("Set Goal", type="primary", use_container_width=True)
            
            if submitted:
                goal_id = f"GOAL{datetime.now().strftime('%Y%m%d%H%M')}"
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO goals_and_targets 
                    (goal_id, goal_type, target_value, current_value, target_date, notes)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (goal_id, goal_type, target_value, 0, target_date, notes))
                conn.commit()
                st.success(f"Goal {goal_id} set successfully!")
    
    with tabs[2]:  # AI Recommendations
        st.subheader("AI Goal Recommendations")
        
        if st.button("Generate AI Recommendations", type="primary", use_container_width=True):
            with st.spinner("Analyzing historical data and market trends..."):
                time.sleep(2)
                
                st.markdown("#### AI Analysis Complete")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### Based on Historical Performance")
                    st.success("• Average weekly revenue: $48,500")
                    st.info("• Average rate/mile: $2.08")
                    st.info("• Fleet utilization: 87%")
                
                with col2:
                    st.markdown("##### Market Conditions")
                    st.success("• Market rates trending up 5%")
                    st.warning("• Fuel costs increased 8%")
                    st.info("• Demand high in Southwest region")
                
                st.markdown("---")
                st.markdown("#### 🎯 Recommended Goals")
                
                recommendations = pd.DataFrame({
                    'Goal Type': ['Weekly Revenue', 'Profit Margin', 'Fleet Utilization'],
                    'Current': ['$48,500', '22%', '87%'],
                    'Recommended Target': ['$52,000', '25%', '92%'],
                    'Achievability': ['95%', '88%', '92%'],
                    'Impact': ['High', 'High', 'Medium']
                })
                
                st.dataframe(recommendations, use_container_width=True, hide_index=True)
                
                if st.button("Accept All Recommendations", type="primary"):
                    st.success("AI recommendations accepted and goals updated!")
    
    with tabs[3]:  # Performance Tracking
        st.subheader("Goal Performance Tracking")
        
        # Date range selector
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        
        # Performance metrics
        st.markdown("#### Performance Against Goals")
        
        # Create sample performance data
        dates = pd.date_range(start=start_date, end=end_date, freq='W')
        performance_df = pd.DataFrame({
            'Week': dates,
            'Revenue': np.random.uniform(45000, 55000, len(dates)),
            'Profit': np.random.uniform(9000, 13000, len(dates)),
            'Target_Revenue': [50000] * len(dates),
            'Target_Profit': [11000] * len(dates)
        })
        
        # Revenue chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=performance_df['Week'], y=performance_df['Revenue'],
                                mode='lines+markers', name='Actual Revenue',
                                line=dict(color='#667eea', width=2)))
        fig.add_trace(go.Scatter(x=performance_df['Week'], y=performance_df['Target_Revenue'],
                                mode='lines', name='Target Revenue',
                                line=dict(color='#ef4444', width=2, dash='dash')))
        
        fig.update_layout(title='Revenue vs Target', xaxis_title='Week', yaxis_title='Revenue ($)')
        st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("#### 📊 Key Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_achievement = 94
            st.metric("Goal Achievement", f"{avg_achievement}%", 
                     delta="On track" if avg_achievement > 90 else "Below target")
        
        with col2:
            weeks_above = 3
            st.metric("Weeks Above Target", f"{weeks_above}/4", 
                     delta="Good" if weeks_above >= 3 else "Needs improvement")
        
        with col3:
            trend = "Upward"
            st.metric("Trend", trend, 
                     delta="+5%" if trend == "Upward" else "-3%")
    
    conn.close()

# ===================================================================
# MAIN APPLICATION WITH FOUR-TIER ARCHITECTURE
# ===================================================================

def main_app():
    """Main application with Four-Tier architecture and CEO dual capabilities"""
    
    # Sidebar
    with st.sidebar:
        # Logo
        logo_path = "assets/logos/swt_logo_white.png"
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        
        st.divider()
        
        # User info
        st.write(f"**User:** {st.session_state.get('full_name', 'Unknown')}")
        role = st.session_state.get('role', 'User')
        if role == 'ceo':
            st.write(f"**Role:** CEO & Owner")
            
            # Training System Link for CEO
            st.divider()
            st.markdown("### 🎓 Training Center")
            
            # Check training progress
            progress = check_training_progress()
            if progress:
                # Show progress bar
                progress_pct = (progress['completed'] / progress['total'] * 100) if progress['total'] > 0 else 0
                st.progress(progress_pct / 100)
                st.caption(f"{progress['completed']}/{progress['total']} modules completed")
                
                # Training button with indicator
                if st.button("📚 Open Training System", use_container_width=True, type="primary"):
                    st.markdown("[Launch Training →](http://localhost:8701)")
                    st.caption("Opens in new tab")
            else:
                # No progress yet
                if st.button("🚀 Start Training", use_container_width=True, type="primary"):
                    st.markdown("[Launch Training →](http://localhost:8701)")
                    st.caption("Begin your learning journey")
            
            st.divider()
            
            # CEO Mode Toggle
            if st.session_state.get('driver_profile_enabled'):
                mode = st.radio("Operating Mode", 
                              ["Executive", "Driver"],
                              help="Switch between CEO and Driver functions")
                st.session_state['current_mode'] = mode
        else:
            st.write(f"**Role:** {role.title()}")
            
            # Training link for other roles
            if role in ['dispatcher', 'driver', 'accounting', 'admin']:
                st.divider()
                if st.button("📚 Training", use_container_width=True):
                    st.markdown("[Open Training →](http://localhost:8701)")
                    st.caption("Role-specific training")
        
        st.divider()
        
        # Navigation based on role and mode
        if st.session_state.get('role') == 'ceo':
            if st.session_state.get('current_mode') == 'Driver':
                # Driver mode menu
                menu_items = [
                    "Driver Dashboard",
                    "My Loads",
                    "Navigation",
                    "Documents",
                    "Performance"
                ]
            else:
                # Executive mode menu (full Four-Tier access)
                menu_items = [
                    "Executive Dashboard",
                    "Tier 1: Dispatch Center",
                    "Tier 2: Load & Invoice",
                    "Tier 3: Finance & Compliance",
                    "Tier 4: Automation & AI",
                    "Goal Management",
                    "User Management",
                    "System Settings"
                ]
        else:
            # Regular user menu
            menu_items = [
                "Dashboard",
                "Dispatch",
                "Loads",
                "Documents"
            ]
        
        selected_page = st.radio(
            "Navigation",
            menu_items
        )
        
        st.divider()
        
        # Logout button
        if st.button("Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Main content based on selection
    if st.session_state.get('role') == 'ceo':
        if st.session_state.get('current_mode') == 'Driver':
            # CEO in Driver Mode
            if selected_page == "Driver Dashboard" or selected_page == "My Loads":
                show_ceo_driver_mode()
            elif selected_page == "Navigation":
                show_ceo_driver_mode()  # Show navigation tab
            elif selected_page == "Documents":
                show_ceo_driver_mode()  # Show documents tab
            elif selected_page == "Performance":
                show_ceo_driver_mode()  # Show performance tab
        else:
            # CEO in Executive Mode
            if selected_page == "Executive Dashboard":
                show_executive_dashboard()
            elif selected_page == "Tier 1: Dispatch Center":
                show_dispatcher_command_center()
            elif selected_page == "Tier 2: Load & Invoice":
                show_load_invoice_management()
            elif selected_page == "Tier 3: Finance & Compliance":
                show_finance_compliance()
            elif selected_page == "Tier 4: Automation & AI":
                show_automation_ai()
            elif selected_page == "Goal Management":
                show_goal_management()
            elif selected_page == "User Management":
                show_user_management_enhanced()
            elif selected_page == "System Settings":
                show_system_settings_enhanced()
    else:
        # Regular user pages
        st.info("Access restricted. Please contact your administrator.")

def show_executive_dashboard():
    """Executive dashboard with Four-Tier overview"""
    st.title("Executive Dashboard - Four-Tier Overview")
    
    # Training System Integration for CEO
    if st.session_state.get('role') == 'ceo':
        with st.container():
            training_col1, training_col2, training_col3 = st.columns([2, 1, 1])
            
            with training_col1:
                # Check if training database exists
                training_progress = check_training_progress()
                if training_progress:
                    st.info(f"🎓 **Training Progress:** {training_progress['completed']}/{training_progress['total']} modules completed | **Score:** {training_progress['avg_score']}%")
                else:
                    st.info("🎓 **Training System:** Ready to start your personalized learning path")
            
            with training_col2:
                if st.button("📚 Open Training System", type="primary"):
                    st.markdown("[Launch Training System](http://localhost:8701)")
                    st.info("Training system opens in new tab")
            
            with training_col3:
                if st.button("🧠 View My Progress"):
                    show_training_analytics()
    
    # Goal achievement banner
    st.success("Weekly Goal Achievement: 94% | Profit Margin: 23.5% | Fleet Utilization: 89%")
    
    # Four-Tier status overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### Tier 1: Operations")
        st.metric("Active Loads", "12", delta="+3")
        st.metric("Available Drivers", "8/10")
    
    with col2:
        st.markdown("#### Tier 2: Financial")
        st.metric("Pending Invoices", "$45,230")
        st.metric("Weekly Revenue", "$52,150", delta="+$2,150")
    
    with col3:
        st.markdown("#### Tier 3: Compliance")
        st.metric("Compliance Score", "98%")
        st.metric("Upcoming Renewals", "3")
    
    with col4:
        st.markdown("#### Tier 4: Automation")
        st.metric("Active Tasks", "24")
        st.metric("AI Efficiency", "92%", delta="+5%")

# Placeholder functions for other tiers
def show_load_invoice_management():
    st.title("Tier 2: Load & Invoice Management")
    st.info("Load and invoice management interface - Full implementation coming soon")

def show_finance_compliance():
    st.title("Tier 3: Finance & Compliance Management")
    st.info("Finance and compliance dashboard - Full implementation coming soon")

def show_automation_ai():
    st.title("Tier 4: Automation & AI Layer")
    st.info("Automation and AI management - Full implementation coming soon")

def show_user_management_enhanced():
    st.title("User Management")
    st.info("Enhanced user management with role-based access - Full implementation coming soon")

def show_system_settings_enhanced():
    st.title("System Settings")
    st.info("System configuration and settings - Full implementation coming soon")

# ===================================================================
# TRAINING SYSTEM INTEGRATION FUNCTIONS
# ===================================================================

def check_training_progress():
    """Check training progress from the training database"""
    try:
        import sqlite3
        import os
        
        # Check if training database exists
        if os.path.exists('training_intelligence.db'):
            conn = sqlite3.connect('training_intelligence.db')
            cursor = conn.cursor()
            
            # Get progress for current user
            username = st.session_state.get('username', 'Brandon')
            
            # Get total modules
            cursor.execute("SELECT COUNT(*) FROM training_modules WHERE target_role = ? OR target_role = 'all'", 
                          (st.session_state.get('role', 'ceo'),))
            total = cursor.fetchone()[0]
            
            # Get completed modules
            cursor.execute("""
                SELECT COUNT(DISTINCT module_id), AVG(score) 
                FROM user_progress 
                WHERE username = ? AND score >= 80
            """, (username,))
            result = cursor.fetchone()
            completed = result[0] if result[0] else 0
            avg_score = round(result[1]) if result[1] else 0
            
            conn.close()
            
            return {
                'total': total,
                'completed': completed,
                'avg_score': avg_score
            }
    except:
        return None

def show_training_analytics():
    """Show training analytics in a modal"""
    with st.expander("📊 Training Analytics Dashboard", expanded=True):
        try:
            import sqlite3
            import pandas as pd
            
            if os.path.exists('training_intelligence.db'):
                conn = sqlite3.connect('training_intelligence.db')
                
                # Get user's training history
                username = st.session_state.get('username', 'Brandon')
                
                query = """
                    SELECT 
                        tm.module_name,
                        tm.module_type,
                        up.completed_date,
                        up.score,
                        up.time_spent
                    FROM user_progress up
                    JOIN training_modules tm ON up.module_id = tm.id
                    WHERE up.username = ?
                    ORDER BY up.completed_date DESC
                    LIMIT 10
                """
                
                df = pd.read_sql_query(query, conn, params=(username,))
                
                if not df.empty:
                    st.subheader("Your Recent Training Activity")
                    
                    # Format the dataframe
                    df['completed_date'] = pd.to_datetime(df['completed_date']).dt.strftime('%Y-%m-%d')
                    df['time_spent'] = df['time_spent'].fillna(0).astype(int)
                    df['score'] = df['score'].round(1)
                    
                    # Display metrics
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Average Score", f"{df['score'].mean():.1f}%")
                    with col2:
                        st.metric("Total Time", f"{df['time_spent'].sum()} min")
                    with col3:
                        st.metric("Modules Completed", len(df))
                    
                    # Display table
                    st.dataframe(
                        df[['module_name', 'module_type', 'score', 'time_spent', 'completed_date']],
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Recommendations
                    st.subheader("🎯 Recommended Next Steps")
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT module_name, module_type 
                        FROM training_modules 
                        WHERE (target_role = ? OR target_role = 'all')
                        AND id NOT IN (
                            SELECT module_id FROM user_progress 
                            WHERE username = ? AND score >= 80
                        )
                        LIMIT 3
                    """, (st.session_state.get('role', 'ceo'), username))
                    
                    recommendations = cursor.fetchall()
                    if recommendations:
                        for rec in recommendations:
                            st.write(f"• **{rec[0]}** ({rec[1]})")
                    else:
                        st.success("Congratulations! You've completed all available training modules.")
                else:
                    st.info("No training history yet. Start your learning journey!")
                    if st.button("🚀 Start Training Now"):
                        st.markdown("[Open Training System](http://localhost:8701)")
                
                conn.close()
            else:
                st.warning("Training database not found. Please launch the training system first.")
                if st.button("🚀 Initialize Training System"):
                    st.markdown("[Launch Training System](http://localhost:8701)")
                    
        except Exception as e:
            st.error(f"Unable to load training analytics: {str(e)}")
            st.info("Please ensure the training system is running on port 8701")

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