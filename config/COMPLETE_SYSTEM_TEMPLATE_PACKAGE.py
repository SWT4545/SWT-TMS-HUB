"""
Complete System Template Package for SWT TMS Hub
Contains company information, styling, and reusable components
"""

# Company Information
COMPANY_INFO = {
    "name": "Smith & Williams Trucking LLC",
    "address": "7600 N 15th St Suite 150, Phoenix, AZ 85020",
    "phone": "(951) 437-5474",
    "email": "Dispatch@smithwilliamstrucking.com",
    "website": "www.smithwilliamstrucking.com",
    "dot_number": "3675217",
    "mc_number": "1276006",
    "logo_path": "assets/logos/swt_logo.png"
}

# Global CSS Styling
GLOBAL_CSS = """
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* CSS Variables */
    :root {
        --primary-color: #1f4e79;
        --primary-light: #2c5aa0;
        --primary-dark: #1a3f63;
        --secondary-color: #ff6b35;
        --accent-color: #ffd700;
        --success-color: #28a745;
        --warning-color: #ffc107;
        --danger-color: #dc3545;
        --info-color: #17a2b8;
        --dark-color: #343a40;
        --light-color: #f8f9fa;
        --white: #ffffff;
        --border-radius: 8px;
        --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        --transition: all 0.3s ease;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Global App Styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Main Content Area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: var(--primary-color);
    }
    
    /* Cards and Containers */
    .metric-card {
        background: var(--white);
        padding: 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--box-shadow);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
        transition: var(--transition);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Status Badges */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-new { background-color: #e3f2fd; color: #1976d2; }
    .status-assigned { background-color: #fff3e0; color: #f57c00; }
    .status-dispatched { background-color: #e8f5e8; color: #388e3c; }
    .status-in-transit { background-color: #f3e5f5; color: #7b1fa2; }
    .status-delivered { background-color: #e0f2f1; color: #00695c; }
    .status-cancelled { background-color: #ffebee; color: #d32f2f; }
    .status-on-hold { background-color: #fff8e1; color: #f9a825; }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--primary-color), var(--primary-light));
    }
    
    .css-1d391kg .css-1v0mbdj {
        border-radius: var(--border-radius);
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: var(--border-radius);
        border: none;
        background: linear-gradient(45deg, var(--primary-color), var(--primary-light));
        color: var(--white);
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        transition: var(--transition);
        padding: 0.5rem 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(31, 78, 121, 0.3);
        background: linear-gradient(45deg, var(--primary-dark), var(--primary-color));
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border-radius: var(--border-radius);
        border: 2px solid #e0e0e0;
        font-family: 'Inter', sans-serif;
        transition: var(--transition);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(31, 78, 121, 0.1);
    }
    
    /* Data Tables */
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: var(--box-shadow);
    }
    
    /* Alert Messages */
    .alert-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    .alert-error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    .alert-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    .alert-info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
        padding: 1rem;
        border-radius: var(--border-radius);
        margin: 1rem 0;
    }
    
    /* Security Footer */
    .data-protection-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.9);
        color: var(--white);
        text-align: center;
        padding: 10px;
        z-index: 999;
        font-size: 11px;
        font-family: 'Inter', sans-serif;
        backdrop-filter: blur(10px);
    }
    
    /* Loading Animations */
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid var(--primary-color);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-dark);
    }
</style>
"""

# Security Branding for Vernon Protection
SECURITY_BRANDING = {
    "message": "🔒 VERNON PROTECTION ACTIVE - All data is secured and monitored",
    "color": "#00ff41",
    "font_size": "11px",
    "font_weight": "600",
    "letter_spacing": "1px"
}

# Reusable Components
class ReusableComponents:
    
    @staticmethod
    def get_status_badge(status):
        """Generate status badge HTML"""
        status_lower = status.lower().replace(' ', '-')
        return f'<span class="status-badge status-{status_lower}">{status}</span>'
    
    @staticmethod
    def get_metric_card(title, value, delta=None, icon=None):
        """Generate metric card HTML"""
        delta_html = ""
        if delta:
            delta_color = "green" if "+" in str(delta) else "red"
            delta_html = f'<p style="color: {delta_color}; margin: 0.5rem 0 0 0; font-size: 14px; font-weight: 500;">{delta}</p>'
        
        icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ""
        
        return f"""
        <div class="metric-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                {icon_html}
                <h4 style="margin: 0; color: var(--primary-color); font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">{title}</h4>
            </div>
            <h2 style="margin: 0; font-size: 2rem; font-weight: 700; color: var(--dark-color);">{value}</h2>
            {delta_html}
        </div>
        """
    
    @staticmethod
    def get_alert_box(message, alert_type="info"):
        """Generate alert box HTML"""
        icons = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️"
        }
        
        icon = icons.get(alert_type, "ℹ️")
        
        return f"""
        <div class="alert-{alert_type}">
            <strong>{icon} {message}</strong>
        </div>
        """
    
    @staticmethod
    def get_page_header(title, subtitle=None, icon=None):
        """Generate page header HTML"""
        icon_html = f'<span style="margin-right: 1rem; font-size: 2.5rem;">{icon}</span>' if icon else ""
        subtitle_html = f'<p style="color: #666; margin: 0.5rem 0 0 0; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ""
        
        return f"""
        <div style="background: var(--white); padding: 2rem; border-radius: var(--border-radius); 
                    box-shadow: var(--box-shadow); margin-bottom: 2rem; 
                    border-left: 5px solid var(--primary-color);">
            <div style="display: flex; align-items: center;">
                {icon_html}
                <div>
                    <h1 style="margin: 0; color: var(--primary-color); font-size: 2.5rem;">{title}</h1>
                    {subtitle_html}
                </div>
            </div>
        </div>
        """

# Application Configuration
APP_CONFIG = {
    "version": "2.0.0",
    "company": COMPANY_INFO["name"],
    "theme": {
        "primary_color": "#1f4e79",
        "secondary_color": "#ff6b35",
        "background_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    },
    "features": {
        "gps_tracking": True,
        "email_notifications": True,
        "sms_alerts": False,
        "customer_portal": False,
        "api_access": False
    },
    "database": {
        "type": "sqlite",
        "auto_backup": True,
        "backup_interval": 24  # hours
    }
}