"""
CEO Personal & Lifestyle Management Module
For managing both business and personal life of the Owner/CEO
"""
import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
from config.database import get_connection
import plotly.express as px
import plotly.graph_objects as go

def show_ceo_personal_management():
    """Main CEO personal management interface"""
    st.title("👔 CEO Personal & Lifestyle Management")
    
    # Check if user is CEO/Owner
    if st.session_state.get('username') != 'Brandon' and st.session_state.get('role') not in ['super_user', 'ceo']:
        st.error("❌ Access Denied: CEO Only")
        return
    
    # Create personal management tables
    init_personal_tables()
    
    # Main tabs for personal management
    tabs = st.tabs([
        "💰 Personal Finance",
        "🏠 Properties",
        "🚗 Personal Vehicles", 
        "💳 Credit Cards",
        "🏦 Bank Accounts",
        "📊 Investments",
        "🎯 Goals",
        "📅 Schedule",
        "👨‍👩‍👧‍👦 Family",
        "🏥 Health",
        "✈️ Travel",
        "📝 Personal Notes"
    ])
    
    with tabs[0]:
        manage_personal_finance()
    
    with tabs[1]:
        manage_properties()
    
    with tabs[2]:
        manage_personal_vehicles()
    
    with tabs[3]:
        manage_credit_cards()
    
    with tabs[4]:
        manage_bank_accounts()
    
    with tabs[5]:
        manage_investments()
    
    with tabs[6]:
        manage_goals()
    
    with tabs[7]:
        manage_schedule()
    
    with tabs[8]:
        manage_family()
    
    with tabs[9]:
        manage_health()
    
    with tabs[10]:
        manage_travel()
    
    with tabs[11]:
        manage_personal_notes()

def init_personal_tables():
    """Initialize all personal management tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Personal expenses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS personal_expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expense_date DATE NOT NULL,
        category TEXT NOT NULL,
        subcategory TEXT,
        description TEXT,
        amount DECIMAL(10,2) NOT NULL,
        payment_method TEXT,
        vendor TEXT,
        is_business_related BOOLEAN DEFAULT 0,
        is_tax_deductible BOOLEAN DEFAULT 0,
        receipt_path TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Personal income table
    cursor.execute('''CREATE TABLE IF NOT EXISTS personal_income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income_date DATE NOT NULL,
        source TEXT NOT NULL,
        category TEXT,
        amount DECIMAL(10,2) NOT NULL,
        is_taxable BOOLEAN DEFAULT 1,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Properties table
    cursor.execute('''CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_name TEXT NOT NULL,
        property_type TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        purchase_date DATE,
        purchase_price DECIMAL(12,2),
        current_value DECIMAL(12,2),
        mortgage_balance DECIMAL(12,2),
        monthly_payment DECIMAL(10,2),
        rental_income DECIMAL(10,2),
        property_tax DECIMAL(10,2),
        insurance_cost DECIMAL(10,2),
        notes TEXT,
        is_primary_residence BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Personal vehicles table
    cursor.execute('''CREATE TABLE IF NOT EXISTS personal_vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_type TEXT,
        make TEXT,
        model TEXT,
        year INTEGER,
        vin TEXT,
        license_plate TEXT,
        purchase_date DATE,
        purchase_price DECIMAL(10,2),
        current_value DECIMAL(10,2),
        loan_balance DECIMAL(10,2),
        monthly_payment DECIMAL(10,2),
        insurance_cost DECIMAL(10,2),
        registration_exp DATE,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Credit cards table
    cursor.execute('''CREATE TABLE IF NOT EXISTS credit_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        card_name TEXT NOT NULL,
        card_number_last4 TEXT,
        bank_name TEXT,
        credit_limit DECIMAL(10,2),
        current_balance DECIMAL(10,2),
        interest_rate DECIMAL(5,2),
        payment_due_date INTEGER,
        annual_fee DECIMAL(10,2),
        rewards_program TEXT,
        notes TEXT,
        is_business_card BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Bank accounts table
    cursor.execute('''CREATE TABLE IF NOT EXISTS bank_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_name TEXT NOT NULL,
        bank_name TEXT,
        account_type TEXT,
        account_number_last4 TEXT,
        current_balance DECIMAL(12,2),
        is_business_account BOOLEAN DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Investments table
    cursor.execute('''CREATE TABLE IF NOT EXISTS investments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        investment_type TEXT,
        investment_name TEXT,
        ticker_symbol TEXT,
        quantity DECIMAL(10,4),
        purchase_price DECIMAL(10,2),
        current_price DECIMAL(10,2),
        purchase_date DATE,
        broker TEXT,
        account_number TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Goals table
    cursor.execute('''CREATE TABLE IF NOT EXISTS personal_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_category TEXT,
        goal_title TEXT NOT NULL,
        description TEXT,
        target_amount DECIMAL(12,2),
        current_progress DECIMAL(12,2),
        target_date DATE,
        priority TEXT,
        status TEXT DEFAULT 'Active',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Family members table
    cursor.execute('''CREATE TABLE IF NOT EXISTS family_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        relationship TEXT,
        first_name TEXT,
        last_name TEXT,
        birth_date DATE,
        phone TEXT,
        email TEXT,
        ssn_last4 TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Health records table
    cursor.execute('''CREATE TABLE IF NOT EXISTS health_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_date DATE,
        record_type TEXT,
        provider TEXT,
        description TEXT,
        cost DECIMAL(10,2),
        insurance_covered DECIMAL(10,2),
        notes TEXT,
        family_member_id INTEGER REFERENCES family_members(id),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Travel records table
    cursor.execute('''CREATE TABLE IF NOT EXISTS travel_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_name TEXT,
        destination TEXT,
        departure_date DATE,
        return_date DATE,
        purpose TEXT,
        total_cost DECIMAL(10,2),
        is_business_trip BOOLEAN DEFAULT 0,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()

def manage_personal_finance():
    """Personal finance management"""
    st.header("💰 Personal Finance Overview")
    
    conn = get_connection()
    
    # Financial dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calculate total personal assets
        try:
            properties = pd.read_sql_query("SELECT SUM(current_value - mortgage_balance) as equity FROM properties", conn)
            vehicles = pd.read_sql_query("SELECT SUM(current_value - loan_balance) as equity FROM personal_vehicles", conn)
            bank = pd.read_sql_query("SELECT SUM(current_balance) as total FROM bank_accounts WHERE is_business_account = 0", conn)
            investments = pd.read_sql_query("SELECT SUM(quantity * current_price) as total FROM investments", conn)
            
            total_assets = (properties['equity'].iloc[0] or 0) + (vehicles['equity'].iloc[0] or 0) + \
                          (bank['total'].iloc[0] or 0) + (investments['total'].iloc[0] or 0)
            
            st.metric("Net Worth", f"${total_assets:,.2f}")
        except:
            st.metric("Net Worth", "$0.00")
    
    with col2:
        # Monthly income
        try:
            monthly_income = pd.read_sql_query("""
                SELECT SUM(amount) as total FROM personal_income 
                WHERE strftime('%Y-%m', income_date) = strftime('%Y-%m', 'now')
            """, conn)
            st.metric("Monthly Income", f"${monthly_income['total'].iloc[0] or 0:,.2f}")
        except:
            st.metric("Monthly Income", "$0.00")
    
    with col3:
        # Monthly expenses
        try:
            monthly_expenses = pd.read_sql_query("""
                SELECT SUM(amount) as total FROM personal_expenses 
                WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
            """, conn)
            st.metric("Monthly Expenses", f"${monthly_expenses['total'].iloc[0] or 0:,.2f}")
        except:
            st.metric("Monthly Expenses", "$0.00")
    
    with col4:
        # Credit card debt
        try:
            cc_debt = pd.read_sql_query("SELECT SUM(current_balance) as total FROM credit_cards", conn)
            st.metric("Credit Card Debt", f"${cc_debt['total'].iloc[0] or 0:,.2f}")
        except:
            st.metric("Credit Card Debt", "$0.00")
    
    # Add personal expense
    st.subheader("➕ Add Personal Expense")
    
    with st.form("add_personal_expense"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            expense_date = st.date_input("Date")
            category = st.selectbox("Category", [
                'Food & Dining', 'Shopping', 'Entertainment', 'Bills & Utilities',
                'Auto & Transport', 'Home', 'Family', 'Health & Fitness',
                'Travel', 'Education', 'Gifts & Donations', 'Investment',
                'Business Related', 'Taxes', 'Other'
            ])
            vendor = st.text_input("Vendor/Store")
        
        with col2:
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            payment_method = st.selectbox("Payment Method", [
                'Personal Card', 'Business Card', 'Cash', 'Check', 
                'Bank Transfer', 'Venmo', 'PayPal', 'Zelle'
            ])
            is_tax_deductible = st.checkbox("Tax Deductible")
        
        with col3:
            description = st.text_area("Description")
            is_business_related = st.checkbox("Business Related")
        
        if st.form_submit_button("💾 Save Expense"):
            if amount > 0:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO personal_expenses 
                        (expense_date, category, vendor, amount, payment_method, 
                         description, is_business_related, is_tax_deductible)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (expense_date, category, vendor, amount, payment_method,
                          description, is_business_related, is_tax_deductible))
                    conn.commit()
                    st.success(f"✅ Personal expense of ${amount:.2f} recorded!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Recent personal expenses
    st.subheader("Recent Personal Expenses")
    try:
        recent_expenses = pd.read_sql_query("""
            SELECT expense_date, category, vendor, amount, payment_method,
                   is_business_related, is_tax_deductible
            FROM personal_expenses
            ORDER BY expense_date DESC
            LIMIT 10
        """, conn)
        
        if not recent_expenses.empty:
            st.dataframe(recent_expenses)
        else:
            st.info("No personal expenses recorded yet")
    except Exception as e:
        st.error(f"Error loading expenses: {str(e)}")

def manage_properties():
    """Property management"""
    st.header("🏠 Property Portfolio")
    
    conn = get_connection()
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Property", use_container_width=True):
            st.session_state.show_add_property = True
    
    if st.session_state.get('show_add_property', False):
        with st.form("add_property"):
            st.subheader("Add New Property")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                property_name = st.text_input("Property Name*")
                property_type = st.selectbox("Type", [
                    'Primary Residence', 'Rental Property', 'Vacation Home',
                    'Commercial', 'Land', 'Other'
                ])
                address = st.text_input("Address")
                city = st.text_input("City")
                state = st.text_input("State")
            
            with col2:
                purchase_date = st.date_input("Purchase Date")
                purchase_price = st.number_input("Purchase Price", min_value=0.0)
                current_value = st.number_input("Current Value", min_value=0.0)
                mortgage_balance = st.number_input("Mortgage Balance", min_value=0.0)
            
            with col3:
                monthly_payment = st.number_input("Monthly Payment", min_value=0.0)
                rental_income = st.number_input("Rental Income", min_value=0.0)
                property_tax = st.number_input("Annual Property Tax", min_value=0.0)
                insurance_cost = st.number_input("Annual Insurance", min_value=0.0)
            
            if st.form_submit_button("Save Property"):
                if property_name:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO properties 
                            (property_name, property_type, address, city, state,
                             purchase_date, purchase_price, current_value, mortgage_balance,
                             monthly_payment, rental_income, property_tax, insurance_cost)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (property_name, property_type, address, city, state,
                              purchase_date, purchase_price, current_value, mortgage_balance,
                              monthly_payment, rental_income, property_tax, insurance_cost))
                        conn.commit()
                        st.success(f"Property {property_name} added!")
                        st.session_state.show_add_property = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display properties
    try:
        properties = pd.read_sql_query("""
            SELECT property_name, property_type, city, state,
                   current_value, mortgage_balance, 
                   (current_value - mortgage_balance) as equity,
                   rental_income, monthly_payment
            FROM properties
            ORDER BY property_name
        """, conn)
        
        if not properties.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Property Value", f"${properties['current_value'].sum():,.2f}")
            with col2:
                st.metric("Total Equity", f"${properties['equity'].sum():,.2f}")
            with col3:
                st.metric("Monthly Rental Income", f"${properties['rental_income'].sum():,.2f}")
            
            st.dataframe(properties)
        else:
            st.info("No properties added yet")
    except Exception as e:
        st.error(f"Error loading properties: {str(e)}")

def manage_personal_vehicles():
    """Personal vehicle management"""
    st.header("🚗 Personal Vehicles")
    
    conn = get_connection()
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add Vehicle", use_container_width=True):
            st.session_state.show_add_personal_vehicle = True
    
    if st.session_state.get('show_add_personal_vehicle', False):
        with st.form("add_personal_vehicle"):
            st.subheader("Add Personal Vehicle")
            
            col1, col2 = st.columns(2)
            
            with col1:
                vehicle_type = st.selectbox("Type", ['Car', 'Truck', 'SUV', 'Motorcycle', 'RV', 'Boat', 'Other'])
                make = st.text_input("Make")
                model = st.text_input("Model")
                year = st.number_input("Year", min_value=1900, max_value=2030)
            
            with col2:
                purchase_price = st.number_input("Purchase Price", min_value=0.0)
                current_value = st.number_input("Current Value", min_value=0.0)
                loan_balance = st.number_input("Loan Balance", min_value=0.0)
                monthly_payment = st.number_input("Monthly Payment", min_value=0.0)
            
            if st.form_submit_button("Save Vehicle"):
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO personal_vehicles 
                        (vehicle_type, make, model, year, purchase_price, 
                         current_value, loan_balance, monthly_payment)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (vehicle_type, make, model, year, purchase_price,
                          current_value, loan_balance, monthly_payment))
                    conn.commit()
                    st.success(f"Vehicle {make} {model} added!")
                    st.session_state.show_add_personal_vehicle = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

def manage_credit_cards():
    """Credit card management"""
    st.header("💳 Credit Cards")
    
    conn = get_connection()
    
    # Add credit card form
    with st.expander("➕ Add Credit Card"):
        with st.form("add_credit_card"):
            col1, col2 = st.columns(2)
            
            with col1:
                card_name = st.text_input("Card Name*")
                bank_name = st.text_input("Bank/Issuer")
                card_last4 = st.text_input("Last 4 Digits")
                credit_limit = st.number_input("Credit Limit", min_value=0.0)
            
            with col2:
                current_balance = st.number_input("Current Balance", min_value=0.0)
                interest_rate = st.number_input("Interest Rate %", min_value=0.0, max_value=100.0)
                annual_fee = st.number_input("Annual Fee", min_value=0.0)
                is_business = st.checkbox("Business Card")
            
            if st.form_submit_button("Save Card"):
                if card_name:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO credit_cards 
                            (card_name, bank_name, card_number_last4, credit_limit,
                             current_balance, interest_rate, annual_fee, is_business_card)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (card_name, bank_name, card_last4, credit_limit,
                              current_balance, interest_rate, annual_fee, is_business))
                        conn.commit()
                        st.success(f"Credit card {card_name} added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display credit cards
    try:
        cards = pd.read_sql_query("""
            SELECT card_name, bank_name, credit_limit, current_balance,
                   (credit_limit - current_balance) as available_credit,
                   interest_rate, is_business_card
            FROM credit_cards
            ORDER BY current_balance DESC
        """, conn)
        
        if not cards.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Credit Limit", f"${cards['credit_limit'].sum():,.2f}")
            with col2:
                st.metric("Total Balance", f"${cards['current_balance'].sum():,.2f}")
            with col3:
                utilization = (cards['current_balance'].sum() / cards['credit_limit'].sum() * 100) if cards['credit_limit'].sum() > 0 else 0
                st.metric("Utilization", f"{utilization:.1f}%")
            
            st.dataframe(cards)
        else:
            st.info("No credit cards added yet")
    except Exception as e:
        st.error(f"Error loading credit cards: {str(e)}")

def manage_bank_accounts():
    """Bank account management"""
    st.header("🏦 Bank Accounts")
    
    conn = get_connection()
    
    # Add bank account
    with st.expander("➕ Add Bank Account"):
        with st.form("add_bank_account"):
            col1, col2 = st.columns(2)
            
            with col1:
                account_name = st.text_input("Account Name*")
                bank_name = st.text_input("Bank Name")
                account_type = st.selectbox("Type", ['Checking', 'Savings', 'Money Market', 'CD', 'Other'])
            
            with col2:
                account_last4 = st.text_input("Last 4 Digits")
                current_balance = st.number_input("Current Balance", format="%.2f")
                is_business = st.checkbox("Business Account")
            
            if st.form_submit_button("Save Account"):
                if account_name:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO bank_accounts 
                            (account_name, bank_name, account_type, account_number_last4,
                             current_balance, is_business_account)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (account_name, bank_name, account_type, account_last4,
                              current_balance, is_business))
                        conn.commit()
                        st.success(f"Account {account_name} added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # Display accounts
    try:
        accounts = pd.read_sql_query("""
            SELECT account_name, bank_name, account_type, current_balance, is_business_account
            FROM bank_accounts
            ORDER BY current_balance DESC
        """, conn)
        
        if not accounts.empty:
            # Summary
            personal_total = accounts[accounts['is_business_account'] == 0]['current_balance'].sum()
            business_total = accounts[accounts['is_business_account'] == 1]['current_balance'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Personal Accounts", f"${personal_total:,.2f}")
            with col2:
                st.metric("Business Accounts", f"${business_total:,.2f}")
            with col3:
                st.metric("Total Cash", f"${personal_total + business_total:,.2f}")
            
            st.dataframe(accounts)
        else:
            st.info("No bank accounts added yet")
    except Exception as e:
        st.error(f"Error loading accounts: {str(e)}")

def manage_investments():
    """Investment portfolio management"""
    st.header("📊 Investment Portfolio")
    st.info("Track stocks, bonds, crypto, and other investments")

def manage_goals():
    """Personal and financial goals"""
    st.header("🎯 Goals & Objectives")
    
    conn = get_connection()
    
    # Add goal
    with st.expander("➕ Add New Goal"):
        with st.form("add_goal"):
            col1, col2 = st.columns(2)
            
            with col1:
                goal_title = st.text_input("Goal Title*")
                goal_category = st.selectbox("Category", [
                    'Financial', 'Business', 'Personal', 'Family', 
                    'Health', 'Education', 'Retirement', 'Other'
                ])
                target_amount = st.number_input("Target Amount ($)", min_value=0.0)
            
            with col2:
                target_date = st.date_input("Target Date")
                priority = st.selectbox("Priority", ['High', 'Medium', 'Low'])
                current_progress = st.number_input("Current Progress ($)", min_value=0.0)
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Save Goal"):
                if goal_title:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO personal_goals 
                            (goal_title, goal_category, target_amount, target_date,
                             priority, current_progress, description)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (goal_title, goal_category, target_amount, target_date,
                              priority, current_progress, description))
                        conn.commit()
                        st.success(f"Goal '{goal_title}' added!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

def manage_schedule():
    """Personal schedule and calendar"""
    st.header("📅 Personal Schedule")
    st.info("Manage appointments, meetings, and personal events")

def manage_family():
    """Family information management"""
    st.header("👨‍👩‍👧‍👦 Family Management")
    st.info("Track family member information, birthdays, and important dates")

def manage_health():
    """Health and medical records"""
    st.header("🏥 Health Records")
    st.info("Track medical appointments, prescriptions, and health expenses")

def manage_travel():
    """Travel planning and records"""
    st.header("✈️ Travel Management")
    st.info("Track personal and business travel")

def manage_personal_notes():
    """Personal notes and reminders"""
    st.header("📝 Personal Notes")
    
    conn = get_connection()
    
    # Create notes table if it doesn't exist
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS personal_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_date DATE,
            category TEXT,
            title TEXT,
            content TEXT,
            priority TEXT,
            is_reminder BOOLEAN DEFAULT 0,
            reminder_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
    except:
        pass
    
    st.info("Keep personal notes, ideas, and reminders")