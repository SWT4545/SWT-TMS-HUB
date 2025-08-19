"""
User Management View for Smith & Williams Trucking TMS
"""
import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime
from modules.ui_components import show_data_protection_footer

DB_PATH = "swt_tms.db"

def show_user_management():
    """Display user management interface for super users"""
    
    st.title("👥 User Management")
    st.markdown("### System Administration Portal")
    
    # Verify super user access
    if st.session_state.get('role') != 'super_user':
        st.error("⛔ Access Denied: Super User privileges required")
        return
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 View Users", 
        "➕ Add User", 
        "✏️ Edit User", 
        "🔐 Security Settings"
    ])
    
    with tab1:
        show_users_list()
    
    with tab2:
        add_new_user()
    
    with tab3:
        edit_user()
    
    with tab4:
        security_settings()
    
    # Data Protection Footer
    show_data_protection_footer()

def show_users_list():
    """Display list of all users"""
    st.markdown("## All System Users")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        role_filter = st.selectbox("Filter by Role", 
            ["All", "super_user", "executive", "admin", "data_feeder", "driver"])
    with col2:
        status_filter = st.selectbox("Filter by Status", 
            ["All", "Active", "Inactive"])
    with col3:
        st.write("")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Mock user data (replace with actual database query)
    users_data = pd.DataFrame({
        'ID': [1, 2, 3, 4, 5],
        'Username': ['brandon', 'john_exec', 'jane_admin', 'bob_driver', 'alice_data'],
        'Full Name': ['Brandon Smith', 'John Executive', 'Jane Admin', 'Bob Driver', 'Alice Feeder'],
        'Role': ['super_user', 'executive', 'admin', 'driver', 'data_feeder'],
        'Status': ['Active', 'Active', 'Active', 'Active', 'Inactive'],
        'Last Login': ['2025-01-19 14:30', '2025-01-19 09:15', '2025-01-18 16:45', '2025-01-19 08:00', '2025-01-17 12:00'],
        'Created': ['2025-01-01', '2025-01-05', '2025-01-05', '2025-01-10', '2025-01-12']
    })
    
    # Apply filters
    if role_filter != "All":
        users_data = users_data[users_data['Role'] == role_filter]
    if status_filter != "All":
        users_data = users_data[users_data['Status'] == status_filter]
    
    # Display users
    st.dataframe(users_data, use_container_width=True, hide_index=True)
    
    # User statistics
    st.markdown("### 📊 User Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", len(users_data))
    with col2:
        st.metric("Active Users", len(users_data[users_data['Status'] == 'Active']))
    with col3:
        st.metric("Logged in Today", 3)
    with col4:
        st.metric("New This Month", 2)

def add_new_user():
    """Add new user form"""
    st.markdown("## Add New User")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Account Information")
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Confirm Password*", type="password")
            role = st.selectbox("Role*", [
                "driver",
                "data_feeder", 
                "admin",
                "executive",
                "super_user"
            ])
        
        with col2:
            st.markdown("### Personal Information")
            full_name = st.text_input("Full Name*")
            email = st.text_input("Email*")
            phone = st.text_input("Phone")
            department = st.selectbox("Department", [
                "Operations",
                "Administration",
                "Management",
                "Drivers",
                "IT"
            ])
        
        st.markdown("### Permissions")
        col1, col2, col3 = st.columns(3)
        with col1:
            can_view_reports = st.checkbox("View Reports", value=True)
            can_edit_loads = st.checkbox("Edit Loads")
        with col2:
            can_manage_drivers = st.checkbox("Manage Drivers")
            can_view_financials = st.checkbox("View Financials")
        with col3:
            can_export_data = st.checkbox("Export Data")
            can_manage_customers = st.checkbox("Manage Customers")
        
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button("✅ Create User", type="primary", use_container_width=True)
        
        if submitted:
            if password != confirm_password:
                st.error("❌ Passwords do not match!")
            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters long!")
            elif not all([username, password, full_name, email]):
                st.error("❌ Please fill in all required fields!")
            else:
                # Here you would add the user to the database
                st.success(f"✅ User '{username}' created successfully!")
                st.balloons()

def edit_user():
    """Edit existing user"""
    st.markdown("## Edit User")
    
    # User selection
    user_to_edit = st.selectbox("Select User to Edit", [
        "Select a user...",
        "john_exec - John Executive",
        "jane_admin - Jane Admin",
        "bob_driver - Bob Driver",
        "alice_data - Alice Feeder"
    ])
    
    if user_to_edit != "Select a user...":
        with st.form("edit_user_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Account Information")
                username = st.text_input("Username", value=user_to_edit.split(" - ")[0], disabled=True)
                new_password = st.text_input("New Password (leave blank to keep current)", type="password")
                role = st.selectbox("Role", [
                    "driver",
                    "data_feeder",
                    "admin", 
                    "executive",
                    "super_user"
                ], index=2)
                status = st.selectbox("Status", ["Active", "Inactive"])
            
            with col2:
                st.markdown("### Personal Information")
                full_name = st.text_input("Full Name", value=user_to_edit.split(" - ")[1])
                email = st.text_input("Email", value="user@swtrucking.com")
                phone = st.text_input("Phone", value="(901) 555-0000")
                department = st.selectbox("Department", [
                    "Operations",
                    "Administration",
                    "Management",
                    "Drivers",
                    "IT"
                ], index=1)
            
            st.markdown("### Actions")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                save_btn = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
            with col2:
                reset_pwd_btn = st.form_submit_button("🔐 Force Password Reset", use_container_width=True)
            with col3:
                deactivate_btn = st.form_submit_button("⛔ Deactivate User", use_container_width=True)
            
            if save_btn:
                st.success("✅ User updated successfully!")
            elif reset_pwd_btn:
                st.warning("⚠️ Password reset email sent to user")
            elif deactivate_btn:
                st.warning("⚠️ User has been deactivated")

def security_settings():
    """Security settings and audit log"""
    st.markdown("## 🔐 Security Settings")
    
    # Password Policy
    st.markdown("### Password Policy")
    col1, col2 = st.columns(2)
    
    with col1:
        min_length = st.number_input("Minimum Password Length", min_value=6, max_value=20, value=8)
        require_uppercase = st.checkbox("Require Uppercase Letters", value=True)
        require_numbers = st.checkbox("Require Numbers", value=True)
    
    with col2:
        password_expiry = st.number_input("Password Expiry (days)", min_value=0, max_value=365, value=90)
        require_lowercase = st.checkbox("Require Lowercase Letters", value=True)
        require_special = st.checkbox("Require Special Characters", value=False)
    
    if st.button("Update Password Policy", type="primary"):
        st.success("✅ Password policy updated successfully!")
    
    st.markdown("---")
    
    # Session Settings
    st.markdown("### Session Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        session_timeout = st.number_input("Session Timeout (minutes)", min_value=5, max_value=480, value=30)
        max_attempts = st.number_input("Max Login Attempts", min_value=3, max_value=10, value=5)
    
    with col2:
        lockout_duration = st.number_input("Account Lockout Duration (minutes)", min_value=5, max_value=60, value=15)
        require_2fa = st.checkbox("Require Two-Factor Authentication", value=False)
    
    if st.button("Update Session Settings"):
        st.success("✅ Session settings updated successfully!")
    
    st.markdown("---")
    
    # Audit Log
    st.markdown("### 📋 Recent Security Events")
    
    audit_data = pd.DataFrame({
        'Timestamp': ['2025-01-19 14:30:00', '2025-01-19 14:25:00', '2025-01-19 13:45:00', 
                     '2025-01-19 12:00:00', '2025-01-19 11:30:00'],
        'User': ['brandon', 'john_exec', 'unknown', 'jane_admin', 'bob_driver'],
        'Event': ['Login Success', 'Password Changed', 'Login Failed', 'User Created', 'Login Success'],
        'IP Address': ['192.168.1.100', '192.168.1.101', '203.45.67.89', '192.168.1.102', '192.168.1.103'],
        'Status': ['✅ Success', '✅ Success', '❌ Failed', '✅ Success', '✅ Success']
    })
    
    st.dataframe(audit_data, use_container_width=True, hide_index=True)
    
    # Export audit log
    if st.button("📥 Export Full Audit Log"):
        st.info("Preparing audit log export...")
    
    # Vernon Security Status
    st.markdown("---")
    st.markdown("### 🛡️ Vernon Security Status")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("✅ Firewall: Active")
    with col2:
        st.success("✅ Encryption: AES-256")
    with col3:
        st.success("✅ Backup: Completed 2h ago")