"""
UI Components Module for Smith & Williams Trucking TMS
"""
import streamlit as st
from datetime import datetime

def apply_global_styles():
    """Apply Smith & Williams red/black/white theme globally"""
    st.markdown("""
    <style>
        /* Smith & Williams Trucking - Global Theme */
        
        /* Main app background */
        .main {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            padding: 0;
        }
        
        .stApp {
            background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
            background-attachment: fixed;
        }
        
        /* Headers - Red */
        h1, h2, h3, h4, h5, h6 {
            color: #DC2626 !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: 700;
        }
        
        /* Sidebar - Black gradient */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%);
            border-right: 3px solid #DC2626;
        }
        
        section[data-testid="stSidebar"] .stMarkdown {
            color: white;
        }
        
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #DC2626 !important;
        }
        
        /* Buttons - Red gradient */
        .stButton > button {
            background: linear-gradient(135deg, #DC2626 0%, #8B0000 100%);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #8B0000 0%, #DC2626 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        }
        
        /* Tabs - Red accent */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: rgba(0, 0, 0, 0.2);
            padding: 5px;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.9);
            color: #000000;
            border-radius: 5px;
            font-weight: 600;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background-color: #DC2626 !important;
            color: white !important;
        }
        
        /* Metrics - White cards with red accents */
        [data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #DC2626;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(220, 38, 38, 0.2);
        }
        
        [data-testid="metric-container"] [data-testid="metric-label"] {
            color: #8B0000;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            color: #000000;
            font-weight: 700;
        }
        
        /* Input fields */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
            background-color: rgba(255, 255, 255, 0.95);
            border: 2px solid #DC2626;
            border-radius: 5px;
            color: #000000;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #8B0000;
            box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.2);
        }
        
        /* Dataframes/Tables */
        .dataframe {
            background-color: white !important;
            color: black !important;
        }
        
        .dataframe thead th {
            background: #DC2626 !important;
            color: white !important;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.85rem;
        }
        
        .dataframe tbody tr:hover {
            background-color: rgba(220, 38, 38, 0.1) !important;
        }
        
        /* Expanders */
        .streamlit-expanderHeader {
            background-color: rgba(220, 38, 38, 0.1);
            border: 1px solid #DC2626;
            border-radius: 5px;
            color: #DC2626;
            font-weight: 600;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: rgba(220, 38, 38, 0.2);
        }
        
        /* Success/Error/Warning/Info boxes */
        .stAlert {
            border-radius: 5px;
            border-left: 5px solid;
        }
        
        div[data-baseweb="notification"] {
            border-radius: 5px;
        }
        
        /* Cards and containers */
        .element-container {
            border-radius: 10px;
        }
        
        /* Custom card styling */
        .custom-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 1.5rem;
            border-radius: 10px;
            border: 2px solid #DC2626;
            box-shadow: 0 4px 8px rgba(220, 38, 38, 0.2);
            margin-bottom: 1rem;
        }
        
        /* Progress bars */
        .stProgress > div > div {
            background-color: #DC2626;
        }
        
        /* Sliders */
        .stSlider > div > div > div {
            background-color: #DC2626;
        }
        
        /* Radio buttons and checkboxes */
        .stRadio > label,
        .stCheckbox > label {
            color: white !important;
        }
        
        /* Download button special styling */
        .stDownloadButton > button {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }
        
        .stDownloadButton > button:hover {
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        }
        
        /* Form submit button */
        div[data-testid="stForm"] button[type="submit"] {
            background: linear-gradient(135deg, #DC2626 0%, #8B0000 100%);
            color: white;
            font-weight: 700;
            text-transform: uppercase;
        }
        
        /* Vernon Protection Badge */
        .vernon-protection {
            position: fixed;
            bottom: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.8);
            color: #DC2626;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            border: 1px solid #DC2626;
            z-index: 9999;
        }
    </style>
    
    <div class="vernon-protection">
        🔒 VERNON PROTECTED
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Display sidebar with navigation and user info"""
    with st.sidebar:
        # Company branding
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: rgba(220, 38, 38, 0.1); border-radius: 10px; margin-bottom: 1rem;'>
            <h2 style='margin: 0; color: #DC2626;'>🚚 SWT</h2>
            <p style='margin: 0; color: white; font-size: 0.9rem;'>Smith & Williams Trucking</p>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        if 'user_full_name' in st.session_state:
            st.markdown(f"""
            <div style='background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;'>
                <p style='color: white; margin: 0; font-size: 0.9rem;'>👤 <strong>{st.session_state.user_full_name}</strong></p>
                <p style='color: #DC2626; margin: 0; font-size: 0.8rem; text-transform: uppercase;'>{st.session_state.role}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation based on role
        st.markdown("### 📍 Navigation")
        
        role = st.session_state.get('role', 'guest')
        
        if role in ['super_user', 'executive', 'admin']:
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_view = 'executive'
                st.rerun()
        
        if role in ['super_user', 'data_feeder', 'admin']:
            if st.button("📝 Data Entry", use_container_width=True):
                st.session_state.current_view = 'data_feeder'
                st.rerun()
        
        if role in ['super_user', 'driver']:
            if st.button("🚛 Driver Portal", use_container_width=True):
                st.session_state.current_view = 'driver'
                st.rerun()
        
        st.markdown("---")
        
        # System info
        st.markdown("### ⚙️ System")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Status", "Online", delta=None)
        with col2:
            st.metric("Time", datetime.now().strftime("%H:%M"))
        
        # Logout button
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            from modules.auth import logout
            logout()
        
        # Footer
        st.markdown("""
        <div style='position: absolute; bottom: 10px; left: 10px; right: 10px;'>
            <p style='color: #DC2626; font-size: 10px; text-align: center; margin: 0;'>
                Vernon Security Enabled
            </p>
            <p style='color: white; font-size: 9px; text-align: center; margin: 0;'>
                © 2025 SWT LLC
            </p>
        </div>
        """, unsafe_allow_html=True)

def create_metric_card(title, value, delta=None, delta_color="normal"):
    """Create a custom metric card with Smith & Williams styling"""
    delta_html = ""
    if delta is not None:
        color = "#10b981" if delta_color == "normal" else "#ef4444"
        delta_html = f"<p style='color: {color}; font-size: 0.9rem; margin: 0;'>{delta}</p>"
    
    return f"""
    <div class='custom-card'>
        <h4 style='color: #8B0000; margin: 0; font-size: 0.9rem; text-transform: uppercase;'>{title}</h4>
        <h2 style='color: #000000; margin: 0.5rem 0;'>{value}</h2>
        {delta_html}
    </div>
    """

def show_data_protection_footer():
    """Display Vernon data protection footer"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 2px solid #DC2626; background: rgba(255, 255, 255, 0.95);'>
        <p style='color: #DC2626; font-size: 12px; font-weight: 600; letter-spacing: 1px; margin: 0;'>
            🔒 DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER
        </p>
        <p style='color: #666; font-size: 10px; margin-top: 5px;'>
            © 2025 Smith & Williams Trucking LLC - Professional Fleet Management Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)