"""
===================================================================
INTERACTIVE TRAINING SYSTEM - TRANSPORTATION MANAGEMENT SYSTEM
Smith & Williams Trucking LLC
===================================================================
This training system teaches you:
1. How to deploy the TMS to production
2. Where everything goes and why
3. How to use every feature of the system
4. Best practices and workflows
===================================================================
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import time

# Page Configuration
st.set_page_config(
    page_title="TMS Training System - Smith & Williams",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Training Progress Tracking
if 'training_progress' not in st.session_state:
    st.session_state.training_progress = {
        'deployment': 0,
        'system_architecture': 0,
        'ceo_features': 0,
        'operations': 0,
        'completed_modules': []
    }

def mark_module_complete(module_name):
    """Mark a training module as complete"""
    if module_name not in st.session_state.training_progress['completed_modules']:
        st.session_state.training_progress['completed_modules'].append(module_name)
        st.balloons()
        st.success(f"✅ Module '{module_name}' completed!")

# ===================================================================
# MAIN TRAINING INTERFACE
# ===================================================================

def main():
    st.title("🎓 TMS Interactive Training System")
    st.markdown("*Complete Production Deployment & Operations Training*")
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## Training Modules")
        
        # Show progress
        total_modules = 12
        completed = len(st.session_state.training_progress['completed_modules'])
        progress = completed / total_modules
        st.progress(progress)
        st.metric("Progress", f"{completed}/{total_modules} modules")
        
        st.markdown("---")
        
        module = st.radio(
            "Select Training Module",
            [
                "1. Getting Started",
                "2. Production Deployment",
                "3. System Architecture",
                "4. Database Setup",
                "5. API Configuration",
                "6. CEO Features",
                "7. Dispatcher Operations",
                "8. Driver Operations",
                "9. Financial Management",
                "10. Goal Setting & AI",
                "11. Troubleshooting",
                "12. Best Practices"
            ]
        )
    
    # Main Content Area
    if "1. Getting Started" in module:
        show_getting_started()
    elif "2. Production Deployment" in module:
        show_production_deployment()
    elif "3. System Architecture" in module:
        show_system_architecture()
    elif "4. Database Setup" in module:
        show_database_setup()
    elif "5. API Configuration" in module:
        show_api_configuration()
    elif "6. CEO Features" in module:
        show_ceo_features()
    elif "7. Dispatcher Operations" in module:
        show_dispatcher_operations()
    elif "8. Driver Operations" in module:
        show_driver_operations()
    elif "9. Financial Management" in module:
        show_financial_management()
    elif "10. Goal Setting" in module:
        show_goal_setting()
    elif "11. Troubleshooting" in module:
        show_troubleshooting()
    elif "12. Best Practices" in module:
        show_best_practices()

# ===================================================================
# MODULE 1: GETTING STARTED
# ===================================================================

def show_getting_started():
    st.header("Module 1: Getting Started with TMS")
    
    tabs = st.tabs(["Overview", "Requirements", "Quick Start", "Quiz"])
    
    with tabs[0]:  # Overview
        st.subheader("System Overview")
        
        st.info("""
        **What is the Transportation Management System (TMS)?**
        
        The TMS is a comprehensive Four-Tier system designed specifically for Smith & Williams Trucking LLC:
        - **Tier 1:** Booking & Dispatching (Operational Command Center)
        - **Tier 2:** Load & Invoice Management (Financial Enrichment)
        - **Tier 3:** Finance & Compliance (Executive Reporting)
        - **Tier 4:** Automation & AI (Smart Management)
        """)
        
        st.markdown("""
        ### Key Benefits:
        1. **Complete Visibility** - Track every load, truck, and driver in real-time
        2. **Smart Automation** - AI-powered load finding and goal management
        3. **Financial Control** - Automated invoicing and profit tracking
        4. **CEO Dual Mode** - Switch between executive and driver roles
        5. **Dynamic Profit Goals** - Adjust targets based on real performance
        """)
        
        with st.expander("System Capabilities"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **Operational Features:**
                - Load prioritization (Contract vs Load Board)
                - Smart load & route planning bot
                - Intelligent negotiation tool
                - Real-time dispatch management
                - Document management with Vector API
                - Driver mobile interface
                """)
            
            with col2:
                st.markdown("""
                **Business Features:**
                - Automated invoicing
                - Factoring workflow
                - Maintenance tracking
                - Compliance monitoring
                - AI-powered goal setting
                - Performance analytics
                """)
    
    with tabs[1]:  # Requirements
        st.subheader("System Requirements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Software Requirements:
            - **Python 3.8+** (Already installed)
            - **Streamlit** (Already installed)
            - **SQLite** (Built-in with Python)
            - **Web Browser** (Chrome/Firefox/Edge)
            
            ### Hardware Requirements:
            - **Server/Computer:** 4GB RAM minimum
            - **Storage:** 10GB free space
            - **Internet:** Stable connection for APIs
            """)
        
        with col2:
            st.markdown("""
            ### API Requirements:
            - **Google Maps API** - For routing
            - **Truckstop.com API** - Load board access
            - **GoMotive API** - ELD/HOS data
            - **Vector API** - Document processing
            - **Treadstone Capital** - Factoring
            
            ### Business Requirements:
            - **DOT Number:** 3675217
            - **MC Number:** 1276006
            - **Business Registration:** Phoenix, AZ
            """)
        
        st.warning("""
        **Important:** Before going to production, ensure you have:
        1. All API keys configured
        2. Backup system in place
        3. SSL certificate for secure access
        4. Domain name (optional but recommended)
        """)
    
    with tabs[2]:  # Quick Start
        st.subheader("Quick Start Guide")
        
        st.markdown("""
        ### Step 1: Access the System
        """)
        
        code_col1, desc_col1 = st.columns([1, 2])
        with code_col1:
            st.code("http://localhost:8600", language="text")
        with desc_col1:
            st.write("Current local access URL")
        
        st.markdown("""
        ### Step 2: Login as CEO
        """)
        
        code_col2, desc_col2 = st.columns([1, 2])
        with code_col2:
            st.code("""
Username: Brandon
Password: ceo123
            """, language="text")
        with desc_col2:
            st.write("Your CEO credentials with full system access")
        
        st.markdown("""
        ### Step 3: Choose Your Mode
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **Executive Mode:**
            - Access all four tiers
            - Manage users and settings
            - View comprehensive reports
            - Set company goals
            """)
        
        with col2:
            st.info("""
            **Driver Mode:**
            - View assigned loads
            - Access navigation
            - Upload documents
            - Track HOS status
            """)
        
        if st.button("Complete Module 1", type="primary"):
            mark_module_complete("Getting Started")
    
    with tabs[3]:  # Quiz
        st.subheader("Knowledge Check")
        
        with st.form("quiz_1"):
            q1 = st.radio(
                "1. How many tiers does the TMS have?",
                ["2", "3", "4", "5"]
            )
            
            q2 = st.radio(
                "2. What is the minimum profit target per mile?",
                ["$1.50", "$2.00", "$2.50", "$3.00"]
            )
            
            q3 = st.multiselect(
                "3. Which APIs does the system use? (Select all)",
                ["Google Maps", "Facebook", "GoMotive", "Vector", "Instagram"]
            )
            
            submitted = st.form_submit_button("Check Answers")
            
            if submitted:
                score = 0
                if q1 == "4":
                    score += 1
                if q2 == "$2.00":
                    score += 1
                if set(q3) == {"Google Maps", "GoMotive", "Vector"}:
                    score += 1
                
                if score == 3:
                    st.success(f"Perfect! Score: {score}/3")
                else:
                    st.warning(f"Score: {score}/3 - Review the material and try again")

# ===================================================================
# MODULE 2: PRODUCTION DEPLOYMENT
# ===================================================================

def show_production_deployment():
    st.header("Module 2: Production Deployment")
    
    tabs = st.tabs(["Local Setup", "Cloud Deployment", "Security", "Checklist"])
    
    with tabs[0]:  # Local Setup
        st.subheader("Local Production Setup")
        
        st.markdown("""
        ### Option 1: Dedicated Computer/Server
        
        This is the simplest approach for small operations:
        """)
        
        with st.expander("Step-by-Step Local Deployment"):
            st.markdown("""
            **1. Prepare the Computer:**
            ```bash
            # Create dedicated folder
            C:\\TMS-Production\\
            
            # Copy all files
            - four_tier_tms.py
            - config/ folder
            - assets/ folder
            - templates/ folder
            ```
            
            **2. Create Startup Script:**
            """)
            
            st.code("""
@echo off
cd C:\\TMS-Production
streamlit run four_tier_tms.py --server.port 80 --server.address 0.0.0.0
            """, language="batch")
            
            st.markdown("""
            **3. Configure Windows to Start on Boot:**
            - Add batch file to Windows Startup folder
            - Or create a Windows Service
            
            **4. Set up Port Forwarding (for remote access):**
            - Configure router to forward port 80
            - Use Dynamic DNS service for stable URL
            """)
        
        st.warning("""
        **Security Note:** For production use, always:
        - Change default passwords
        - Enable Windows Firewall
        - Use VPN for remote access
        - Regular backups to external drive
        """)
    
    with tabs[1]:  # Cloud Deployment
        st.subheader("Cloud Deployment Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Option 2: Cloud Hosting
            
            **Recommended: Streamlit Cloud (Free)**
            1. Push code to GitHub
            2. Connect to Streamlit Cloud
            3. Deploy with one click
            
            **Benefits:**
            - Free for small apps
            - Automatic HTTPS
            - No maintenance
            - Accessible anywhere
            """)
            
            with st.expander("Streamlit Cloud Setup"):
                st.code("""
# 1. Create requirements.txt
streamlit==1.28.0
pandas
plotly
requests
Pillow

# 2. Push to GitHub
git init
git add .
git commit -m "Initial TMS"
git push

# 3. Deploy
# Go to share.streamlit.io
# Connect GitHub repo
# Click Deploy
                """, language="bash")
        
        with col2:
            st.markdown("""
            ### Option 3: AWS/Azure
            
            **For larger operations:**
            1. EC2/VM instance
            2. Install Python & dependencies
            3. Configure security groups
            4. Set up domain name
            
            **Benefits:**
            - Full control
            - Scalable
            - Professional domain
            - Database options
            """)
            
            with st.expander("AWS EC2 Setup"):
                st.code("""
# Connect to EC2
ssh ec2-user@your-instance

# Install Python
sudo yum install python3

# Install TMS
git clone your-repo
cd tms
pip3 install -r requirements.txt

# Run with systemd
sudo systemctl start tms
                """, language="bash")
    
    with tabs[2]:  # Security
        st.subheader("Security Configuration")
        
        st.error("""
        **CRITICAL: Production Security Checklist**
        """)
        
        security_items = {
            "Change all default passwords": False,
            "Enable HTTPS/SSL": False,
            "Configure firewall rules": False,
            "Set up VPN access": False,
            "Enable database encryption": False,
            "Configure backup system": False,
            "Set up monitoring alerts": False,
            "Create user access policies": False
        }
        
        for item, default in security_items.items():
            st.checkbox(item, value=default, key=f"sec_{item}")
        
        st.markdown("""
        ### Password Security
        
        **Change these immediately in production:**
        """)
        
        st.code("""
# In four_tier_tms.py, line 252-259:

# Change from:
ceo_password = hashlib.sha256('ceo123'.encode()).hexdigest()

# To something like:
ceo_password = hashlib.sha256('YourSecurePassword2024!'.encode()).hexdigest()
        """, language="python")
        
        st.markdown("""
        ### Database Security
        """)
        
        st.code("""
# Add database encryption
import sqlite3
from cryptography.fernet import Fernet

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt sensitive data before storing
encrypted_data = cipher_suite.encrypt(sensitive_data.encode())
        """, language="python")
    
    with tabs[3]:  # Checklist
        st.subheader("Production Deployment Checklist")
        
        st.markdown("""
        ### Pre-Deployment
        """)
        
        pre_deploy = [
            "All API keys obtained and tested",
            "Database backup system configured",
            "SSL certificate installed",
            "Domain name registered (optional)",
            "Firewall rules configured",
            "Admin passwords changed",
            "Test data removed"
        ]
        
        for item in pre_deploy:
            st.checkbox(item, key=f"pre_{item}")
        
        st.markdown("""
        ### Deployment
        """)
        
        deploy = [
            "Code deployed to production environment",
            "Database initialized",
            "API keys configured in environment variables",
            "Startup scripts created",
            "Monitoring configured",
            "First backup completed"
        ]
        
        for item in deploy:
            st.checkbox(item, key=f"dep_{item}")
        
        st.markdown("""
        ### Post-Deployment
        """)
        
        post_deploy = [
            "System accessible from all required locations",
            "All users can login successfully",
            "Test load created and processed",
            "Reports generating correctly",
            "Backup restoration tested",
            "Training completed for all users"
        ]
        
        for item in post_deploy:
            st.checkbox(item, key=f"post_{item}")
        
        if st.button("Complete Module 2", type="primary"):
            mark_module_complete("Production Deployment")

# ===================================================================
# MODULE 3: SYSTEM ARCHITECTURE
# ===================================================================

def show_system_architecture():
    st.header("Module 3: System Architecture")
    
    tabs = st.tabs(["Four Tiers", "Data Flow", "File Structure", "Understanding"])
    
    with tabs[0]:  # Four Tiers
        st.subheader("Understanding the Four-Tier Architecture")
        
        st.markdown("""
        ### Why Four Tiers?
        
        Each tier has a specific purpose and builds on the previous one:
        """)
        
        tier_data = {
            "Tier": ["Tier 1", "Tier 2", "Tier 3", "Tier 4"],
            "Name": ["Booking & Dispatching", "Load & Invoice", "Finance & Compliance", "Automation & AI"],
            "Purpose": [
                "Operational data entry and management",
                "Financial enrichment and invoicing",
                "Executive reporting and compliance",
                "Smart automation and goal management"
            ],
            "Users": ["Dispatchers, Drivers", "Admin, Accounting", "CEO, Management", "System (Automated)"]
        }
        
        df = pd.DataFrame(tier_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        with st.expander("Tier 1: Booking & Dispatching - Details"):
            st.markdown("""
            **Purpose:** The operational heart of the system
            
            **Key Features:**
            - Load prioritization (Contract loads first)
            - Smart load finder bot
            - Negotiation tool ($2.00/mile target)
            - Driver-truck assignments
            - Document management
            - Factoring preparation
            
            **Data Created:**
            - Load records
            - Driver assignments
            - Route plans
            - Documents (BOL, POD)
            
            **Why It's First:** All business operations start here
            """)
        
        with st.expander("Tier 2: Load & Invoice Management - Details"):
            st.markdown("""
            **Purpose:** Add financial data to operations
            
            **Key Features:**
            - Invoice generation
            - Rate calculations
            - Maintenance tracking
            - Cost analysis
            - Payment tracking
            
            **Data Created:**
            - Invoices
            - Payment records
            - Maintenance logs
            - Cost reports
            
            **Why It's Second:** Builds on operational data from Tier 1
            """)
        
        with st.expander("Tier 3: Finance & Compliance - Details"):
            st.markdown("""
            **Purpose:** Executive oversight and compliance
            
            **Key Features:**
            - P&L reports
            - Payroll processing
            - Compliance tracking
            - QuickBooks integration
            - IFTA reporting
            
            **Data Created:**
            - Financial reports
            - Compliance records
            - Payroll data
            
            **Why It's Third:** Aggregates data from Tiers 1 & 2
            """)
        
        with st.expander("Tier 4: Automation & AI - Details"):
            st.markdown("""
            **Purpose:** Intelligent automation and optimization
            
            **Key Features:**
            - AI goal setting
            - Task automation
            - Performance optimization
            - Predictive analytics
            - Alert management
            
            **Data Created:**
            - Goals and targets
            - Automated tasks
            - Performance predictions
            
            **Why It's Fourth:** Oversees and optimizes all other tiers
            """)
    
    with tabs[1]:  # Data Flow
        st.subheader("Data Flow Through the System")
        
        st.markdown("""
        ### How Data Moves Through Tiers:
        
        ```
        1. Load Created (Tier 1)
           ↓
        2. Driver Assigned (Tier 1)
           ↓
        3. Documents Uploaded (Tier 1)
           ↓
        4. Invoice Generated (Tier 2)
           ↓
        5. Payment Recorded (Tier 2)
           ↓
        6. P&L Updated (Tier 3)
           ↓
        7. AI Analyzes Performance (Tier 4)
           ↓
        8. Goals Adjusted (Tier 4)
        ```
        """)
        
        st.info("""
        **Example: Processing a Load**
        
        1. **Dispatcher** (Tier 1): Creates load, assigns driver
        2. **Driver** (Tier 1): Uploads signed BOL
        3. **System** (Tier 2): Automatically generates invoice
        4. **Accounting** (Tier 2): Records payment when received
        5. **CEO** (Tier 3): Views updated P&L report
        6. **AI** (Tier 4): Suggests rate adjustment based on profitability
        """)
    
    with tabs[2]:  # File Structure
        st.subheader("File Structure & Organization")
        
        st.code("""
C:\\SWTTMSHUB\\                    # Root directory
│
├── four_tier_tms.py              # Main application file
├── four_tier_tms.db              # SQLite database
├── requirements.txt              # Python dependencies
│
├── config/                       # Configuration files
│   ├── COMPLETE_SYSTEM_TEMPLATE_PACKAGE.py
│   └── TEMPLATE_EVOLUTION_FRAMEWORK.py
│
├── assets/                       # Media files
│   ├── logos/
│   │   ├── swt_logo.png
│   │   └── swt_logo_white.png
│   └── videos/
│       └── company_logo_animation.mp4.MOV
│
├── templates/                    # PDF templates
│   ├── pdf_generator.py
│   ├── universal_pdf_generator.py
│   └── professional_pdf_generator.py
│
├── backups/                      # Database backups
│   └── backup_20250117.db
│
└── documents/                    # Uploaded documents
    ├── rate_confirmations/
    ├── bills_of_lading/
    └── proof_of_delivery/
        """, language="text")
        
        st.markdown("""
        ### Why This Structure?
        
        - **Root Level:** Main application and database for easy access
        - **config/:** Separates configuration from code
        - **assets/:** Keeps media organized
        - **templates/:** Reusable PDF generation
        - **backups/:** Critical for data recovery
        - **documents/:** Organized by type for easy retrieval
        """)
    
    with tabs[3]:  # Understanding
        st.subheader("Understanding the System")
        
        st.markdown("""
        ### Key Concepts to Master:
        
        1. **Load Prioritization**
           - Contract loads (CanAmex, Metro) ALWAYS first
           - Load board only when trucks available
           - $2.00/mile minimum (adjustable in goals)
        
        2. **Dynamic Driver-Truck Assignment**
           - Drivers not permanently assigned to trucks
           - Assignment per load basis
           - Tracked in database for history
        
        3. **Document Flow**
           - Rate Confirmation → Dispatcher uploads
           - BOL → Driver uploads after signature
           - POD → Driver uploads at delivery
           - All processed through Vector API
        
        4. **Factoring Timeline**
           - Load Board/Metro: Submit by 11 AM EST for next-day payment
           - CanAmex: Weekly submission (Sunday-Saturday loads)
        
        5. **Goal Management**
           - AI suggests based on historical data
           - CEO approves/modifies
           - System adjusts all recommendations
        """)
        
        if st.button("Complete Module 3", type="primary"):
            mark_module_complete("System Architecture")

# ===================================================================
# MODULE 6: CEO FEATURES TRAINING
# ===================================================================

def show_ceo_features():
    st.header("Module 6: CEO Features & Dual Mode")
    
    tabs = st.tabs(["CEO Overview", "Executive Mode", "Driver Mode", "Practice"])
    
    with tabs[0]:  # Overview
        st.subheader("CEO Unique Capabilities")
        
        st.info("""
        As CEO, you have complete control over the system with two operating modes:
        
        **Executive Mode:** Strategic management and oversight
        **Driver Mode:** Operational tasks when you're driving
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Executive Mode Powers:
            - User management (create/edit/delete)
            - System settings control
            - Goal setting with AI assistance
            - Override any system decision
            - Access all financial data
            - View all driver/truck data
            - Modify any record
            - Generate executive reports
            """)
        
        with col2:
            st.markdown("""
            ### Driver Mode Features:
            - View assigned loads
            - Access navigation
            - Upload documents
            - Track HOS status
            - View performance metrics
            - Update load status
            - Communicate with dispatch
            - Access route information
            """)
    
    with tabs[1]:  # Executive Mode
        st.subheader("Executive Mode Training")
        
        with st.expander("Setting Company Goals"):
            st.markdown("""
            **Navigate to: Goal Management**
            
            1. **Review AI Suggestions:**
               - System analyzes your historical data
               - Suggests achievable profit goals
               - Shows market trends
            
            2. **Set Custom Goals:**
               ```
               Target Rate/Mile: $2.25 (up from $2.00)
               Weekly Revenue: $50,000
               Fleet Utilization: 90%
               Empty Miles: <15%
               ```
            
            3. **System Adjustments:**
               - Negotiation tool uses new target
               - Load finder prioritizes higher rates
               - Reports track against new goals
            """)
        
        with st.expander("User Management"):
            st.markdown("""
            **Navigate to: User Management**
            
            **Creating Users:**
            1. Click "Create User"
            2. Enter details:
               - Username
               - Password (they'll change on first login)
               - Role (Admin, Dispatcher, Driver, Accounting)
               - Contact info
            
            **Role Permissions:**
            - **Admin:** Everything except user management
            - **Dispatcher:** Tier 1 full access, Tier 2 view
            - **Driver:** Limited Tier 1 (own loads only)
            - **Accounting:** Tier 2 full, Tier 3 view
            """)
        
        with st.expander("System Overrides"):
            st.markdown("""
            **CEO Override Capabilities:**
            
            1. **Rate Override:**
               - Accept loads below $2.00/mile when strategic
               - Set custom rates for specific customers
            
            2. **Assignment Override:**
               - Assign any driver to any truck
               - Bypass HOS restrictions (with caution)
            
            3. **Payment Override:**
               - Adjust driver pay manually
               - Add bonuses or deductions
            
            4. **Status Override:**
               - Change any load status
               - Mark exceptions
            """)
    
    with tabs[2]:  # Driver Mode
        st.subheader("Driver Mode Training")
        
        st.info("""
        **To Switch to Driver Mode:**
        1. Click your name in sidebar
        2. Select "Driver Mode"
        3. Interface changes to driver view
        """)
        
        with st.expander("Managing Your Loads"):
            st.markdown("""
            **My Loads Dashboard Shows:**
            - Load number and details
            - Pickup/delivery locations
            - Times and appointments
            - Special instructions
            - Rate and miles
            
            **Status Updates:**
            1. "En Route to Pickup"
            2. "At Pickup"
            3. "Loading"
            4. "In Transit"
            5. "At Delivery"
            6. "Delivered"
            """)
        
        with st.expander("Document Upload Process"):
            st.markdown("""
            **Critical Documents to Upload:**
            
            1. **At Pickup:**
               - Take photo of unsigned BOL
               - Upload as "BOL - Unsigned"
               
            2. **After Loading:**
               - Get BOL signed by shipper
               - Take clear photo
               - Upload as "BOL - Signed"
               
            3. **At Delivery:**
               - Get POD signed
               - Take photo of delivered load (if required)
               - Upload immediately
               
            **Vector API Processing:**
            - Automatically converts photos to PDF
            - Indexes for easy retrieval
            - Links to load record
            """)
    
    with tabs[3]:  # Practice
        st.subheader("Practice Scenarios")
        
        scenario = st.selectbox(
            "Choose a scenario to practice:",
            [
                "Scenario 1: High-value load below target rate",
                "Scenario 2: Driver calls in sick",
                "Scenario 3: Month-end reporting",
                "Scenario 4: Setting new profit goals"
            ]
        )
        
        if "Scenario 1" in scenario:
            st.markdown("""
            ### Scenario: High-Value Load Below Target Rate
            
            **Situation:** 
            - Customer: FedEx (high-value contract)
            - Rate offered: $1.85/mile
            - Distance: 500 miles
            - Your target: $2.00/mile
            
            **Decision Points:**
            1. Is this a strategic customer?
            2. Will it position truck better?
            3. What's the opportunity cost?
            
            **CEO Actions:**
            1. Check truck's current position
            2. Review upcoming loads in that area
            3. Calculate total round-trip profitability
            4. Override if strategic
            
            **System Updates:**
            - Override logged in audit trail
            - Exception noted in reports
            - AI learns from decision
            """)
            
            decision = st.radio(
                "What would you do?",
                ["Accept - Strategic value", "Decline - Below target", "Counter at $2.00/mile"]
            )
            
            if st.button("Check Answer"):
                if decision == "Accept - Strategic value":
                    st.success("Correct! FedEx contract loads have priority and maintain relationship")
                else:
                    st.warning("Consider: Contract relationships sometimes outweigh per-load rates")
        
        if st.button("Complete Module 6", type="primary"):
            mark_module_complete("CEO Features")

# ===================================================================
# SIMPLIFIED MODULES (7-12)
# ===================================================================

def show_dispatcher_operations():
    st.header("Module 7: Dispatcher Operations")
    st.info("Training content for dispatcher operations - includes load booking, driver assignment, and negotiation tools")
    if st.button("Complete Module 7", type="primary"):
        mark_module_complete("Dispatcher Operations")

def show_driver_operations():
    st.header("Module 8: Driver Operations")
    st.info("Training content for driver operations - includes mobile app usage, document upload, and HOS management")
    if st.button("Complete Module 8", type="primary"):
        mark_module_complete("Driver Operations")

def show_financial_management():
    st.header("Module 9: Financial Management")
    st.info("Training content for financial management - includes invoicing, payments, and P&L reporting")
    if st.button("Complete Module 9", type="primary"):
        mark_module_complete("Financial Management")

def show_goal_setting():
    st.header("Module 10: Goal Setting & AI")
    st.info("Training content for AI-powered goal setting and performance optimization")
    if st.button("Complete Module 10", type="primary"):
        mark_module_complete("Goal Setting & AI")

def show_troubleshooting():
    st.header("Module 11: Troubleshooting")
    st.info("Common issues and solutions, error messages, and support contacts")
    if st.button("Complete Module 11", type="primary"):
        mark_module_complete("Troubleshooting")

def show_best_practices():
    st.header("Module 12: Best Practices")
    st.info("Industry best practices, workflow optimization, and efficiency tips")
    if st.button("Complete Module 12", type="primary"):
        mark_module_complete("Best Practices")

def show_database_setup():
    st.header("Module 4: Database Setup")
    st.info("Database initialization, backup procedures, and data management")
    if st.button("Complete Module 4", type="primary"):
        mark_module_complete("Database Setup")

def show_api_configuration():
    st.header("Module 5: API Configuration")
    st.info("Setting up Google Maps, GoMotive, Truckstop.com, and Vector APIs")
    if st.button("Complete Module 5", type="primary"):
        mark_module_complete("API Configuration")

# ===================================================================
# MAIN EXECUTION
# ===================================================================

if __name__ == "__main__":
    main()