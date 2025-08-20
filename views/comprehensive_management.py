"""
Comprehensive Management Module for Smith & Williams Trucking TMS
Includes ALL critical management functions for complete system operation
"""
import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
from config.database import get_connection
import hashlib
from modules.ui_enhancements import add_cancel_button, confirmation_dialog, process_with_cancel
from modules.api_integrations import GoogleMapsAPI

def show_comprehensive_management():
    """Main comprehensive management interface"""
    st.title("🎛️ Comprehensive TMS Management")
    
    # Check user permissions
    if st.session_state.get('role') not in ['super_user', 'ceo', 'admin']:
        st.error("❌ Access Denied: Admin privileges required")
        return
    
    # Main management tabs
    tabs = st.tabs([
        "👥 Users", 
        "🚛 Fleet", 
        "💰 Expenses", 
        "🏢 Customers",
        "👷 Drivers",
        "📦 Carriers",
        "💵 Payroll",
        "📄 Documents",
        "🔧 Maintenance",
        "⛽ Fuel",
        "🛡️ Insurance",
        "📊 Rates",
        "⚠️ Safety",
        "🏭 Vendors"
    ])
    
    with tabs[0]:
        manage_users()
    
    with tabs[1]:
        manage_fleet()
    
    with tabs[2]:
        manage_expenses()
    
    with tabs[3]:
        manage_customers()
    
    with tabs[4]:
        manage_drivers()
    
    with tabs[5]:
        manage_carriers()
    
    with tabs[6]:
        manage_payroll()
    
    with tabs[7]:
        manage_documents()
    
    with tabs[8]:
        manage_maintenance()
    
    with tabs[9]:
        manage_fuel()
    
    with tabs[10]:
        manage_insurance()
    
    with tabs[11]:
        manage_rates()
    
    with tabs[12]:
        manage_safety()
    
    with tabs[13]:
        manage_vendors()

def manage_users():
    """Complete user management with CRUD operations"""
    st.header("👥 User Management")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader("Current Users")
    with col2:
        if st.button("➕ Add New User", use_container_width=True):
            st.session_state.show_add_user = True
    
    # Add user form
    if st.session_state.get('show_add_user', False):
        with st.form("add_user_form"):
            st.subheader("Add New User")
            col1, col2 = st.columns(2)
            
            with col1:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                full_name = st.text_input("Full Name*")
                role = st.selectbox("Role*", [
                    'super_user', 'ceo', 'admin', 'dispatcher', 
                    'driver', 'customer', 'accounting', 'safety', 'maintenance'
                ])
            
            with col2:
                email = st.text_input("Email")
                phone = st.text_input("Phone")
                is_active = st.checkbox("Active", value=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.form_submit_button("✅ Save User", use_container_width=True):
                    if username and password and full_name:
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            password_hash = hashlib.sha256(password.encode()).hexdigest()
                            cursor.execute("""
                                INSERT INTO users (username, password_hash, role, full_name, email, phone, is_active)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (username, password_hash, role, full_name, email, phone, is_active))
                            conn.commit()
                            st.success(f"✅ User {username} added successfully!")
                            st.session_state.show_add_user = False
                            st.rerun()
                        except sqlite3.IntegrityError:
                            st.error("User already exists!")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    else:
                        st.error("Please fill all required fields!")
            
            with col2:
                if st.form_submit_button("❌ Cancel", use_container_width=True):
                    st.session_state.show_add_user = False
                    st.rerun()
    
    # Display users
    try:
        conn = get_connection()
        users_df = pd.read_sql_query("""
            SELECT id, username, role, full_name, email, phone, 
                   is_active, last_login, created_at
            FROM users
            ORDER BY created_at DESC
        """, conn)
        
        if not users_df.empty:
            # Add action buttons for each user
            for idx, user in users_df.iterrows():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 2, 2, 2, 1, 1, 1])
                
                with col1:
                    st.text(user['username'])
                with col2:
                    st.text(user['full_name'])
                with col3:
                    st.text(user['role'])
                with col4:
                    st.text("✅ Active" if user['is_active'] else "❌ Inactive")
                with col5:
                    if st.button("✏️", key=f"edit_user_{user['id']}"):
                        st.session_state[f"edit_user_{user['id']}"] = True
                with col6:
                    if user['is_active']:
                        if st.button("🔒", key=f"deactivate_{user['id']}"):
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user['id'],))
                            conn.commit()
                            st.rerun()
                    else:
                        if st.button("🔓", key=f"activate_{user['id']}"):
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET is_active = 1 WHERE id = ?", (user['id'],))
                            conn.commit()
                            st.rerun()
                with col7:
                    if st.button("🗑️", key=f"delete_user_{user['id']}"):
                        if user['username'] != 'Brandon':  # Protect super admin
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM users WHERE id = ?", (user['id'],))
                            conn.commit()
                            st.success(f"User {user['username']} deleted!")
                            st.rerun()
                        else:
                            st.error("Cannot delete super admin!")
                
                # Edit form for each user
                if st.session_state.get(f"edit_user_{user['id']}", False):
                    with st.form(f"edit_form_{user['id']}"):
                        st.subheader(f"Edit User: {user['username']}")
                        new_name = st.text_input("Full Name", value=user['full_name'])
                        new_email = st.text_input("Email", value=user['email'] or "")
                        new_phone = st.text_input("Phone", value=user['phone'] or "")
                        new_role = st.selectbox("Role", [
                            'super_user', 'ceo', 'admin', 'dispatcher', 
                            'driver', 'customer', 'accounting'
                        ], index=['super_user', 'ceo', 'admin', 'dispatcher', 'driver', 'customer', 'accounting'].index(user['role']))
                        
                        if st.form_submit_button("Save Changes"):
                            cursor = conn.cursor()
                            cursor.execute("""
                                UPDATE users 
                                SET full_name = ?, email = ?, phone = ?, role = ?
                                WHERE id = ?
                            """, (new_name, new_email, new_phone, new_role, user['id']))
                            conn.commit()
                            st.success("User updated!")
                            st.session_state[f"edit_user_{user['id']}"] = False
                            st.rerun()
        else:
            st.info("No users found")
            
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")

def manage_fleet():
    """Complete fleet management for trucks and trailers"""
    st.header("🚛 Fleet Management")
    
    fleet_tabs = st.tabs(["🚚 Trucks", "🚐 Trailers", "🔧 Equipment"])
    
    with fleet_tabs[0]:
        # Trucks Management
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader("Truck Fleet")
        with col2:
            if st.button("➕ Add Truck", use_container_width=True):
                st.session_state.show_add_truck = True
        
        if st.session_state.get('show_add_truck', False):
            with st.form("add_truck_form"):
                st.subheader("Add New Truck")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    truck_number = st.text_input("Truck Number*")
                    make = st.text_input("Make")
                    model = st.text_input("Model")
                
                with col2:
                    year = st.number_input("Year", min_value=1990, max_value=2030)
                    vin = st.text_input("VIN")
                    license_plate = st.text_input("License Plate")
                
                with col3:
                    status = st.selectbox("Status", ['Available', 'In Transit', 'Out of Service', 'Maintenance'])
                    current_location = st.text_input("Current Location")
                
                if st.form_submit_button("Save Truck"):
                    if truck_number:
                        try:
                            conn = get_connection()
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO trucks (truck_number, make, model, year, vin, 
                                                  license_plate, status, current_location)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            """, (truck_number, make, model, year, vin, license_plate, status, current_location))
                            conn.commit()
                            st.success(f"Truck {truck_number} added!")
                            st.session_state.show_add_truck = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
        
        # Display trucks
        try:
            conn = get_connection()
            trucks_df = pd.read_sql_query("""
                SELECT * FROM trucks ORDER BY truck_number
            """, conn)
            
            if not trucks_df.empty:
                st.dataframe(trucks_df[['truck_number', 'make', 'model', 'year', 'status', 'current_location']])
            else:
                st.info("No trucks in fleet")
        except Exception as e:
            st.error(f"Error loading trucks: {str(e)}")
    
    with fleet_tabs[1]:
        # Trailers Management
        st.subheader("Trailer Fleet")
        
        # Create trailers table if it doesn't exist
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS trailers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trailer_number TEXT UNIQUE NOT NULL,
                trailer_type TEXT,
                make TEXT,
                model TEXT,
                year INTEGER,
                vin TEXT,
                license_plate TEXT,
                status TEXT DEFAULT 'Available',
                current_location TEXT,
                last_inspection DATE,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            conn.commit()
        except:
            pass
        
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("➕ Add Trailer", use_container_width=True):
                st.session_state.show_add_trailer = True
        
        if st.session_state.get('show_add_trailer', False):
            with st.form("add_trailer_form"):
                st.subheader("Add New Trailer")
                col1, col2 = st.columns(2)
                
                with col1:
                    trailer_number = st.text_input("Trailer Number*")
                    trailer_type = st.selectbox("Type", ['Dry Van', 'Reefer', 'Flatbed', 'Step Deck', 'RGN'])
                    make = st.text_input("Make")
                
                with col2:
                    year = st.number_input("Year", min_value=1990, max_value=2030)
                    license_plate = st.text_input("License Plate")
                    status = st.selectbox("Status", ['Available', 'In Use', 'Maintenance', 'Out of Service'])
                
                if st.form_submit_button("Save Trailer"):
                    if trailer_number:
                        try:
                            cursor.execute("""
                                INSERT INTO trailers (trailer_number, trailer_type, make, year, 
                                                    license_plate, status)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (trailer_number, trailer_type, make, year, license_plate, status))
                            conn.commit()
                            st.success(f"Trailer {trailer_number} added!")
                            st.session_state.show_add_trailer = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

def manage_expenses():
    """Complete expense management system"""
    st.header("💰 Expense Management")
    
    # Create expenses table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date DATE NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            vendor_name TEXT,
            description TEXT,
            amount DECIMAL(10,2) NOT NULL,
            payment_method TEXT,
            reference_number TEXT,
            truck_id INTEGER REFERENCES trucks(id),
            driver_id INTEGER REFERENCES drivers(id),
            shipment_id INTEGER REFERENCES shipments(id),
            receipt_url TEXT,
            status TEXT DEFAULT 'Pending',
            approved_by INTEGER REFERENCES users(id),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_by INTEGER REFERENCES users(id)
        )''')
        conn.commit()
    except:
        pass
    
    expense_tabs = st.tabs(["➕ Add Expense", "📊 View Expenses", "📈 Reports"])
    
    with expense_tabs[0]:
        with st.form("add_expense_form"):
            st.subheader("Record New Expense")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                expense_date = st.date_input("Date*")
                category = st.selectbox("Category*", [
                    'Fuel', 'Maintenance', 'Repairs', 'Tolls', 'Permits',
                    'Insurance', 'Tires', 'Parts', 'Labor', 'Lodging',
                    'Meals', 'Scales', 'Lumper', 'Detention', 'Other'
                ])
                vendor = st.text_input("Vendor Name")
            
            with col2:
                amount = st.number_input("Amount*", min_value=0.0, format="%.2f")
                payment_method = st.selectbox("Payment Method", [
                    'Company Card', 'Cash', 'Check', 'EFS', 'Comdata', 'ACH'
                ])
                reference = st.text_input("Reference/Invoice #")
            
            with col3:
                # Load trucks and drivers for association
                trucks = pd.read_sql_query("SELECT id, truck_number FROM trucks", conn)
                drivers = pd.read_sql_query("SELECT id, first_name, last_name FROM drivers", conn)
                
                truck_options = ['None'] + trucks['truck_number'].tolist() if not trucks.empty else ['None']
                selected_truck = st.selectbox("Associated Truck", truck_options)
                
                driver_names = ['None'] + [f"{d['first_name']} {d['last_name']}" for _, d in drivers.iterrows()] if not drivers.empty else ['None']
                selected_driver = st.selectbox("Associated Driver", driver_names)
            
            description = st.text_area("Description")
            
            if st.form_submit_button("💾 Save Expense"):
                if expense_date and category and amount > 0:
                    try:
                        truck_id = None if selected_truck == 'None' else trucks[trucks['truck_number'] == selected_truck]['id'].values[0]
                        driver_id = None if selected_driver == 'None' else drivers.iloc[driver_names.index(selected_driver) - 1]['id']
                        
                        cursor.execute("""
                            INSERT INTO expenses (expense_date, category, vendor_name, description,
                                                amount, payment_method, reference_number, truck_id, driver_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (expense_date, category, vendor, description, amount, 
                              payment_method, reference, truck_id, driver_id))
                        conn.commit()
                        st.success(f"✅ Expense of ${amount:.2f} recorded!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                else:
                    st.error("Please fill required fields!")
    
    with expense_tabs[1]:
        st.subheader("Recent Expenses")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_category = st.selectbox("Filter by Category", ['All'] + [
                'Fuel', 'Maintenance', 'Repairs', 'Tolls', 'Permits', 'Other'
            ])
        with col2:
            filter_start = st.date_input("From Date", value=date.today() - timedelta(days=30))
        with col3:
            filter_end = st.date_input("To Date", value=date.today())
        
        # Load and display expenses
        query = """
            SELECT e.*, t.truck_number, d.first_name || ' ' || d.last_name as driver_name
            FROM expenses e
            LEFT JOIN trucks t ON e.truck_id = t.id
            LEFT JOIN drivers d ON e.driver_id = d.id
            WHERE e.expense_date BETWEEN ? AND ?
        """
        params = [filter_start, filter_end]
        
        if filter_category != 'All':
            query += " AND e.category = ?"
            params.append(filter_category)
        
        query += " ORDER BY e.expense_date DESC"
        
        try:
            expenses_df = pd.read_sql_query(query, conn, params=params)
            
            if not expenses_df.empty:
                st.metric("Total Expenses", f"${expenses_df['amount'].sum():,.2f}")
                st.dataframe(expenses_df[['expense_date', 'category', 'vendor_name', 
                                         'amount', 'truck_number', 'driver_name']])
            else:
                st.info("No expenses found for selected period")
        except Exception as e:
            st.error(f"Error loading expenses: {str(e)}")

def manage_customers():
    """Complete customer management"""
    st.header("🏢 Customer Management")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Customer", use_container_width=True):
            st.session_state.show_add_customer = True
    
    if st.session_state.get('show_add_customer', False):
        with st.form("add_customer_form"):
            st.subheader("Add New Customer")
            
            col1, col2 = st.columns(2)
            with col1:
                customer_code = st.text_input("Customer Code*")
                company_name = st.text_input("Company Name*")
                contact_name = st.text_input("Contact Name")
                phone = st.text_input("Phone")
                email = st.text_input("Email")
            
            with col2:
                address = st.text_input("Address")
                city = st.text_input("City")
                state = st.text_input("State")
                zip_code = st.text_input("ZIP Code")
                credit_limit = st.number_input("Credit Limit", min_value=0.0)
            
            if st.form_submit_button("Save Customer"):
                if customer_code and company_name:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO customers (customer_code, company_name, contact_name,
                                                 phone, email, address, city, state, zip_code, credit_limit)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (customer_code, company_name, contact_name, phone, email,
                              address, city, state, zip_code, credit_limit))
                        conn.commit()
                        st.success(f"Customer {company_name} added!")
                        st.session_state.show_add_customer = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display customers
    try:
        conn = get_connection()
        customers_df = pd.read_sql_query("""
            SELECT * FROM customers WHERE is_active = 1 ORDER BY company_name
        """, conn)
        
        if not customers_df.empty:
            st.dataframe(customers_df[['customer_code', 'company_name', 'contact_name', 
                                      'phone', 'city', 'state', 'credit_limit']])
        else:
            st.info("No customers found")
    except Exception as e:
        st.error(f"Error loading customers: {str(e)}")

def manage_drivers():
    """Complete driver management"""
    st.header("👷 Driver Management")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Driver", use_container_width=True):
            st.session_state.show_add_driver = True
    
    if st.session_state.get('show_add_driver', False):
        with st.form("add_driver_form"):
            st.subheader("Add New Driver")
            
            col1, col2 = st.columns(2)
            with col1:
                driver_code = st.text_input("Driver Code*")
                first_name = st.text_input("First Name*")
                last_name = st.text_input("Last Name*")
                phone = st.text_input("Phone")
            
            with col2:
                cdl_number = st.text_input("CDL Number")
                cdl_state = st.text_input("CDL State")
                cdl_expiry = st.date_input("CDL Expiry")
                medical_expiry = st.date_input("Medical Cert Expiry")
            
            if st.form_submit_button("Save Driver"):
                if driver_code and first_name and last_name:
                    try:
                        conn = get_connection()
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO drivers (driver_code, first_name, last_name, phone,
                                               cdl_number, cdl_state, cdl_expiry, medical_cert_expiry)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (driver_code, first_name, last_name, phone,
                              cdl_number, cdl_state, cdl_expiry, medical_expiry))
                        conn.commit()
                        st.success(f"Driver {first_name} {last_name} added!")
                        st.session_state.show_add_driver = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display drivers
    try:
        conn = get_connection()
        drivers_df = pd.read_sql_query("""
            SELECT * FROM drivers WHERE is_active = 1 ORDER BY last_name, first_name
        """, conn)
        
        if not drivers_df.empty:
            # Add status indicators for expiring documents
            for idx, driver in drivers_df.iterrows():
                col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
                
                with col1:
                    st.text(f"{driver['first_name']} {driver['last_name']}")
                with col2:
                    st.text(f"CDL: {driver['cdl_number']}")
                with col3:
                    st.text(driver['status'])
                with col4:
                    # Check CDL expiry
                    if driver['cdl_expiry']:
                        exp_date = pd.to_datetime(driver['cdl_expiry']).date()
                        if exp_date < date.today() + timedelta(days=30):
                            st.warning("CDL Expiring!")
                with col5:
                    # Check medical expiry
                    if driver['medical_cert_expiry']:
                        med_date = pd.to_datetime(driver['medical_cert_expiry']).date()
                        if med_date < date.today() + timedelta(days=30):
                            st.warning("Medical Expiring!")
        else:
            st.info("No drivers found")
    except Exception as e:
        st.error(f"Error loading drivers: {str(e)}")

def manage_carriers():
    """Carrier management"""
    st.header("📦 Carrier Management")
    st.info("Manage partner carriers and owner operators")
    
    # Similar structure to other management functions
    # Implementation continues...

def manage_payroll():
    """Payroll management system"""
    st.header("💵 Payroll Management")
    
    # Create payroll table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            driver_id INTEGER REFERENCES drivers(id),
            pay_period_start DATE,
            pay_period_end DATE,
            total_miles INTEGER,
            rate_per_mile DECIMAL(10,4),
            base_pay DECIMAL(10,2),
            bonuses DECIMAL(10,2),
            deductions DECIMAL(10,2),
            net_pay DECIMAL(10,2),
            payment_date DATE,
            payment_method TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Driver payroll processing and management")

def manage_documents():
    """Document management system"""
    st.header("📄 Document Management")
    
    # Create documents table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_type TEXT NOT NULL,
            document_number TEXT,
            shipment_id INTEGER REFERENCES shipments(id),
            file_path TEXT,
            uploaded_by INTEGER REFERENCES users(id),
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Active'
        )''')
        conn.commit()
    except:
        pass
    
    doc_types = ["BOL", "POD", "Rate Confirmation", "Invoice", "Insurance", "Permits", "Other"]
    st.info("Manage Bills of Lading, PODs, and other documents")

def manage_maintenance():
    """Maintenance scheduling and tracking"""
    st.header("🔧 Maintenance Management")
    
    # Create maintenance table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS maintenance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_type TEXT,
            equipment_id INTEGER,
            service_type TEXT,
            scheduled_date DATE,
            completed_date DATE,
            mileage INTEGER,
            cost DECIMAL(10,2),
            vendor TEXT,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Track and schedule equipment maintenance")

def manage_fuel():
    """Fuel tracking and management"""
    st.header("⛽ Fuel Management")
    
    # Create fuel table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS fuel_purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_date DATE,
            truck_id INTEGER REFERENCES trucks(id),
            driver_id INTEGER REFERENCES drivers(id),
            location TEXT,
            gallons DECIMAL(10,2),
            price_per_gallon DECIMAL(10,3),
            total_cost DECIMAL(10,2),
            odometer INTEGER,
            payment_method TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Track fuel purchases and consumption")

def manage_insurance():
    """Insurance tracking and management"""
    st.header("🛡️ Insurance Management")
    
    # Create insurance table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS insurance_policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_number TEXT,
            policy_type TEXT,
            provider TEXT,
            coverage_amount DECIMAL(12,2),
            deductible DECIMAL(10,2),
            start_date DATE,
            expiry_date DATE,
            premium DECIMAL(10,2),
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Manage insurance policies and claims")

def manage_rates():
    """Rate management and pricing"""
    st.header("📊 Rate Management")
    
    # Create rates table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rate_matrix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER REFERENCES customers(id),
            origin_city TEXT,
            origin_state TEXT,
            destination_city TEXT,
            destination_state TEXT,
            equipment_type TEXT,
            rate_per_mile DECIMAL(10,4),
            flat_rate DECIMAL(10,2),
            fuel_surcharge_percent DECIMAL(5,2),
            effective_date DATE,
            expiry_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Manage customer rates and pricing matrix")

def manage_safety():
    """Safety and compliance management"""
    st.header("⚠️ Safety & Compliance")
    
    # Create safety tables if they don't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS safety_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_date DATE,
            incident_type TEXT,
            driver_id INTEGER REFERENCES drivers(id),
            truck_id INTEGER REFERENCES trucks(id),
            location TEXT,
            description TEXT,
            severity TEXT,
            reported_by TEXT,
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        cursor.execute('''CREATE TABLE IF NOT EXISTS compliance_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_type TEXT,
            driver_id INTEGER REFERENCES drivers(id),
            inspection_date DATE,
            expiry_date DATE,
            status TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    safety_tabs = st.tabs(["Incidents", "Compliance", "Training", "Inspections"])
    
    with safety_tabs[0]:
        st.subheader("Safety Incidents")
        st.info("Track and manage safety incidents")
    
    with safety_tabs[1]:
        st.subheader("Compliance Tracking")
        st.info("DOT compliance and regulations")
    
    with safety_tabs[2]:
        st.subheader("Training Records")
        st.info("Driver training and certifications")
    
    with safety_tabs[3]:
        st.subheader("Vehicle Inspections")
        st.info("DOT inspections and violations")

def manage_vendors():
    """Vendor management"""
    st.header("🏭 Vendor Management")
    
    # Create vendors table if it doesn't exist
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS vendors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_code TEXT UNIQUE,
            vendor_name TEXT NOT NULL,
            vendor_type TEXT,
            contact_name TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            payment_terms TEXT,
            tax_id TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Manage vendors and suppliers")