"""
===================================================================
SMITH & WILLIAMS TRUCKING - TMS HUB
Main Application Entry Point - Refactored and Organized
===================================================================
Version: 2.0.0
Created: 2025-08-18
Company: Smith & Williams Trucking LLC
Author: Refactored by Claude for better organization and persistence

Professional Transportation Management System with comprehensive
shipment tracking, route optimization, and freight billing.
===================================================================
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import modules
from config.database import init_database
from modules.auth import show_login, check_authentication, logout
from modules.ui_components import apply_global_styles, show_sidebar
from views.executive import show_executive_view
from views.data_entry import show_data_feeder_view
from views.driver import show_driver_view
from views.user_management import show_user_management

# Page Configuration
st.set_page_config(
    page_title="TMS Hub - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Version and Company Info
APP_VERSION = "2.0.0"
COMPANY_NAME = "Smith & Williams Trucking LLC"

def initialize_app():
    """Initialize application and database"""
    if "app_initialized" not in st.session_state:
        try:
            # Initialize database with persistent storage
            init_database()
            st.session_state["app_initialized"] = True
        except Exception as e:
            st.error(f"❌ Database initialization failed: {str(e)}")
            st.stop()

def main():
    """Main application entry point"""
    
    # Apply global styling
    apply_global_styles()
    
    # Initialize app
    initialize_app()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not check_authentication():
        show_login()
    else:
        show_main_interface()

def show_main_interface():
    """Display the main interface based on user role"""
    
    # Show sidebar navigation
    show_sidebar()
    
    # Get current view from session state
    current_view = st.session_state.get('current_view', 'dashboard')
    user_role = st.session_state.get('role', 'user')
    
    # Route to appropriate view based on selection
    if current_view == 'dashboard':
        show_executive_view()
    elif current_view == 'shipments':
        show_shipments_view()
    elif current_view == 'data_entry' or current_view == 'data_feeder':
        show_data_feeder_view()
    elif current_view == 'dispatch':
        show_dispatch_view()
    elif current_view == 'billing':
        show_billing_view()
    elif current_view == 'reports':
        show_reports_view()
    elif current_view == 'driver':
        show_driver_view()
    elif current_view == 'user_management' and user_role in ['super_user', 'ceo', 'admin']:
        show_user_management()
    elif current_view == 'system_settings' and user_role in ['super_user', 'ceo']:
        show_system_settings()
    else:
        # Default to dashboard
        show_executive_view()

def show_shipments_view():
    """Import and show shipments management"""
    try:
        from views.shipments import show_shipment_management
        show_shipment_management()
    except ImportError:
        st.error("Shipments module not yet implemented. Using legacy code.")
        # Fallback to basic implementation
        st.title("📦 Shipment Management")
        st.info("This module is being refactored. Please use the Data Entry tab for now.")

def show_dispatch_view():
    """Import and show dispatch management"""
    try:
        from views.dispatch import show_dispatch_management
        show_dispatch_management()
    except ImportError:
        st.error("Dispatch module not yet implemented. Using legacy code.")
        st.title("🚚 Dispatch Management")
        st.info("This module is being refactored. Please check back soon.")

def show_billing_view():
    """Import and show billing management"""
    try:
        from views.billing import show_billing_management
        show_billing_management()
    except ImportError:
        st.error("Billing module not yet implemented. Using legacy code.")
        st.title("💰 Billing & Invoicing")
        st.info("This module is being refactored. Please check back soon.")

def show_reports_view():
    """Import and show reports"""
    try:
        from views.reports import show_reports_dashboard
        show_reports_dashboard()
    except ImportError:
        st.error("Reports module not yet implemented. Using legacy code.")
        st.title("📈 Reports & Analytics")
        st.info("This module is being refactored. Please check back soon.")

def show_system_settings():
    """Import and show system settings"""
    try:
        from views.settings import show_system_settings
        show_system_settings()
    except ImportError:
        st.error("Settings module not yet implemented. Using legacy code.")
        st.title("⚙️ System Settings")
        st.info("This module is being refactored. Please check back soon.")

# Error handling
def handle_error(error):
    """Global error handler"""
    st.error(f"An error occurred: {str(error)}")
    st.info("Please refresh the page or contact system administrator.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        handle_error(e)