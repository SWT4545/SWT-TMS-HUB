"""
Authentication Module for Smith & Williams Trucking TMS
"""
import streamlit as st
import sqlite3
import hashlib
import base64
import os
import time
import logging
from datetime import datetime
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "swt_tms.db"

def init_database():
    """Initialize database with users table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
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
    
    # Check if any users exist
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    # If no users, create default admin
    if user_count == 0:
        # Create default brandon/ceo123 user
        brandon_hash = hashlib.sha256("ceo123".encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("brandon", brandon_hash, "super_user", "Brandon Smith", "brandon@swtrucking.com", 1))
        
        # Also create a demo admin
        admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
        cursor.execute("""INSERT INTO users 
            (username, password_hash, role, full_name, email, is_active) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            ("admin", admin_hash, "super_user", "System Administrator", "admin@swtrucking.com", 1))
        
        conn.commit()
    
    conn.close()

def authenticate_user(username, password):
    """Authenticate user against database"""
    # Ensure database exists
    init_database()
    
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
        return {
            'id': user[0],
            'username': user[1],
            'role': user[2],
            'full_name': user[3],
            'email': user[4]
        }
    
    conn.close()
    return None

def show_login():
    """Display clean professional login interface"""
    
    # Initialize database on first run
    init_database()
    
    # Simple centered logo display - NO CONTAINERS OR BOXES
    st.markdown("""
    <style>
    .clean-logo {
        text-align: center;
        margin: 40px 0;
    }
    .clean-logo img {
        filter: drop-shadow(0 8px 16px rgba(0,0,0,0.4));
    }
    .company-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.4em;
        font-weight: 300;
        letter-spacing: 2px;
        margin: 20px 0;
    }
    .company-slogan {
        text-align: center;
        color: #60a5fa;
        font-size: 1.6em;
        font-weight: 800;
        letter-spacing: 2px;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Clean logo display - centered with no background boxes
    logo_path = "assets/logos/swt_logo_white.png"
    try:
        st.markdown('<div class="clean-logo">', unsafe_allow_html=True)
        st.image(logo_path, width=580)
        st.markdown('</div>', unsafe_allow_html=True)
        logger.info("Clean logo displayed successfully")
        
    except Exception as e:
        logger.error(f"Error loading logo: {e}")
        # Clean text fallback
        st.markdown("""
        <div style="text-align: center; margin: 40px 0;">
            <h1 style="color: white; font-size: 3em; margin: 0;">SMITH & WILLIAMS</h1>
            <h2 style="color: #e2e8f0; font-size: 2em; margin: 10px 0;">TRUCKING LLC</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Clean company information
    st.markdown("""
    <p class="company-title">TRANSPORTATION MANAGEMENT SYSTEM</p>
    <p class="company-slogan">PROFESSIONAL FLEET MANAGEMENT SOLUTIONS</p>
    """, unsafe_allow_html=True)
    
    # Show default credentials info
    with st.expander("Login Information"):
        st.info("""
        **Default Credentials:**
        - Username: `brandon` | Password: `ceo123`
        - Username: `admin` | Password: `admin123`
        """)
    
    # Clean login form section
    st.markdown("""
    <style>
    .simple-login {
        max-width: 400px;
        margin: 40px auto;
        padding: 30px;
        background: rgba(15, 23, 42, 0.8);
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .login-header {
        color: white;
        font-size: 1.8em;
        font-weight: 600;
        text-align: center;
        margin-bottom: 25px;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Simple centered login form
    st.markdown('<div class="simple-login">', unsafe_allow_html=True)
    st.markdown('<h2 class="login-header">SECURE LOGIN</h2>', unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            login_button = st.form_submit_button("LOGIN", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.form_submit_button("CLEAR", use_container_width=True)
        
        if login_button:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user = user['username']
                    st.session_state.role = user['role']
                    st.session_state.user_full_name = user['full_name']
                    st.session_state.user_id = user['id']
                    st.success(f"Welcome back, {user['full_name']}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter both username and password")
        
        if clear_button:
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout():
    """Logout the current user"""
    for key in ['authenticated', 'user', 'role', 'user_full_name', 'user_id']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()