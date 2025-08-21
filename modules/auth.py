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
    
    # Center column for logo/video
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # PRIORITY: Display video first, fallback to logo if needed
        # ONLY ONE WILL DISPLAY - NEVER BOTH
        
        # Log current working directory and check for video
        logger.info(f"Current working directory: {os.getcwd()}")
        logger.info(f"Looking for video file...")
        
        # Check multiple possible paths
        video_paths = [
            "assets/videos/company_logo_animation.mp4.MOV",
            "assets/videos/company_logo_animation.mp4",
            "./assets/videos/company_logo_animation.mp4.MOV",
            os.path.join(os.getcwd(), "assets", "videos", "company_logo_animation.mp4.MOV")
        ]
        
        video_found = False
        for vp in video_paths:
            video_path = Path(vp)
            logger.info(f"Checking path: {vp}")
            logger.info(f"Path exists: {video_path.exists()}")
            logger.info(f"Absolute path: {video_path.absolute()}")
            
            if video_path.exists():
                video_found = True
                logger.info(f"Video found at: {video_path.absolute()}")
                logger.info(f"File size: {video_path.stat().st_size / 1024 / 1024:.2f} MB")
                
                try:
                    # Check if mobile device and use smaller video
                    import streamlit as st
                    user_agent = st.context.headers.get("User-Agent", "").lower() if hasattr(st.context, 'headers') else ""
                    is_mobile = any(x in user_agent for x in ["mobile", "android", "iphone", "ipad"])
                    
                    # Use mobile version if available and on mobile device
                    mobile_video_path = Path("assets/videos/company_logo_animation_mobile.mp4")
                    video_to_use = mobile_video_path if (is_mobile and mobile_video_path.exists()) else video_path
                    
                    # Smaller dimensions for mobile
                    width, height = (300, 225) if is_mobile else (400, 300)
                    
                    # Display video with HTML5 for loop and muted autoplay
                    with open(video_to_use, 'rb') as video_file:
                        video_bytes = video_file.read()
                        video_b64 = base64.b64encode(video_bytes).decode()
                        
                        # HTML5 video with autoplay, muted, and loop
                        video_html = f'''
                        <div style="display: flex; justify-content: center; margin: 20px 0;">
                            <video width="{width}" height="{height}" autoplay muted loop playsinline style="border-radius: 10px;">
                                <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                                <source src="data:video/quicktime;base64,{video_b64}" type="video/quicktime">
                                Your browser does not support the video tag.
                            </video>
                        </div>
                        '''
                        st.markdown(video_html, unsafe_allow_html=True)
                        logger.info("Video displayed with loop and muted")
                    break
                except Exception as e:
                    logger.error(f"Error displaying video: {e}")
                    st.error(f"Error loading video: {e}")
        
        if not video_found:
            logger.warning("Video file not found at any expected location")
            # List files in assets directory for debugging
            try:
                assets_path = Path("assets")
                if assets_path.exists():
                    logger.info(f"Contents of assets directory: {list(assets_path.iterdir())}")
                    videos_path = assets_path / "videos"
                    if videos_path.exists():
                        logger.info(f"Contents of assets/videos: {list(videos_path.iterdir())}")
            except Exception as e:
                logger.error(f"Error listing directory contents: {e}")
            
            st.info("🚚 Smith & Williams Trucking")
    
    # Company titles
    st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>Transportation Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8B0000; font-weight: bold;'>SMITH & WILLIAMS TRUCKING</h3>", unsafe_allow_html=True)
    
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