"""
User Management View for SWT TMS Hub
"""
import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
from config.database import get_connection
from modules.ui_components import show_page_header, show_success_message, show_error_message
from modules.auth import require_role

@require_role(['super_user', 'ceo', 'admin'])
def show_user_management():
    """Display user management interface"""
    show_page_header(
        "👥 User Management", 
        "Manage system users, roles, and permissions"
    )
    
    tabs = st.tabs(["👀 View Users", "➕ Create User", "✏️ Edit User", "🔐 Permissions", "📊 Activity Log"])
    
    with tabs[0]:
        show_users_list()
    
    with tabs[1]:
        show_create_user()
    
    with tabs[2]:
        show_edit_user()
    
    with tabs[3]:
        show_permissions_matrix()
    
    with tabs[4]:
        show_activity_log()

def show_users_list():
    """Display list of all users"""
    st.subheader("All System Users")
    
    conn = get_connection()
    users = pd.read_sql_query("""
        SELECT id, username, full_name, role, email, phone, 
               is_active, last_login, created_at
        FROM users
        ORDER BY role, username
    """, conn)
    
    if not users.empty:
        # User statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", len(users))
        
        with col2:
            active_count = len(users[users['is_active'] == 1])
            st.metric("Active Users", active_count)
        
        with col3:
            admin_count = len(users[users['role'].isin(['super_user', 'ceo', 'admin'])])
            st.metric("Admin Users", admin_count)
        
        with col4:
            driver_count = len(users[users['role'] == 'driver'])
            st.metric("Drivers", driver_count)
        
        st.markdown("---")
        
        # Display users by role
        roles = ['super_user', 'ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting']
        
        for role in roles:
            role_users = users[users['role'] == role]
            if not role_users.empty:
                st.markdown(f"#### {role.replace('_', ' ').title()} Users ({len(role_users)})")
                
                display_columns = ['username', 'full_name', 'email', 'phone', 'is_active', 'last_login']
                formatted_users = role_users[display_columns].copy()
                
                # Format the display
                formatted_users['is_active'] = formatted_users['is_active'].map({1: '✅ Active', 0: '❌ Inactive'})
                formatted_users['last_login'] = pd.to_datetime(formatted_users['last_login']).dt.strftime('%Y-%m-%d %H:%M')
                
                st.dataframe(formatted_users, use_container_width=True, hide_index=True)
                st.markdown("")
    else:
        st.info("No users found in the system")
    
    conn.close()

def show_create_user():
    """Create new user form"""
    st.subheader("Create New User")
    
    # Check permissions
    current_role = st.session_state.get('role')
    if current_role not in ['super_user', 'ceo']:
        st.error("❌ Only Super Users and CEOs can create new users")
        return
    
    with st.form("create_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### User Information")
            username = st.text_input("Username*", placeholder="Enter unique username")
            password = st.text_input("Password*", type="password", placeholder="Enter secure password")
            confirm_password = st.text_input("Confirm Password*", type="password")
            full_name = st.text_input("Full Name*", placeholder="First Last")
            
            # Role selection
            available_roles = ['admin', 'dispatcher', 'driver', 'customer', 'accounting']
            if current_role == 'super_user':
                available_roles.insert(0, 'ceo')
            
            role = st.selectbox("Role*", available_roles)
        
        with col2:
            st.markdown("##### Contact Information")
            email = st.text_input("Email", placeholder="user@company.com")
            phone = st.text_input("Phone", placeholder="(XXX) XXX-XXXX")
            
            st.markdown("##### Settings")
            is_active = st.checkbox("Active User", value=True)
            
            # Role description
            role_descriptions = {
                'ceo': "Full system access including user management",
                'admin': "Full operational access, no user management",
                'dispatcher': "Manage shipments, dispatch, and operations",
                'driver': "View assigned loads and update status",
                'customer': "View own shipments and invoices",
                'accounting': "Manage billing, invoices, and financial reports"
            }
            
            st.info(f"**{role.title()} Role:** {role_descriptions.get(role, 'Standard user access')}")
        
        submitted = st.form_submit_button("👤 Create User", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([username, password, full_name]):
                show_error_message("Username, Password, and Full Name are required")
            elif password != confirm_password:
                show_error_message("Passwords do not match")
            elif len(password) < 6:
                show_error_message("Password must be at least 6 characters long")
            else:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    # Check if username exists
                    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
                    if cursor.fetchone()[0] > 0:
                        show_error_message("Username already exists")
                    else:
                        # Create user
                        password_hash = hashlib.sha256(password.encode()).hexdigest()
                        cursor.execute("""INSERT INTO users 
                            (username, password_hash, role, full_name, email, phone, is_active, created_by)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                            (username, password_hash, role, full_name, email, phone, 
                             1 if is_active else 0, st.session_state.get('user_id')))
                        conn.commit()
                        
                        show_success_message(f"User '{username}' created successfully!")
                        st.balloons()
                        
                    conn.close()
                    
                except Exception as e:
                    show_error_message(f"Error creating user: {str(e)}")

def show_edit_user():
    """Edit existing user"""
    st.subheader("Edit User")
    
    conn = get_connection()
    
    # Get users (exclude super_user from editing unless current user is super_user)
    current_role = st.session_state.get('role')
    if current_role == 'super_user':
        users_query = "SELECT id, username, full_name, role, email, phone, is_active FROM users WHERE username != ? ORDER BY username"
        users = pd.read_sql_query(users_query, conn, params=(st.session_state.get('username'),))
    else:
        users_query = "SELECT id, username, full_name, role, email, phone, is_active FROM users WHERE role NOT IN ('super_user', 'ceo') ORDER BY username"
        users = pd.read_sql_query(users_query, conn)
    
    if not users.empty:
        # Select user to edit
        user_options = {}
        for _, user in users.iterrows():
            display_name = f"{user['username']} ({user['full_name']} - {user['role']})"
            user_options[display_name] = user['id']
        
        selected_user_display = st.selectbox("Select User to Edit", options=list(user_options.keys()))
        selected_user_id = user_options[selected_user_display]
        
        # Get selected user details
        selected_user = users[users['id'] == selected_user_id].iloc[0]
        
        # Edit form
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("##### Basic Information")
            new_full_name = st.text_input("Full Name", value=selected_user['full_name'])
            new_email = st.text_input("Email", value=selected_user['email'] or "")
            new_phone = st.text_input("Phone", value=selected_user['phone'] or "")
        
        with col2:
            st.markdown("##### Role & Status")
            
            # Role selection based on current user permissions
            if current_role == 'super_user':
                role_options = ['ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting']
            else:
                role_options = ['admin', 'dispatcher', 'driver', 'customer', 'accounting']
            
            current_role_index = role_options.index(selected_user['role']) if selected_user['role'] in role_options else 0
            new_role = st.selectbox("Role", options=role_options, index=current_role_index)
            
            new_status = st.selectbox("Status", options=["Active", "Inactive"], 
                                    index=0 if selected_user['is_active'] else 1)
        
        with col3:
            st.markdown("##### Actions")
            
            if st.button("💾 Update User", type="primary", use_container_width=True):
                try:
                    cursor = conn.cursor()
                    cursor.execute("""UPDATE users 
                        SET full_name = ?, email = ?, phone = ?, role = ?, is_active = ?
                        WHERE id = ?""",
                        (new_full_name, new_email, new_phone, new_role, 
                         1 if new_status == "Active" else 0, selected_user_id))
                    conn.commit()
                    show_success_message("User updated successfully!")
                    st.rerun()
                except Exception as e:
                    show_error_message(f"Error updating user: {str(e)}")
            
            if st.button("🔄 Reset Password", use_container_width=True):
                temp_password = f"temp{datetime.now().strftime('%H%M')}"
                password_hash = hashlib.sha256(temp_password.encode()).hexdigest()
                
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                                 (password_hash, selected_user_id))
                    conn.commit()
                    st.success(f"🔑 Password reset to: **{temp_password}**")
                    st.warning("⚠️ User should change this password immediately!")
                except Exception as e:
                    show_error_message(f"Error resetting password: {str(e)}")
            
            # Delete user (only for super_user)
            if current_role == 'super_user':
                st.markdown("---")
                if st.button("🗑️ Delete User", type="secondary", use_container_width=True):
                    if st.checkbox("⚠️ Confirm deletion", key="confirm_delete"):
                        try:
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM users WHERE id = ?", (selected_user_id,))
                            conn.commit()
                            show_success_message("User deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            show_error_message(f"Error deleting user: {str(e)}")
    else:
        st.info("No users available to edit")
    
    conn.close()

def show_permissions_matrix():
    """Display role permissions matrix"""
    st.subheader("Role Permissions Matrix")
    
    st.markdown("""
    ### System Access by Role
    
    | Feature | Super User | CEO | Admin | Dispatcher | Driver | Customer | Accounting |
    |---------|------------|-----|-------|------------|--------|----------|------------|
    | **Dashboard** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Limited | ✅ Limited | ✅ Full |
    | **Shipments** | ✅ All | ✅ All | ✅ All | ✅ All | 👁️ Assigned | 👁️ Own Only | 👁️ View |
    | **Data Entry** | ✅ All | ✅ All | ✅ All | ✅ All | ❌ | ❌ | ❌ |
    | **Dispatch** | ✅ All | ✅ All | ✅ All | ✅ All | 👁️ Assigned | ❌ | ❌ |
    | **Billing** | ✅ All | ✅ All | ✅ All | 👁️ View | ❌ | 👁️ Own Only | ✅ All |
    | **Reports** | ✅ All | ✅ All | ✅ All | ✅ Operational | 👁️ Own | 👁️ Own | ✅ Financial |
    | **User Management** | ✅ All | ✅ All | ✅ Limited | ❌ | ❌ | ❌ | ❌ |
    | **System Settings** | ✅ All | ✅ All | ❌ | ❌ | ❌ | ❌ | ❌ |
    
    **Legend:**
    - ✅ **Full Access** - Complete read/write access
    - 👁️ **Limited Access** - Read-only or restricted scope
    - ❌ **No Access** - Feature not available
    
    ### Role Descriptions
    
    **Super User:** Complete system administration including user management and system settings
    
    **CEO:** Full business access with user management capabilities
    
    **Admin:** Full operational access without user management
    
    **Dispatcher:** Complete shipment and dispatch management
    
    **Driver:** View assigned loads and update delivery status
    
    **Customer:** View own shipments and invoices
    
    **Accounting:** Manage billing, invoices, and financial reporting
    """)

def show_activity_log():
    """Display user activity log"""
    st.subheader("User Activity Log")
    
    conn = get_connection()
    
    # Recent login activity
    activity = pd.read_sql_query("""
        SELECT username, full_name, role, last_login, is_active
        FROM users
        WHERE last_login IS NOT NULL
        ORDER BY last_login DESC
        LIMIT 50
    """, conn)
    
    if not activity.empty:
        st.markdown("#### Recent Login Activity")
        
        # Format the activity data
        formatted_activity = activity.copy()
        formatted_activity['last_login'] = pd.to_datetime(formatted_activity['last_login']).dt.strftime('%Y-%m-%d %H:%M:%S')
        formatted_activity['is_active'] = formatted_activity['is_active'].map({1: '✅ Active', 0: '❌ Inactive'})
        formatted_activity = formatted_activity.rename(columns={
            'username': 'Username',
            'full_name': 'Full Name',
            'role': 'Role',
            'last_login': 'Last Login',
            'is_active': 'Status'
        })
        
        st.dataframe(formatted_activity, use_container_width=True, hide_index=True)
        
        # Export activity log
        csv = formatted_activity.to_csv(index=False)
        st.download_button(
            "📥 Export Activity Log",
            csv,
            f"user_activity_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.info("No user activity logged yet")
    
    # System statistics
    st.markdown("#### System Statistics")
    
    stats = pd.read_sql_query("""
        SELECT 
            role,
            COUNT(*) as total_users,
            SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_users,
            SUM(CASE WHEN last_login IS NOT NULL THEN 1 ELSE 0 END) as users_with_logins
        FROM users
        GROUP BY role
        ORDER BY total_users DESC
    """, conn)
    
    if not stats.empty:
        st.dataframe(stats, use_container_width=True, hide_index=True)
    
    conn.close()