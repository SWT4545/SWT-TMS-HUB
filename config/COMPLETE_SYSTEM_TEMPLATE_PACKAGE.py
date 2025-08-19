"""
===================================================================
COMPLETE SYSTEM TEMPLATE PACKAGE FOR SMITH & WILLIAMS TRUCKING LLC
===================================================================
Version: 1.0.0
Created: 2025-08-17
Company: Smith & Williams Trucking LLC
Author: Brandon Smith (Owner)

This comprehensive template package contains all the design elements,
company branding, code patterns, and lessons learned from building
the Trailer Fleet Management System. Use this as a foundation for
all future projects.

===================================================================
TABLE OF CONTENTS
===================================================================
1. COMPANY INFORMATION & BRANDING
2. VISUAL STYLING & CSS
3. LOGIN SYSTEM WITH VIDEO LOGO
4. DATABASE ARCHITECTURE
5. PDF GENERATION TEMPLATES
6. ERROR HANDLING PATTERNS
7. REUSABLE COMPONENTS
8. LESSONS LEARNED
9. BEST PRACTICES
10. QUICK START TEMPLATE
===================================================================
"""

# ===================================================================
# 1. COMPANY INFORMATION & BRANDING
# ===================================================================

COMPANY_INFO = {
    "name": "Smith & Williams Trucking LLC",
    "short_name": "SWT",
    "owner": "Brandon Smith",
    "tagline": "Professional Fleet Management Solutions",
    "address": {
        "street": "Your Street Address",
        "city": "Memphis",
        "state": "TN",
        "zip": "38xxx"
    },
    "contact": {
        "phone": "(901) XXX-XXXX",
        "email": "info@swtrucking.com",
        "website": "www.swtrucking.com"
    },
    "ein": "XX-XXXXXXX",
    "dot_number": "XXXXXXX",
    "mc_number": "XXXXXXX",
    "logo_files": {
        "main": "swt_logo.png",
        "white": "swt_logo_white.png",
        "video": "company_logo_animation.mp4.MOV"
    },
    "colors": {
        "primary": "#DC2626",      # Red
        "secondary": "#8B0000",    # Dark Red
        "success": "#10b981",      # Green
        "warning": "#f59e0b",      # Orange
        "danger": "#ef4444",       # Red
        "dark": "#000000",         # Black
        "light": "#ffffff"         # White
    }
}

# Security Manager Branding (Vernon Protection)
SECURITY_BRANDING = {
    "manager": "VERNON",
    "title": "SENIOR IT SECURITY MANAGER",
    "message": "DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER",
    "color": "#28a745",
    "font_size": "11px",
    "font_weight": "600",
    "letter_spacing": "0.5px"
}

# ===================================================================
# 2. VISUAL STYLING & CSS
# ===================================================================

GLOBAL_CSS = """
<style>
    /* Global App Styling */
    .main {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        padding: 0;
    }
    
    /* Streamlit Container Background */
    .stApp {
        background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
        background-attachment: fixed;
    }
    
    /* Header Styling */
    h1, h2, h3 {
        color: #DC2626;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Logo Container */
    .logo-container {
        text-align: center;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .logo-img {
        max-width: 200px;
        margin: 0 auto;
    }
    
    /* Tab Navigation - Horizontal Scroll for Many Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        overflow-x: auto !important;
        white-space: nowrap !important;
        scrollbar-width: thin;
        -webkit-overflow-scrolling: touch;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 8px 8px 0 0;
        flex-shrink: 0;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #DC2626 !important;
        color: white !important;
    }
    
    /* Card Styling */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #DC2626 0%, #8B0000 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Data Protection Footer */
    .data-protection-footer {
        text-align: center;
        padding: 20px;
        margin-top: 60px;
        border-top: 1px solid #e0e0e0;
        background: rgba(255, 255, 255, 0.95);
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    
    .stError {
        background-color: #f8d7da;
        border-color: #f5c6cb;
        color: #721c24;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Table Styling */
    .dataframe {
        font-size: 14px;
    }
    
    .dataframe th {
        background: #DC2626;
        color: white;
        font-weight: 600;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(220, 38, 38, 0.1);
        border-radius: 5px;
    }
</style>
"""

# ===================================================================
# 3. LOGIN SYSTEM WITH VIDEO LOGO
# ===================================================================

def create_login_page():
    """
    Complete login page with video logo animation
    """
    import streamlit as st
    import base64
    import os
    import time
    
    # Display video logo with fallback to static image
    animation_file = COMPANY_INFO["logo_files"]["video"]
    
    if os.path.exists(animation_file):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                with open(animation_file, 'rb') as video_file:
                    video_bytes = video_file.read()
                    video_b64 = base64.b64encode(video_bytes).decode()
                    video_html = f'''
                    <video width="100%" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    '''
                    st.markdown(video_html, unsafe_allow_html=True)
            except Exception:
                # Fallback to static logo
                logo_path = COMPANY_INFO["logo_files"]["white"]
                if os.path.exists(logo_path):
                    st.image(logo_path, use_container_width=True)
    
    st.title("🚚 Fleet Management System")
    st.subheader(COMPANY_INFO["name"])
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        with col2:
            if st.form_submit_button("Clear", use_container_width=True):
                st.rerun()
        
        if submitted:
            # Your authentication logic here
            if authenticate_user(username, password):
                st.session_state['authenticated'] = True
                st.session_state['user'] = username
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    # Vernon Protection Footer
    st.markdown(f"""
    <div class='data-protection-footer'>
        <p style='color: {SECURITY_BRANDING["color"]}; 
                  font-size: {SECURITY_BRANDING["font_size"]}; 
                  margin: 0; 
                  font-weight: {SECURITY_BRANDING["font_weight"]}; 
                  letter-spacing: {SECURITY_BRANDING["letter_spacing"]};'>
            {SECURITY_BRANDING["message"]}
        </p>
        <p style='color: #666; font-size: 10px; margin-top: 5px;'>
            © 2025 {COMPANY_INFO["name"]} - All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

# ===================================================================
# 4. DATABASE ARCHITECTURE
# ===================================================================

DATABASE_SCHEMA = """
-- Main Database Tables Structure

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    permissions TEXT,
    driver_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_title TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,
    location_type TEXT CHECK(location_type IN ('base', 'customer', 'yard')),
    is_base_location BOOLEAN DEFAULT 0,
    contact_name TEXT,
    contact_phone TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trailers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trailer_number TEXT UNIQUE NOT NULL,
    status TEXT CHECK(status IN ('available', 'in_transit', 'at_customer', 'maintenance', 'delivered')),
    current_location_id INTEGER REFERENCES locations(id),
    last_move_date DATE,
    is_new BOOLEAN DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_name TEXT UNIQUE NOT NULL,
    driver_type TEXT CHECK(driver_type IN ('owner', 'employee', 'contractor')),
    status TEXT CHECK(status IN ('active', 'inactive', 'on_leave')),
    phone TEXT,
    email TEXT,
    hire_date DATE,
    cdl_number TEXT,
    cdl_expiry DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS moves (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    system_id TEXT UNIQUE NOT NULL,
    mlbl_number TEXT,
    move_date DATE NOT NULL,
    trailer_id INTEGER REFERENCES trailers(id),
    new_trailer TEXT,
    old_trailer TEXT,
    origin_location_id INTEGER REFERENCES locations(id),
    destination_location_id INTEGER REFERENCES locations(id),
    driver_id INTEGER REFERENCES drivers(id),
    driver_name TEXT,
    status TEXT CHECK(status IN ('active', 'completed', 'cancelled')),
    payment_status TEXT CHECK(payment_status IN ('pending', 'paid', 'invoiced')),
    estimated_earnings DECIMAL(10,2),
    actual_earnings DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_moves_date ON moves(move_date);
CREATE INDEX idx_moves_driver ON moves(driver_id);
CREATE INDEX idx_moves_status ON moves(status);
CREATE INDEX idx_trailers_status ON trailers(status);
"""

# ===================================================================
# 4.5 REQUIRED APIS AND DEPENDENCIES
# ===================================================================

REQUIRED_DEPENDENCIES = """
# CORE PYTHON PACKAGES (Install with pip)
pip install streamlit==1.28.0
pip install pandas
pip install sqlite3
pip install reportlab  # For PDF generation
pip install pillow      # For image handling
pip install plotly      # For advanced charts (optional)
pip install folium      # For GPS/mapping (optional)
pip install googlemaps  # For distance calculation (optional)

# REQUIRED FILES TO COPY
1. pdf_generator.py - Main PDF generation system
2. universal_pdf_generator.py - Alternative PDF generator
3. professional_pdf_generator.py - Professional PDF templates
4. inventory_pdf_generator.py - Inventory reports

# COMPANY FILES REQUIRED
- swt_logo.png (Main company logo)
- swt_logo_white.png (White logo for dark backgrounds)
- company_logo_animation.mp4.MOV (Login page video)

# OPTIONAL API INTEGRATIONS
- Google Maps API (for distance calculations)
- Stripe/PayPal API (for payment processing)
- Twilio API (for SMS notifications)
- SendGrid API (for email notifications)

# REPORTLAB SPECIFIC REQUIREMENTS
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
"""

# Company Information for PDFs
PDF_COMPANY_INFO = {
    'name': 'SMITH & WILLIAMS TRUCKING LLC',
    'address': '7600 N 15th St Suite 150, Phoenix, AZ 85020',
    'phone': '(951) 437-5474',
    'email': 'Dispatch@smithwilliamstrucking.com',
    'website': 'www.smithwilliamstrucking.com',
    'dot': 'DOT #3675217',
    'mc': 'MC #1276006',
    'owner': 'Brandon Smith'
}

# ===================================================================
# 5. PDF GENERATION TEMPLATES
# ===================================================================

PDF_TEMPLATE_STRUCTURE = """
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import os

def create_professional_pdf(filename, title, data):
    '''
    Creates professional PDF with company branding
    '''
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Add logo if exists
    logo_path = "swt_logo.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2*inch, height=1*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 12))
    
    # Company header
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Smith & Williams Trucking LLC", header_style))
    elements.append(Paragraph(title, styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    # Add data table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 24))
    
    # Footer with Vernon protection
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#28a745'),
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER", footer_style))
    elements.append(Paragraph(f"© 2025 Smith & Williams Trucking LLC - All Rights Reserved", footer_style))
    
    # Build PDF
    doc.build(elements)
    return filename
"""

# ===================================================================
# 6. ERROR HANDLING PATTERNS
# ===================================================================

ERROR_HANDLING_PATTERNS = """
# LESSON: Always wrap database operations in try-except blocks
def safe_database_operation():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Your database operations here
        cursor.execute("SELECT * FROM table")
        result = cursor.fetchall()
        
        conn.commit()
        return result
        
    except sqlite3.IntegrityError as e:
        st.error(f"Database integrity error: {str(e)}")
        if conn:
            conn.rollback()
        return None
        
    except sqlite3.OperationalError as e:
        st.error(f"Database operational error: {str(e)}")
        return None
        
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None
        
    finally:
        if conn:
            conn.close()

# LESSON: Initialize variables before conditional blocks
def prevent_unbound_errors():
    # Always initialize variables that will be used later
    result = []  # Initialize to prevent UnboundLocalError
    data = None
    
    if condition:
        result = fetch_data()
    else:
        result = fetch_alternative_data()
    
    # Now 'result' is always defined
    if result:
        process_data(result)

# LESSON: Handle missing imports gracefully
try:
    from specialized_module import SpecialFeature
    FEATURE_AVAILABLE = True
except ImportError:
    FEATURE_AVAILABLE = False
    # Provide fallback functionality
    def SpecialFeature(*args, **kwargs):
        return "Feature not available"

# LESSON: Validate user input thoroughly
def validate_input(value, field_name):
    if value is None or value == "":
        st.error(f"{field_name} is required")
        return False
    
    if field_name == "email" and "@" not in value:
        st.error("Invalid email format")
        return False
    
    if field_name == "phone" and len(value) < 10:
        st.error("Phone number must be at least 10 digits")
        return False
    
    return True

# LESSON: Use session state to prevent data loss
def preserve_user_data():
    # Store form data in session state
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    
    # Update session state on change
    value = st.text_input("Field", 
                          value=st.session_state.form_data.get('field', ''),
                          key='field_input')
    
    if value:
        st.session_state.form_data['field'] = value
"""

# ===================================================================
# 7. REUSABLE COMPONENTS
# ===================================================================

class ReusableComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def create_metric_card(title, value, delta=None, delta_color="normal"):
        """Creates a styled metric card"""
        import streamlit as st
        
        with st.container():
            st.markdown("""
            <div class="metric-card">
                <h4>{}</h4>
                <h2>{}</h2>
                {}
            </div>
            """.format(
                title, 
                value,
                '<p style="color: {}">{}</p>'.format("green" if delta_color == "normal" else "red", delta) if delta else ''
            ), unsafe_allow_html=True)
    
    @staticmethod
    def create_sidebar_with_logo():
        """Creates sidebar with company logo"""
        import streamlit as st
        
        with st.sidebar:
            # Logo
            logo_path = COMPANY_INFO["logo_files"]["white"]
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
            
            st.divider()
            
            # User info
            if 'user' in st.session_state:
                st.write(f"👤 **User:** {st.session_state['user']}")
                st.write(f"📋 **Role:** {st.session_state.get('role', 'User')}")
            
            st.divider()
            
            # Navigation or actions
            return st.sidebar
    
    @staticmethod
    def create_data_table(data, columns, searchable=True, downloadable=True):
        """Creates an interactive data table"""
        import streamlit as st
        import pandas as pd
        
        df = pd.DataFrame(data, columns=columns)
        
        if searchable:
            search = st.text_input("🔍 Search table", "")
            if search:
                mask = df.apply(lambda x: x.astype(str).str.contains(search, case=False).any(), axis=1)
                df = df[mask]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        if downloadable:
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Download CSV",
                csv,
                "data.csv",
                "text/csv",
                key='download-csv'
            )
        
        return df
    
    @staticmethod
    def create_date_range_selector():
        """Creates date range selector"""
        import streamlit as st
        from datetime import datetime, timedelta
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            start_date = st.date_input(
                "From Date",
                datetime.now() - timedelta(days=30)
            )
        
        with col2:
            end_date = st.date_input(
                "To Date",
                datetime.now()
            )
        
        with col3:
            quick_select = st.selectbox(
                "Quick Select",
                ["Custom", "Today", "This Week", "This Month", "Last 30 Days"]
            )
        
        if quick_select == "Today":
            start_date = end_date = datetime.now().date()
        elif quick_select == "This Week":
            start_date = datetime.now().date() - timedelta(days=datetime.now().weekday())
            end_date = datetime.now().date()
        elif quick_select == "This Month":
            start_date = datetime.now().replace(day=1).date()
            end_date = datetime.now().date()
        elif quick_select == "Last 30 Days":
            start_date = datetime.now().date() - timedelta(days=30)
            end_date = datetime.now().date()
        
        return start_date, end_date

# ===================================================================
# 8. LESSONS LEARNED
# ===================================================================

LESSONS_LEARNED = """
CRITICAL LESSONS FROM PRODUCTION DEPLOYMENT:

1. DATABASE MIGRATIONS:
   - ALWAYS check table structure before queries
   - Use PRAGMA table_info() to verify columns exist
   - Have fallback queries for different schema versions
   - Never assume database structure

2. VARIABLE INITIALIZATION:
   - Initialize ALL variables before conditional blocks
   - The UnboundLocalError is common in Streamlit apps
   - Set defaults for all variables that might not be assigned

3. IMPORT HANDLING:
   - Always use try-except for optional imports
   - Provide fallback functionality
   - Check availability with boolean flags

4. SESSION STATE MANAGEMENT:
   - Critical for preserving data across reruns
   - Always check if key exists before accessing
   - Use get() method with defaults
   - Clear cache periodically to prevent memory issues

5. FILE OPERATIONS:
   - Always verify file exists before reading
   - Use absolute paths in production
   - Handle encoding issues explicitly
   - Provide meaningful error messages

6. PDF GENERATION:
   - Have multiple fallback options
   - Text files as ultimate fallback
   - Check for required libraries at startup
   - Template all company information

7. USER AUTHENTICATION:
   - Never store plain text passwords
   - Use session state for auth status
   - Implement role-based access control
   - Add audit logging for sensitive operations

8. ERROR MESSAGES:
   - Be specific but don't leak sensitive info
   - Log full errors, show user-friendly messages
   - Provide actionable next steps
   - Include support contact information

9. PERFORMANCE:
   - Cache expensive operations
   - Use indices on frequently queried columns
   - Paginate large datasets
   - Clear cache periodically

10. DEPLOYMENT:
    - Test with production-like data volumes
    - Have backup and restore procedures
    - Monitor resource usage
    - Plan for concurrent users
"""

# ===================================================================
# 9. BEST PRACTICES
# ===================================================================

BEST_PRACTICES = """
STREAMLIT BEST PRACTICES:

1. PAGE CONFIGURATION:
   st.set_page_config(
       page_title="Your App Title",
       page_icon="🚚",
       layout="wide",
       initial_sidebar_state="expanded"
   )

2. CACHING STRATEGY:
   - Use @st.cache_data for data operations
   - Use @st.cache_resource for resources
   - Clear cache on version changes
   - Implement time-based cache clearing

3. STATE MANAGEMENT:
   - Initialize all session state variables at startup
   - Use callbacks for form submissions
   - Preserve user input across reruns
   - Clean up state on logout

4. UI/UX PATTERNS:
   - Use columns for responsive layouts
   - Implement loading spinners for long operations
   - Provide clear feedback for all actions
   - Use tabs for complex interfaces

5. DATABASE CONNECTIONS:
   - Use connection pooling for production
   - Always close connections in finally blocks
   - Implement retry logic for transient failures
   - Use transactions for multi-step operations

6. SECURITY:
   - Never commit secrets to repository
   - Use environment variables for sensitive data
   - Implement input validation
   - Sanitize all user inputs
   - Add CSRF protection for forms

7. TESTING:
   - Test with various data volumes
   - Test all error conditions
   - Test with concurrent users
   - Implement automated testing

8. DOCUMENTATION:
   - Document all configuration options
   - Provide setup instructions
   - Include troubleshooting guide
   - Maintain changelog

9. MONITORING:
   - Log all critical operations
   - Monitor resource usage
   - Track user activities
   - Set up alerts for failures

10. BACKUP & RECOVERY:
    - Automated daily backups
    - Test restore procedures
    - Version control for code
    - Document recovery steps
"""

# ===================================================================
# 10. QUICK START TEMPLATE
# ===================================================================

def create_new_app():
    """
    Complete template for starting a new Streamlit app with all
    Smith & Williams Trucking branding and best practices
    """
    
    app_template = '''
import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import os
import json
import time
import base64

# Page Configuration
st.set_page_config(
    page_title="Fleet Management System",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Version Management
APP_VERSION = "1.0.0"
COMPANY_NAME = "Smith & Williams Trucking LLC"

# Apply Global Styling
st.markdown("""''' + GLOBAL_CSS + '''""", unsafe_allow_html=True)

# Database Path
DB_PATH = "fleet_management.db"

# Initialize Database
def init_database():
    """Initialize database with all required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables using the schema
    cursor.executescript("""''' + DATABASE_SCHEMA + '''""")
    
    conn.commit()
    conn.close()

# Authentication Check
def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

# Login Page
def show_login():
    """Display login page with video logo"""
    ''' + str(create_login_page.__doc__) + '''
    
    # Video logo implementation
    animation_file = "company_logo_animation.mp4.MOV"
    if os.path.exists(animation_file):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                with open(animation_file, "rb") as video_file:
                    video_bytes = video_file.read()
                    video_b64 = base64.b64encode(video_bytes).decode()
                    video_html = f"""
                    <video width="100%" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                    </video>
                    """
                    st.markdown(video_html, unsafe_allow_html=True)
            except:
                if os.path.exists("swt_logo_white.png"):
                    st.image("swt_logo_white.png", use_container_width=True)
    
    st.title("🚚 Fleet Management System")
    st.subheader(COMPANY_NAME)
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login", type="primary"):
            # Add your authentication logic
            if username and password:  # Replace with actual auth
                st.session_state["authenticated"] = True
                st.session_state["user"] = username
                st.success("Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    # Vernon Protection Footer
    st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 60px; border-top: 1px solid #e0e0e0;">
        <p style="color: #28a745; font-size: 11px; margin: 0; font-weight: 600; letter-spacing: 0.5px;">
            DATA PROTECTED BY VERNON - SENIOR IT SECURITY MANAGER
        </p>
        <p style="color: #666; font-size: 10px; margin-top: 5px;">
            © 2025 Smith & Williams Trucking LLC - All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main Application
def main_app():
    """Main application after login"""
    
    # Sidebar
    with st.sidebar:
        # Logo
        if os.path.exists("swt_logo_white.png"):
            st.image("swt_logo_white.png", use_container_width=True)
        
        st.divider()
        
        # User info
        st.write(f"👤 **User:** {st.session_state.get('user', 'Unknown')}")
        st.write(f"📋 **Role:** {st.session_state.get('role', 'User')}")
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Main content area
    st.title("Fleet Management Dashboard")
    st.write(f"Welcome to {COMPANY_NAME}")
    
    # Create tabs for different sections
    tabs = st.tabs(["📊 Dashboard", "🚚 Fleet", "📋 Moves", "👥 Drivers", "📈 Reports", "⚙️ Settings"])
    
    with tabs[0]:
        st.header("Dashboard")
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Trailers", "45", "↑ 3")
        
        with col2:
            st.metric("Today's Moves", "12", "↑ 2")
        
        with col3:
            st.metric("Active Drivers", "8", "→ 0")
        
        with col4:
            st.metric("Revenue MTD", "$45,230", "↑ 15%")
        
        # Add your dashboard content here
    
    with tabs[1]:
        st.header("Fleet Management")
        # Add fleet management features
    
    with tabs[2]:
        st.header("Move Management")
        # Add move management features
    
    with tabs[3]:
        st.header("Driver Management")
        # Add driver management features
    
    with tabs[4]:
        st.header("Reports")
        # Add reporting features
    
    with tabs[5]:
        st.header("Settings")
        # Add settings features

# Main execution
def main():
    """Main application entry point"""
    
    # Initialize database on first run
    if "db_initialized" not in st.session_state:
        init_database()
        st.session_state["db_initialized"] = True
    
    # Check authentication
    if not check_authentication():
        show_login()
    else:
        main_app()

if __name__ == "__main__":
    main()
'''
    
    return app_template

# ===================================================================
# DEPLOYMENT CHECKLIST
# ===================================================================

DEPLOYMENT_CHECKLIST = """
PRE-DEPLOYMENT CHECKLIST:

□ Database:
  - [ ] Production database created
  - [ ] All tables created with proper schema
  - [ ] Indexes added for performance
  - [ ] Backup system configured
  - [ ] Migration scripts tested

□ Security:
  - [ ] All passwords changed from defaults
  - [ ] Environment variables configured
  - [ ] SSL certificates installed
  - [ ] Input validation implemented
  - [ ] SQL injection prevention verified

□ Files:
  - [ ] Company logos uploaded (swt_logo.png, swt_logo_white.png)
  - [ ] Video animation file uploaded (company_logo_animation.mp4.MOV)
  - [ ] All PDF templates tested
  - [ ] File permissions set correctly

□ Configuration:
  - [ ] Company information updated
  - [ ] Email settings configured
  - [ ] Payment processing setup
  - [ ] Notification system tested

□ Testing:
  - [ ] All user roles tested
  - [ ] Data import/export verified
  - [ ] PDF generation working
  - [ ] Error handling verified
  - [ ] Performance testing completed

□ Documentation:
  - [ ] User manual created
  - [ ] Admin guide written
  - [ ] API documentation (if applicable)
  - [ ] Troubleshooting guide prepared

□ Monitoring:
  - [ ] Logging configured
  - [ ] Error tracking setup
  - [ ] Performance monitoring enabled
  - [ ] Backup verification scheduled

□ Training:
  - [ ] User training completed
  - [ ] Admin training completed
  - [ ] Support procedures established
  - [ ] Emergency contacts documented
"""

# ===================================================================
# USAGE INSTRUCTIONS
# ===================================================================

USAGE_INSTRUCTIONS = """
HOW TO USE THIS TEMPLATE PACKAGE:

1. STARTING A NEW PROJECT:
   - Copy the create_new_app() function output to a new file
   - Update COMPANY_INFO dictionary with your details
   - Customize colors in the CSS section
   - Add your logo files to the project directory

2. APPLYING STYLING:
   - Copy GLOBAL_CSS into your app
   - Apply with st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
   - Customize colors using COMPANY_INFO['colors']

3. IMPLEMENTING LOGIN:
   - Use create_login_page() function
   - Ensure video and logo files are present
   - Implement your authentication backend

4. DATABASE SETUP:
   - Use DATABASE_SCHEMA as template
   - Run init_database() on first launch
   - Implement migration scripts for updates

5. PDF GENERATION:
   - Use PDF_TEMPLATE_STRUCTURE as base
   - Customize with company branding
   - Test with sample data

6. ERROR HANDLING:
   - Implement patterns from ERROR_HANDLING_PATTERNS
   - Always initialize variables
   - Use try-except blocks consistently

7. COMPONENTS:
   - Import ReusableComponents class
   - Use provided methods for consistent UI
   - Extend with your own components

8. DEPLOYMENT:
   - Follow DEPLOYMENT_CHECKLIST
   - Test in staging environment first
   - Monitor initial deployment closely

9. MAINTENANCE:
   - Regular backups
   - Monitor error logs
   - Update dependencies
   - Document all changes

For support and questions, contact Brandon Smith - Owner
Smith & Williams Trucking LLC
"""

# ===================================================================
# EXPORT READY-TO-USE APP
# ===================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SMITH & WILLIAMS TRUCKING LLC")
    print("Complete System Template Package")
    print("Version 1.0.0")
    print("=" * 70)
    print("\nThis package contains everything needed to create new")
    print("applications with consistent branding and best practices.")
    print("\nFiles needed:")
    print("  - swt_logo.png")
    print("  - swt_logo_white.png")
    print("  - company_logo_animation.mp4.MOV")
    print("\nRefer to USAGE_INSTRUCTIONS for implementation details.")
    print("=" * 70)
    
    # Generate a ready-to-use app file
    with open("new_app_template.py", "w") as f:
        f.write(create_new_app())
    
    print("\n✅ Template files generated successfully!")
    print("   - new_app_template.py created")
    print("\nYou can now start building your new application!")