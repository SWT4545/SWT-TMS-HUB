"""
Simple Authentication Module - No Video Loading
"""
import streamlit as st
import sqlite3
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = "swt_tms.db"

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user against database"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute("SELECT role FROM users WHERE username = ? AND password_hash = ?", 
                      (username, password_hash))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]  # Return role
        return None
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None

def show_simple_login():
    """Display simple login form without video"""
    st.markdown("<h1 style='text-align: center;'>🚚 SMITH & WILLIAMS TRUCKING</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Transportation Management System</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username and password:
                    role = authenticate_user(username, password)
                    if role:
                        st.session_state.authenticated = True
                        st.session_state.user_role = role
                        st.session_state.username = username
                        st.success(f"Welcome {username}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Please enter both username and password")

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)