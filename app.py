"""
===================================================================
SMITH & WILLIAMS TRUCKING - TMS HUB
Main Application Entry Point
===================================================================
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from modules.auth import show_login, check_authentication
from modules.ui_components import apply_global_styles, show_sidebar
from views.user_management import show_user_management

# Import enhanced views
from views.executive_enhanced import show_executive_view
from views.data_feeder_enhanced import show_data_feeder_view  
from views.driver_enhanced import show_driver_view

# Initialize enhanced database
from modules.database_enhanced import init_enhanced_database
init_enhanced_database()

# Page Configuration
st.set_page_config(
    page_title="TMS - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
apply_global_styles()

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login()
    else:
        # Show main interface based on user role
        show_main_interface()

def show_main_interface():
    """Display the main interface based on user role"""
    
    # Show sidebar
    show_sidebar()
    
    # Check if user management should be shown
    if st.session_state.get('show_user_management', False) and st.session_state.role == 'super_user':
        show_user_management()
        
        # Add back button
        if st.button("⬅️ Back to Main View"):
            st.session_state.show_user_management = False
            st.rerun()
    else:
        # Main content area based on selected view
        current_view = st.session_state.get('current_view', 'executive')
        
        if current_view == 'executive':
            show_executive_view()
        elif current_view == 'data_feeder':
            show_data_feeder_view()
        elif current_view == 'driver':
            show_driver_view()
    
    # User Management button - Only for super_user
    if st.session_state.role == 'super_user':
        with st.sidebar:
            st.markdown("---")
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.show_user_management = True
                st.rerun()

if __name__ == "__main__":
    main()