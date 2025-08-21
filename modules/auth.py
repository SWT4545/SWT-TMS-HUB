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
    """Display professional login interface with premium Smith & Williams branding"""
    
    # Initialize database on first run
    init_database()
    
    # Professional page styling
    st.markdown("""
    <style>
    .professional-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 30%, #334155 70%, #475569 100%);
        padding: 50px 40px;
        border-radius: 25px;
        margin: 20px 0 40px 0;
        box-shadow: 
            0 25px 50px rgba(0,0,0,0.4),
            inset 0 1px 0 rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.1);
        position: relative;
    }
    .professional-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #06b6d4, #8b5cf6, #3b82f6);
        border-radius: 25px 25px 0 0;
    }
    .company-tagline {
        font-size: 1.3em;
        color: #94a3b8;
        text-align: center;
        margin: 25px 0 20px 0;
        letter-spacing: 2px;
        font-weight: 300;
    }
    .professional-badges {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin-top: 25px;
        flex-wrap: wrap;
    }
    .pro-badge {
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        padding: 10px 20px;
        border-radius: 25px;
        font-size: 0.95em;
        font-weight: 600;
        border: 1px solid rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main professional header
    st.markdown('<div class="professional-header">', unsafe_allow_html=True)
    
    # Enhanced logo display with professional layout
    col1, col2, col3 = st.columns([0.1, 1, 0.1])
    with col2:
        # Display company logo with raised effect and perfect centering
        logo_path = "assets/logos/swt_logo_white.png"
        try:
            # Centered logo with raised effect
            st.markdown("""
            <div style="
                display: flex; 
                justify-content: center; 
                align-items: center; 
                margin: 30px 0 40px 0;
                padding: 25px;
                background: rgba(255,255,255,0.05);
                border-radius: 20px;
                box-shadow: 
                    0 20px 40px rgba(0,0,0,0.4),
                    inset 0 1px 0 rgba(255,255,255,0.2),
                    inset 0 -1px 0 rgba(0,0,0,0.2);
                border: 1px solid rgba(255,255,255,0.1);
            ">
            """, unsafe_allow_html=True)
            
            # Logo with additional raised effect
            st.markdown("""
            <style>
            .raised-logo img {
                filter: drop-shadow(0 10px 20px rgba(0,0,0,0.5)) 
                        drop-shadow(0 5px 10px rgba(0,0,0,0.3));
                transition: all 0.3s ease;
            }
            .raised-logo img:hover {
                filter: drop-shadow(0 15px 30px rgba(0,0,0,0.6)) 
                        drop-shadow(0 8px 15px rgba(0,0,0,0.4));
                transform: translateY(-2px);
            }
            </style>
            <div class="raised-logo">
            """, unsafe_allow_html=True)
            
            st.image(logo_path, width=580)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            logger.info("Raised logo displayed successfully")
            
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            # Professional fallback branding
            st.markdown("""
            <div style="text-align: center;">
                <h1 style="color: white; font-size: 3.5em; font-weight: 800; margin: 0; letter-spacing: 2px; text-shadow: 2px 2px 10px rgba(0,0,0,0.7);">
                    SMITH & WILLIAMS
                </h1>
                <h2 style="color: #e2e8f0; font-size: 2em; font-weight: 300; margin: 15px 0; letter-spacing: 3px;">
                    TRUCKING LLC
                </h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Company slogan and professional description
        st.markdown("""
        <p class="company-tagline">
            TRANSPORTATION MANAGEMENT SYSTEM
        </p>
        <div style="text-align: center; margin-top: 25px;">
            <p style="color: #60a5fa; font-size: 1.4em; font-weight: 600; letter-spacing: 2px; margin: 0;">
                "MOVING AMERICA FORWARD, ONE LOAD AT A TIME"
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show default credentials info
    with st.expander("Login Information"):
        st.info("""
        **Default Credentials:**
        - Username: `brandon` | Password: `ceo123`
        - Username: `admin` | Password: `admin123`
        """)
    
    # Professional login form section
    st.markdown("""
    <style>
    .login-container {
        background: rgba(15, 23, 42, 0.95);
        padding: 40px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    .login-title {
        color: white;
        font-size: 2.2em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }
    .stTextInput input {
        font-size: 1.1em !important;
        padding: 12px !important;
        background: rgba(30, 41, 59, 0.8) !important;
        border: 2px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    .stTextInput label {
        font-size: 1.2em !important;
        color: #e2e8f0 !important;
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional login form container
    col1, col2, col3 = st.columns([0.3, 1, 0.3])
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="login-title">SECURE LOGIN</h2>', unsafe_allow_html=True)
        
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