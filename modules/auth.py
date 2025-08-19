"""
Authentication Module for Smith & Williams Trucking TMS
"""
import streamlit as st
import sqlite3
import hashlib
import base64
import os
import time
from datetime import datetime

DB_PATH = "swt_tms.db"

def authenticate_user(username, password):
    """Authenticate user against database"""
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
    """Display login page with Smith & Williams branding and video logo"""
    
    # Custom CSS for login page - Red, Black, and White theme
    st.markdown("""
    <style>
        /* Login Page Styling - Smith & Williams Theme */
        .main {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        }
        
        .stApp {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        }
        
        /* Login container */
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(220, 38, 38, 0.3);
            border: 2px solid #DC2626;
        }
        
        /* Headers */
        h1 {
            color: #DC2626 !important;
            text-align: center;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        h3 {
            color: #8B0000 !important;
            text-align: center;
        }
        
        /* Input fields */
        .stTextInput > div > div > input {
            background-color: white;
            border: 2px solid #DC2626;
            border-radius: 5px;
            color: #000000;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #8B0000;
            box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.2);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #DC2626 0%, #8B0000 100%);
            color: white;
            border: none;
            padding: 0.75rem 2rem;
            font-weight: 600;
            border-radius: 5px;
            width: 100%;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #8B0000 0%, #DC2626 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        }
        
        /* Video container */
        .video-container {
            text-align: center;
            margin-bottom: 2rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.05);
            border-radius: 10px;
        }
        
        /* Footer */
        .login-footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1rem;
            border-top: 2px solid #DC2626;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create centered login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display video logo
        animation_file = "assets/videos/company_logo_animation.mp4.MOV"
        
        if os.path.exists(animation_file):
            try:
                with open(animation_file, 'rb') as video_file:
                    video_bytes = video_file.read()
                    video_b64 = base64.b64encode(video_bytes).decode()
                    video_html = f'''
                    <div class="video-container">
                        <video width="100%" height="auto" autoplay loop muted playsinline style="max-width: 400px; border-radius: 10px;">
                            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    '''
                    st.markdown(video_html, unsafe_allow_html=True)
            except Exception as e:
                # Fallback to static logo
                logo_path = "assets/logos/swt_logo.png"
                if os.path.exists(logo_path):
                    st.image(logo_path, use_container_width=True)
        else:
            # Fallback to static logo
            logo_path = "assets/logos/swt_logo.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
        
        # Company name and title
        st.markdown("<h1>🚚 SMITH & WILLIAMS TRUCKING</h1>", unsafe_allow_html=True)
        st.markdown("<h3>Transportation Management System</h3>", unsafe_allow_html=True)
        
        # Login form
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                login_button = st.form_submit_button("🔐 Login", type="primary", use_container_width=True)
            with col_btn2:
                clear_button = st.form_submit_button("🔄 Clear", use_container_width=True)
            
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
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer with Vernon protection message
    st.markdown("""
    <div class='login-footer'>
        <p style='color: #DC2626; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin: 0;'>
            🔒 DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER
        </p>
        <p style='color: #ffffff; font-size: 11px; margin-top: 5px;'>
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