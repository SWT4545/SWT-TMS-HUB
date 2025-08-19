"""
UI Components Module for Smith & Williams Trucking TMS
"""
import streamlit as st
from datetime import datetime

def apply_global_styles():
    """Apply Smith & Williams red/black/white theme globally"""
    st.markdown("""
    <style>
        /* Hide Streamlit header */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        
        /* Hide/Minimize Streamlit's "Manage app" button in bottom right */
        .stDeployButton {
            display: none !important;
        }
        
        /* Alternative: If you want to keep it but make it smaller/less intrusive */
        button[kind="header"] {
            display: none !important;
        }
        
        /* Hide the Streamlit menu button */
        #MainMenu {
            visibility: hidden !important;
        }
        
        /* Hide the Streamlit footer */
        footer {
            visibility: hidden !important;
        }
        
        /* Hide the Streamlit "Deploy" button specifically */
        [data-testid="manage-app-button"] {
            display: none !important;
        }
        
        /* Hide toolbar/menu items */
        .stToolbar {
            display: none !important;
        }
        
        /* Custom S&W header bar */
        .stApp::before {
            content: 'SMITH & WILLIAMS TRUCKING - TMS';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #8B0000;
            color: white;
            font-size: 24px;
            font-weight: 900;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            border-bottom: 3px solid #660000;
        }
        
        /* Main app - pure black background */
        .stApp {
            padding-top: 60px;
            background-color: #000000 !important;
        }
        
        /* Main container - black background with proper spacing */
        .main .block-container {
            background-color: #000000 !important;
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
            max-width: 100%;
        }
        
        /* Prevent text truncation */
        .element-container {
            overflow: visible !important;
        }
        
        /* Ensure no text overlap */
        div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 1rem;
        }
        
        /* Sidebar - black background with red accent */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            border-right: 3px solid #8B0000 !important;
        }
        
        /* Sidebar content - white text for visibility */
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] p, 
        section[data-testid="stSidebar"] span, 
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 600 !important;
            text-shadow: 1px 1px 2px rgba(139, 0, 0, 0.3) !important;
        }
        
        /* Sidebar headers - extra bold */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] h5,
        section[data-testid="stSidebar"] h6 {
            color: #ffffff !important;
            font-weight: 800 !important;
            text-shadow: 2px 2px 4px rgba(139, 0, 0, 0.5) !important;
        }
        
        /* Sidebar buttons - S&W red with clean borders */
        section[data-testid="stSidebar"] .stButton button {
            background-color: #8B0000 !important;
            color: white !important;
            border: 3px solid #ffffff !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            padding: 0.5rem 1rem !important;
            box-shadow: 0 2px 4px rgba(255, 255, 255, 0.2) !important;
        }
        
        section[data-testid="stSidebar"] .stButton button:hover {
            background-color: #A00000 !important;
            border: 3px solid #ffcccc !important;
            box-shadow: 0 4px 8px rgba(255, 255, 255, 0.4) !important;
        }
        
        /* Main area text - white on black */
        .stMarkdown, p, span, label, li {
            color: #ffffff !important;
            font-weight: 500 !important;
            text-shadow: 1px 1px 2px rgba(139, 0, 0, 0.3) !important;
        }
        
        /* Headers with S&W branding */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-weight: 700 !important;
            text-shadow: 2px 2px 4px rgba(139, 0, 0, 0.5) !important;
            border-bottom: 2px solid #8B0000 !important;
            padding-bottom: 10px !important;
            margin-bottom: 20px !important;
        }
        
        /* Metrics - black with red accent, white text, no truncation */
        div[data-testid="metric-container"] {
            background-color: #1a1a1a !important;
            border: 3px solid #8B0000 !important;
            border-radius: 10px !important;
            padding: 20px !important;
            box-shadow: 0 4px 6px rgba(139, 0, 0, 0.3) !important;
            min-width: 200px !important;
            overflow: visible !important;
        }
        
        /* Metric labels - white and visible */
        div[data-testid="metric-container"] label {
            color: #ffffff !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
            margin-bottom: 10px !important;
        }
        
        /* Metric values - large white text with no truncation */
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 2.5rem !important;
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            width: auto !important;
            min-width: fit-content !important;
        }
        
        /* Metric delta - green/red for positive/negative */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            color: #00ff00 !important;
            font-weight: 600 !important;
        }
        
        /* Buttons - S&W red style */
        .stButton button {
            background-color: #8B0000 !important;
            color: white !important;
            border: 2px solid #ffffff !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }
        
        .stButton button:hover {
            background-color: #A00000 !important;
            border: 2px solid #ffcccc !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(139, 0, 0, 0.5) !important;
        }
        
        /* Tabs - black with red underline */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #000000 !important;
            border-bottom: 3px solid #8B0000 !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #ffffff !important;
            font-weight: 600 !important;
            background-color: #1a1a1a !important;
            border-radius: 8px 8px 0 0 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #8B0000 !important;
            border: 2px solid #ffffff !important;
            border-bottom: none !important;
        }
        
        /* Input fields - black with red border */
        .stTextInput input, .stTextArea textarea, .stSelectbox select, .stNumberInput input {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #8B0000 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus, 
        .stSelectbox select:focus, .stNumberInput input:focus {
            border: 3px solid #ff0000 !important;
            box-shadow: 0 0 10px rgba(139, 0, 0, 0.5) !important;
        }
        
        /* Dataframes - black with red accents */
        .dataframe {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #8B0000 !important;
        }
        
        .dataframe th {
            background-color: #8B0000 !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
        }
        
        .dataframe td {
            background-color: #0a0a0a !important;
            color: #ffffff !important;
            border: 1px solid #333333 !important;
        }
        
        /* Expanders - black with red accent */
        .streamlit-expanderHeader {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #8B0000 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #2a2a2a !important;
            border: 2px solid #ff0000 !important;
        }
        
        /* Success/Error/Warning/Info messages */
        .stAlert {
            background-color: #1a1a1a !important;
            color: #ffffff !important;
            border: 2px solid #8B0000 !important;
            border-radius: 8px !important;
        }
        
        /* Vernon Protection Badge - Relocated to top right */
        .vernon-protection {
            position: fixed;
            top: 70px;
            right: 10px;
            background: #8B0000;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            border: 2px solid white;
            z-index: 99999;
            text-transform: uppercase;
        }
    </style>
    
    <div class="vernon-protection">
        🔒 VERNON PROTECTED
    </div>
    """, unsafe_allow_html=True)

def show_sidebar():
    """Display sidebar with navigation and user info"""
    from pathlib import Path
    
    with st.sidebar:
        # Display SWT Logo at top of sidebar
        logo_path = Path("assets/logos/swt_logo_white.png")
        if logo_path.exists():
            st.image(str(logo_path), use_container_width=True)
            st.markdown("---")
        else:
            # Fallback to text branding if logo not found
            st.markdown("""
            <div style='text-align: center; padding: 1rem; background: #8B0000; border-radius: 10px; margin-bottom: 1rem; border: 3px solid white;'>
                <h2 style='margin: 0; color: white; font-weight: 900;'>🚚 SWT</h2>
                <p style='margin: 0; color: white; font-size: 0.9rem; font-weight: 700;'>Smith & Williams Trucking</p>
            </div>
            """, unsafe_allow_html=True)
        
        # User info
        if 'user_full_name' in st.session_state:
            st.markdown(f"""
            <div style='background: #1a1a1a; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; border: 2px solid #8B0000;'>
                <p style='color: white; margin: 0; font-size: 0.9rem; font-weight: 600;'>👤 <strong>{st.session_state.user_full_name}</strong></p>
                <p style='color: #8B0000; margin: 0; font-size: 0.8rem; text-transform: uppercase; font-weight: 700;'>{st.session_state.role}</p>
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
            <p style='color: #8B0000; font-size: 10px; text-align: center; margin: 0; font-weight: 700;'>
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
        color = "#00ff00" if delta_color == "normal" else "#ff0000"
        delta_html = f"<p style='color: {color}; font-size: 0.9rem; margin: 0; font-weight: 600;'>{delta}</p>"
    
    return f"""
    <div style='background: #1a1a1a; padding: 1.5rem; border-radius: 10px; border: 3px solid #8B0000; box-shadow: 0 4px 6px rgba(139, 0, 0, 0.3);'>
        <h4 style='color: white; margin: 0; font-size: 0.9rem; text-transform: uppercase; font-weight: 700;'>{title}</h4>
        <h2 style='color: white; margin: 0.5rem 0; font-weight: 800;'>{value}</h2>
        {delta_html}
    </div>
    """

def show_data_protection_footer():
    """Display Vernon data protection footer"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem; margin-top: 3rem; border-top: 3px solid #8B0000; background: #000000;'>
        <p style='color: #8B0000; font-size: 12px; font-weight: 700; letter-spacing: 1px; margin: 0; text-transform: uppercase;'>
            🔒 DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER
        </p>
        <p style='color: white; font-size: 10px; margin-top: 5px; font-weight: 600;'>
            © 2025 Smith & Williams Trucking LLC - Professional Fleet Management Solutions
        </p>
    </div>
    """, unsafe_allow_html=True)