"""
UI Components and styling for SWT TMS Hub
"""
import streamlit as st
import os
from pathlib import Path

# Global CSS styling
GLOBAL_CSS = """
<style>
    /* Main theme colors */
    :root {
        --primary-color: #1f4e79;
        --secondary-color: #2c5aa0;
        --accent-color: #ff6b35;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --dark-color: #343a40;
        --light-color: #f8f9fa;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid var(--primary-color);
    }
    
    .status-new { background-color: #e3f2fd; color: #1976d2; }
    .status-assigned { background-color: #fff3e0; color: #f57c00; }
    .status-dispatched { background-color: #e8f5e8; color: #388e3c; }
    .status-in-transit { background-color: #f3e5f5; color: #7b1fa2; }
    .status-delivered { background-color: #e0f2f1; color: #00695c; }
    .status-cancelled { background-color: #ffebee; color: #d32f2f; }
    
    .data-protection-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        padding: 10px;
        z-index: 999;
        font-size: 12px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 5px;
        border: none;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        font-weight: bold;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
"""

def apply_global_styles():
    """Apply global CSS styles"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def show_header(title, subtitle=None):
    """Display formatted header"""
    st.markdown(f"""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">{title}</h1>
        {f'<p style="color: #e0e0e0; margin: 0.5rem 0 0 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Display sidebar with navigation and user info"""
    with st.sidebar:
        # Logo
        logo_path = Path(__file__).parent.parent / "assets" / "logos" / "swt_logo_white.png"
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
        else:
            st.markdown("## 🚚 SWT TMS")
        
        st.divider()
        
        # User info
        user_name = st.session_state.get('full_name', 'Unknown User')
        user_role = st.session_state.get('role', 'user')
        
        st.markdown(f"👤 **User:** {user_name}")
        
        if user_role == 'super_user':
            st.markdown("👑 **Role:** Super User")
        elif user_role == 'ceo':
            st.markdown("👑 **Role:** CEO")
        else:
            st.markdown(f"📋 **Role:** {user_role.title()}")
        
        st.divider()
        
        # Navigation menu based on user role
        navigation_menu = get_navigation_menu(user_role)
        
        selected_page = st.radio(
            "Navigation",
            list(navigation_menu.keys()),
            format_func=lambda x: f"{navigation_menu[x]} {x}"
        )
        
        st.session_state['current_view'] = selected_page.lower().replace(' ', '_')
        
        st.divider()
        
        # Quick actions
        st.markdown("### Quick Actions")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            from modules.auth import logout
            logout()
            st.rerun()

def get_navigation_menu(user_role):
    """Get navigation menu based on user role"""
    base_menu = {
        "Dashboard": "📊",
        "Shipments": "📦",
        "Dispatch": "🚚",
        "Billing": "💰",
        "Reports": "📈"
    }
    
    if user_role in ['super_user', 'ceo']:
        base_menu.update({
            "User Management": "👥",
            "System Settings": "⚙️"
        })
    elif user_role == 'admin':
        base_menu.update({
            "User Management": "👥"
        })
    
    return base_menu

def show_metric_card(title, value, delta=None, delta_color="normal"):
    """Display a metric card"""
    delta_html = ""
    if delta:
        color = "green" if delta_color == "normal" else "red"
        delta_html = f'<p style="color: {color}; margin: 0; font-size: 14px;">{delta}</p>'
    
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="margin: 0; color: var(--primary-color);">{title}</h3>
        <h2 style="margin: 0.5rem 0;">{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def show_status_badge(status):
    """Display a status badge"""
    status_lower = status.lower().replace(' ', '-')
    return f'<span class="status-{status_lower}" style="padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">{status}</span>'

def show_data_table(data, title=None, export_name=None):
    """Display a formatted data table with export option"""
    if title:
        st.subheader(title)
    
    if not data.empty:
        st.dataframe(data, use_container_width=True, hide_index=True)
        
        if export_name:
            csv = data.to_csv(index=False)
            st.download_button(
                "📥 Export to CSV",
                csv,
                f"{export_name}.csv",
                "text/csv",
                key=f"export_{export_name}"
            )
    else:
        st.info("No data available")

def show_confirmation_dialog(message, key):
    """Show a confirmation dialog"""
    st.warning(message)
    return st.checkbox("I confirm this action", key=key)

def show_loading_spinner(text="Loading..."):
    """Show loading spinner"""
    with st.spinner(text):
        return True

def format_currency(amount):
    """Format currency display"""
    return f"${amount:,.2f}" if amount else "$0.00"

def format_date(date_obj):
    """Format date display"""
    if date_obj:
        return date_obj.strftime("%m/%d/%Y")
    return "N/A"

def show_page_header(title, description=None):
    """Show page header with title and optional description"""
    st.title(title)
    if description:
        st.markdown(f"*{description}*")
    st.markdown("---")

def show_success_message(message):
    """Show success message"""
    st.success(f"✅ {message}")

def show_error_message(message):
    """Show error message"""
    st.error(f"❌ {message}")

def show_warning_message(message):
    """Show warning message"""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Show info message"""
    st.info(f"ℹ️ {message}")