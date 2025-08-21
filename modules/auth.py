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
    """Display login interface with enhanced Smith & Williams branding"""
    
    # Initialize database on first run
    init_database()
    
    # Enhanced logo section with better styling
    st.markdown("""
    <style>
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 30px 0;
        padding: 40px;
        background: linear-gradient(145deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        border-radius: 20px;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.3),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .logo-wrapper {
        text-align: center;
        max-width: 600px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center logo with enhanced styling
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.markdown('<div class="logo-wrapper">', unsafe_allow_html=True)
        
        # Display company logo - enhanced and bigger
        logo_path = "assets/logos/swt_logo_white.png"
        try:
            # Bigger, cleaner logo with better styling
            st.image(logo_path, width=550, use_column_width=False)
            logger.info("Enhanced white logo displayed successfully")
            
            # Add subtle tagline below logo
            st.markdown("""
            <div style="margin-top: 20px;">
                <p style="color: #94a3b8; font-size: 1.1em; margin: 0; font-weight: 300; letter-spacing: 1px;">
                    TRANSPORTATION MANAGEMENT SYSTEM
                </p>
                <p style="color: #64748b; font-size: 0.9em; margin: 10px 0 0 0; font-style: italic;">
                    Reliable • Professional • Efficient
                </p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            # Enhanced fallback with better styling
            st.markdown("""
            <div style="text-align: center;">
                <h1 style="color: white; margin: 0; font-size: 3.5em; font-weight: 700; text-shadow: 2px 2px 8px rgba(0,0,0,0.5);">
                    SMITH & WILLIAMS
                </h1>
                <h2 style="color: #e2e8f0; margin: 15px 0; font-size: 2.2em; font-weight: 400;">
                    TRUCKING LLC
                </h2>
                <div style="width: 200px; height: 3px; background: linear-gradient(90deg, #3b82f6, #06b6d4); margin: 20px auto; border-radius: 2px;"></div>
                <p style="color: #94a3b8; font-size: 1.1em; margin: 20px 0 0 0; letter-spacing: 1px;">
                    🚚 TRANSPORTATION MANAGEMENT SYSTEM
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show default credentials info
    with st.expander("📌 Login Information"):
        st.info("""
        **Default Credentials:**
        - Username: `brandon` | Password: `ceo123`
        - Username: `admin` | Password: `admin123`
        """)
    
    # Login form with proper styling
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            login_button = st.form_submit_button("🔐 LOGIN", type="primary", use_container_width=True)
        with col_btn2:
            clear_button = st.form_submit_button("🔄 CLEAR", use_container_width=True)
        
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
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter both username and password")
        
        if clear_button:
            st.rerun()
    
    # Apply aggressive button styling using JavaScript injection
    st.markdown("""
    <script>
        // Wait for page to load then style buttons
        setTimeout(function() {
            // Find all form submit buttons
            const buttons = document.querySelectorAll('.stFormSubmitButton button');
            if (buttons.length >= 2) {
                // Style Login button - black with red border
                buttons[0].style.backgroundColor = '#000000';
                buttons[0].style.color = '#ffffff';
                buttons[0].style.border = '3px solid #8B0000';
                buttons[0].style.fontWeight = '700';
                buttons[0].style.textTransform = 'uppercase';
                
                // Style Clear button - red with black border  
                buttons[1].style.backgroundColor = '#8B0000';
                buttons[1].style.color = '#ffffff';
                buttons[1].style.border = '3px solid #000000';
                buttons[1].style.fontWeight = '700';
                buttons[1].style.textTransform = 'uppercase';
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # Vernon Protection Footer
    st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 3px solid #8B0000;'>
        <p style='color: #8B0000; font-size: 12px; font-weight: 700; letter-spacing: 1px; margin: 0; text-transform: uppercase;'>
            🔒 DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER
        </p>
        <p style='color: white; font-size: 11px; margin-top: 5px; font-weight: 600;'>
            © 2025 Smith & Williams Trucking LLC - All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout():
    """Logout the current user"""
    for key in ['authenticated', 'user', 'role', 'user_full_name', 'user_id']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()