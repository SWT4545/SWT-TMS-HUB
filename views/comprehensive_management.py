"""
MINIMAL Comprehensive Management Module - CANNOT FAIL
Emergency version with zero external dependencies
"""
import streamlit as st
import sqlite3
import hashlib
from datetime import datetime

def show_comprehensive_management_view():
    """Minimal management interface that cannot fail"""
    st.title("Management Center")
    
    # Check permissions
    if st.session_state.get('role') not in ['super_user', 'ceo', 'admin']:
        st.error("Access Denied: Admin privileges required")
        return
    
    # Simple tabs
    tab1, tab2 = st.tabs(["User Management", "System Status"])
    
    with tab1:
        show_minimal_user_management()
    
    with tab2:
        show_system_status()

def show_minimal_user_management():
    """Minimal user management"""
    st.header("User Management")
    
    # Add user form
    with st.expander("Add New User"):
        with st.form("add_user"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            role = st.selectbox("Role", ["super_user", "admin", "user"])
            full_name = st.text_input("Full Name")
            
            if st.form_submit_button("Add User"):
                if username and password:
                    try:
                        conn = sqlite3.connect("swt_tms.db")
                        cursor = conn.cursor()
                        
                        # Create table if needed
                        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password_hash TEXT NOT NULL,
                            role TEXT NOT NULL,
                            full_name TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            is_active BOOLEAN DEFAULT 1
                        )''')
                        
                        # Add user
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        cursor.execute("""
                            INSERT INTO users (username, password_hash, role, full_name, is_active)
                            VALUES (?, ?, ?, ?, ?)
                        """, (username, password_hash, role, full_name, 1))
                        
                        conn.commit()
                        conn.close()
                        st.success(f"User {username} added successfully!")
                        
                    except sqlite3.IntegrityError:
                        st.error("Username already exists!")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please fill username and password")
    
    # List users
    try:
        conn = sqlite3.connect("swt_tms.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username, role, full_name, is_active FROM users")
        users = cursor.fetchall()
        conn.close()
        
        if users:
            st.subheader("Current Users")
            for user in users:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.text(user[0])  # username
                with col2:
                    st.text(user[1])  # role
                with col3:
                    st.text(user[2] or "")  # full_name
                with col4:
                    st.text("Active" if user[3] else "Inactive")
        else:
            st.info("No users found")
            
    except Exception as e:
        st.warning(f"Could not load users: {str(e)}")
        st.info("Database may not be initialized yet")

def show_system_status():
    """Show basic system status"""
    st.header("System Status")
    
    # Test database
    try:
        conn = sqlite3.connect("swt_tms.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        conn.close()
        st.success(f"Database connected - {table_count} tables")
    except Exception as e:
        st.error(f"Database issue: {str(e)}")
    
    # Session info
    if 'username' in st.session_state:
        st.info(f"Logged in as: {st.session_state.get('username', 'Unknown')}")
        st.info(f"Role: {st.session_state.get('role', 'Unknown')}")
    else:
        st.warning("No session information")
    
    # Basic info
    st.text(f"Current time: {datetime.now()}")
    st.text("Management Center - Minimal Mode")
    st.info("This is a simplified interface. Full features will be added as the system stabilizes.")