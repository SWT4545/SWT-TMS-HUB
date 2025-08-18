"""
Authentication module for SWT TMS Hub
"""
import streamlit as st
import hashlib
import time
from datetime import datetime
from config.database import get_connection
import logging

logger = logging.getLogger(__name__)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    """Authenticate user against database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        
        cursor.execute("""SELECT id, username, role, full_name, email, is_active 
                         FROM users 
                         WHERE username = ? AND password_hash = ? AND is_active = 1""",
                      (username, password_hash))
        user = cursor.fetchone()
        
        if user:
            # Update last login
            cursor.execute("UPDATE users SET last_login = ? WHERE id = ?",
                          (datetime.now(), user[0]))
            conn.commit()
            logger.info(f"User {username} authenticated successfully")
            
            return {
                'id': user[0],
                'username': user[1],
                'role': user[2],
                'full_name': user[3],
                'email': user[4],
                'is_active': user[5]
            }
        else:
            logger.warning(f"Authentication failed for user: {username}")
            return None
            
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        return None
    finally:
        conn.close()

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout():
    """Clear session and logout user"""
    user = st.session_state.get('username', 'Unknown')
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    logger.info(f"User {user} logged out")

def show_login():
    """Display login form"""
    st.markdown("<h1 style='text-align: center;'>🚚 TMS Hub Login</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Smith & Williams Trucking LLC</h3>", unsafe_allow_html=True)
    
    # Create login form
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("🔐 Login", type="primary", use_container_width=True)
        with col2:
            clear_btn = st.form_submit_button("🔄 Clear", use_container_width=True)
        
        if clear_btn:
            st.rerun()
            
        if login_btn:
            if username and password:
                user = authenticate_user(username, password)
                if user:
                    # Set session state
                    st.session_state['authenticated'] = True
                    st.session_state['user_id'] = user['id']
                    st.session_state['username'] = user['username']
                    st.session_state['role'] = user['role']
                    st.session_state['full_name'] = user['full_name']
                    st.session_state['email'] = user['email']
                    
                    st.success(f"Welcome, {user['full_name']}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.error("⚠️ Please enter both username and password")
    
    # Show default credentials
    st.info("💡 **Default Login:** Username: `Brandon` | Password: `ceo123`")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<p style='text-align: center; color: #666;'>© 2025 Smith & Williams Trucking LLC - All Rights Reserved</p>",
        unsafe_allow_html=True
    )

def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not check_authentication():
            show_login()
            return None
        return func(*args, **kwargs)
    return wrapper

def require_role(required_roles):
    """Decorator to require specific roles"""
    if isinstance(required_roles, str):
        required_roles = [required_roles]
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_authentication():
                show_login()
                return None
            
            user_role = st.session_state.get('role')
            if user_role not in required_roles and 'super_user' not in required_roles:
                st.error(f"❌ Access denied. Required role: {', '.join(required_roles)}")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator