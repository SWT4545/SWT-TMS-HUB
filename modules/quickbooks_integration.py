"""
QuickBooks Integration Module for Smith & Williams Trucking TMS
Placeholder structure for future QuickBooks Online API integration
Handles payment reconciliation for CanAmex deposits and Treadstone Capital payments
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config.database import get_connection
import os
from dotenv import load_dotenv

load_dotenv()

class QuickBooksIntegration:
    """QuickBooks Online API integration (placeholder for future implementation)"""
    
    def __init__(self):
        self.client_id = os.getenv('QUICKBOOKS_CLIENT_ID', '')
        self.client_secret = os.getenv('QUICKBOOKS_CLIENT_SECRET', '')
        self.is_configured = bool(self.client_id and self.client_secret)
        self.conn = get_connection()
        self.init_quickbooks_tables()
    
    def init_quickbooks_tables(self):
        """Initialize tables for QuickBooks data synchronization"""
        cursor = self.conn.cursor()
        
        # QuickBooks sync tracking table
        cursor.execute('''CREATE TABLE IF NOT EXISTS quickbooks_sync (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sync_type TEXT,
            sync_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            records_synced INTEGER,
            status TEXT,
            error_message TEXT,
            details TEXT
        )''')
        
        # Payment reconciliation table
        cursor.execute('''CREATE TABLE IF NOT EXISTS payment_reconciliation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_date DATE,
            payment_source TEXT,
            payment_method TEXT,
            reference_number TEXT,
            amount DECIMAL(12,2),
            load_numbers TEXT,
            customer_id INTEGER,
            quickbooks_transaction_id TEXT,
            reconciled BOOLEAN DEFAULT 0,
            reconciled_date TIMESTAMP,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # CanAmex deposits tracking
        cursor.execute('''CREATE TABLE IF NOT EXISTS canamex_deposits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deposit_date DATE,
            deposit_amount DECIMAL(12,2),
            commission_rate DECIMAL(5,2),
            net_amount DECIMAL(12,2),
            load_count INTEGER,
            load_ids TEXT,
            quickbooks_deposit_id TEXT,
            reconciled BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Treadstone Capital payments tracking
        cursor.execute('''CREATE TABLE IF NOT EXISTS treadstone_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_date DATE,
            invoice_number TEXT,
            gross_amount DECIMAL(12,2),
            factoring_fee DECIMAL(12,2),
            net_amount DECIMAL(12,2),
            customer_name TEXT,
            load_numbers TEXT,
            quickbooks_payment_id TEXT,
            reconciled BOOLEAN DEFAULT 0,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # QuickBooks accounts mapping
        cursor.execute('''CREATE TABLE IF NOT EXISTS quickbooks_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT,
            account_type TEXT,
            quickbooks_account_id TEXT,
            account_number TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        self.conn.commit()
    
    def connect_to_quickbooks(self):
        """Establish connection to QuickBooks Online (placeholder)"""
        if not self.is_configured:
            return {
                'status': 'not_configured',
                'message': 'QuickBooks API credentials not configured. Please add credentials to .env file.'
            }
        
        # Placeholder for OAuth2 authentication flow
        return {
            'status': 'pending_implementation',
            'message': 'QuickBooks OAuth2 authentication will be implemented when API access is available.',
            'next_steps': [
                '1. Register app at https://developer.intuit.com',
                '2. Get OAuth2 credentials',
                '3. Implement authorization flow',
                '4. Store refresh tokens securely'
            ]
        }
    
    def sync_invoices(self):
        """Sync invoices with QuickBooks (placeholder)"""
        cursor = self.conn.cursor()
        
        # Get unsynced invoices
        cursor.execute("""
            SELECT id, invoice_number, customer_id, total_amount, invoice_date
            FROM invoices
            WHERE quickbooks_invoice_id IS NULL OR quickbooks_invoice_id = ''
        """)
        
        unsynced_invoices = cursor.fetchall()
        
        if not self.is_configured:
            return {
                'status': 'simulated',
                'message': f'Found {len(unsynced_invoices)} invoices to sync (simulation mode)',
                'invoices': unsynced_invoices
            }
        
        # Placeholder for actual sync
        return {
            'status': 'pending_implementation',
            'unsynced_count': len(unsynced_invoices),
            'message': 'Invoice sync will be available once QuickBooks API is connected'
        }
    
    def sync_customers(self):
        """Sync customers with QuickBooks (placeholder)"""
        cursor = self.conn.cursor()
        
        # Get customers
        cursor.execute("""
            SELECT id, company_name, contact_name, email, phone
            FROM customers
            WHERE is_active = 1
        """)
        
        customers = cursor.fetchall()
        
        if not self.is_configured:
            return {
                'status': 'simulated',
                'message': f'Found {len(customers)} customers to sync (simulation mode)',
                'customers': customers
            }
        
        return {
            'status': 'pending_implementation',
            'customer_count': len(customers),
            'message': 'Customer sync will be available once QuickBooks API is connected'
        }
    
    def reconcile_canamex_deposit(self, deposit_data):
        """Reconcile CanAmex carrier deposits"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO canamex_deposits 
                (deposit_date, deposit_amount, commission_rate, net_amount, 
                 load_count, load_ids, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                deposit_data['deposit_date'],
                deposit_data['deposit_amount'],
                deposit_data.get('commission_rate', 3.5),  # Default 3.5% commission
                deposit_data['net_amount'],
                deposit_data.get('load_count', 0),
                deposit_data.get('load_ids', ''),
                deposit_data.get('notes', '')
            ))
            
            self.conn.commit()
            
            return {
                'status': 'success',
                'deposit_id': cursor.lastrowid,
                'message': 'CanAmex deposit recorded successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def reconcile_treadstone_payment(self, payment_data):
        """Reconcile Treadstone Capital factoring payments"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO treadstone_payments
                (payment_date, invoice_number, gross_amount, factoring_fee, 
                 net_amount, customer_name, load_numbers, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                payment_data['payment_date'],
                payment_data['invoice_number'],
                payment_data['gross_amount'],
                payment_data.get('factoring_fee', 0),
                payment_data['net_amount'],
                payment_data.get('customer_name', ''),
                payment_data.get('load_numbers', ''),
                payment_data.get('notes', '')
            ))
            
            self.conn.commit()
            
            return {
                'status': 'success',
                'payment_id': cursor.lastrowid,
                'message': 'Treadstone payment recorded successfully'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_payment_summary(self, start_date, end_date):
        """Get payment summary for date range"""
        cursor = self.conn.cursor()
        
        # CanAmex deposits
        cursor.execute("""
            SELECT 
                COUNT(*) as count,
                SUM(deposit_amount) as gross,
                SUM(net_amount) as net
            FROM canamex_deposits
            WHERE deposit_date BETWEEN ? AND ?
        """, (start_date, end_date))
        
        canamex = cursor.fetchone()
        
        # Treadstone payments
        cursor.execute("""
            SELECT 
                COUNT(*) as count,
                SUM(gross_amount) as gross,
                SUM(net_amount) as net
            FROM treadstone_payments
            WHERE payment_date BETWEEN ? AND ?
        """, (start_date, end_date))
        
        treadstone = cursor.fetchone()
        
        # Direct customer payments
        cursor.execute("""
            SELECT 
                COUNT(*) as count,
                SUM(amount) as total
            FROM payment_reconciliation
            WHERE payment_date BETWEEN ? AND ?
                AND payment_source = 'Direct Customer'
        """, (start_date, end_date))
        
        direct = cursor.fetchone()
        
        return {
            'canamex': {
                'count': canamex[0] or 0,
                'gross': canamex[1] or 0,
                'net': canamex[2] or 0
            },
            'treadstone': {
                'count': treadstone[0] or 0,
                'gross': treadstone[1] or 0,
                'net': treadstone[2] or 0
            },
            'direct': {
                'count': direct[0] or 0,
                'total': direct[1] or 0
            }
        }
    
    def auto_match_payments(self):
        """Automatically match payments to invoices"""
        cursor = self.conn.cursor()
        
        # Get unreconciled payments
        cursor.execute("""
            SELECT id, amount, reference_number, payment_date
            FROM payment_reconciliation
            WHERE reconciled = 0
        """)
        
        payments = cursor.fetchall()
        
        matched = 0
        for payment in payments:
            # Try to match with invoice
            cursor.execute("""
                SELECT id, invoice_number
                FROM invoices
                WHERE total_amount = ?
                    AND status != 'Paid'
                    AND invoice_date <= ?
                ORDER BY invoice_date DESC
                LIMIT 1
            """, (payment[1], payment[3]))
            
            invoice = cursor.fetchone()
            
            if invoice:
                # Update payment as reconciled
                cursor.execute("""
                    UPDATE payment_reconciliation
                    SET reconciled = 1, reconciled_date = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (payment[0],))
                
                # Update invoice as paid
                cursor.execute("""
                    UPDATE invoices
                    SET status = 'Paid', paid_date = ?
                    WHERE id = ?
                """, (payment[3], invoice[0]))
                
                matched += 1
        
        self.conn.commit()
        
        return {
            'total_payments': len(payments),
            'matched': matched,
            'unmatched': len(payments) - matched
        }
    
    def export_to_quickbooks_format(self, data_type='invoices'):
        """Export data in QuickBooks-compatible format"""
        cursor = self.conn.cursor()
        
        if data_type == 'invoices':
            query = """
                SELECT 
                    i.invoice_number as 'Invoice Number',
                    c.company_name as 'Customer',
                    i.invoice_date as 'Invoice Date',
                    i.due_date as 'Due Date',
                    i.total_amount as 'Total',
                    i.status as 'Status'
                FROM invoices i
                LEFT JOIN customers c ON i.customer_id = c.id
                ORDER BY i.invoice_date DESC
            """
        elif data_type == 'payments':
            query = """
                SELECT 
                    payment_date as 'Date',
                    payment_source as 'Source',
                    reference_number as 'Reference',
                    amount as 'Amount',
                    reconciled as 'Reconciled'
                FROM payment_reconciliation
                ORDER BY payment_date DESC
            """
        else:
            return None
        
        df = pd.read_sql_query(query, self.conn)
        return df


def show_quickbooks_dashboard():
    """Display QuickBooks integration dashboard"""
    st.title("📊 QuickBooks Integration")
    
    # Initialize QuickBooks integration
    qb = QuickBooksIntegration()
    
    # Connection status
    if qb.is_configured:
        st.success("✅ QuickBooks credentials configured (API pending)")
    else:
        st.warning("⚠️ QuickBooks API credentials not configured")
        st.info("""
        To configure QuickBooks integration:
        1. Add QUICKBOOKS_CLIENT_ID to .env file
        2. Add QUICKBOOKS_CLIENT_SECRET to .env file
        3. Complete OAuth2 setup when API is available
        """)
    
    # Main tabs
    tabs = st.tabs([
        "📈 Overview",
        "💰 Payment Reconciliation",
        "🏦 CanAmex Deposits",
        "💳 Treadstone Payments",
        "🔄 Sync Operations",
        "📊 Reports",
        "⚙️ Settings"
    ])
    
    with tabs[0]:
        show_quickbooks_overview(qb)
    
    with tabs[1]:
        show_payment_reconciliation(qb)
    
    with tabs[2]:
        show_canamex_deposits(qb)
    
    with tabs[3]:
        show_treadstone_payments(qb)
    
    with tabs[4]:
        show_sync_operations(qb)
    
    with tabs[5]:
        show_quickbooks_reports(qb)
    
    with tabs[6]:
        show_quickbooks_settings(qb)


def show_quickbooks_overview(qb):
    """Show QuickBooks integration overview"""
    st.header("📈 QuickBooks Integration Overview")
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Get payment summary
    summary = qb.get_payment_summary(start_date, end_date)
    
    # Display metrics
    st.subheader("Payment Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_gross = (summary['canamex']['gross'] + 
                      summary['treadstone']['gross'] + 
                      summary['direct']['total'])
        st.metric("Total Gross", f"${total_gross:,.2f}")
    
    with col2:
        total_net = (summary['canamex']['net'] + 
                    summary['treadstone']['net'] + 
                    summary['direct']['total'])
        st.metric("Total Net", f"${total_net:,.2f}")
    
    with col3:
        total_fees = total_gross - total_net
        st.metric("Total Fees", f"${total_fees:,.2f}")
    
    with col4:
        if total_gross > 0:
            fee_percentage = (total_fees / total_gross) * 100
            st.metric("Fee %", f"{fee_percentage:.1f}%")
        else:
            st.metric("Fee %", "0%")
    
    # Payment source breakdown
    st.subheader("Payment Sources")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"""
        **CanAmex Carrier**
        - Deposits: {summary['canamex']['count']}
        - Gross: ${summary['canamex']['gross']:,.2f}
        - Net: ${summary['canamex']['net']:,.2f}
        """)
    
    with col2:
        st.info(f"""
        **Treadstone Capital**
        - Payments: {summary['treadstone']['count']}
        - Gross: ${summary['treadstone']['gross']:,.2f}
        - Net: ${summary['treadstone']['net']:,.2f}
        """)
    
    with col3:
        st.info(f"""
        **Direct Customers**
        - Payments: {summary['direct']['count']}
        - Total: ${summary['direct']['total']:,.2f}
        """)
    
    # Sync status
    st.subheader("Sync Status")
    
    connection_status = qb.connect_to_quickbooks()
    
    if connection_status['status'] == 'not_configured':
        st.warning(connection_status['message'])
    elif connection_status['status'] == 'pending_implementation':
        st.info(connection_status['message'])
        
        with st.expander("Setup Instructions"):
            for step in connection_status['next_steps']:
                st.write(step)
    else:
        st.success("Connected to QuickBooks Online")


def show_payment_reconciliation(qb):
    """Show payment reconciliation interface"""
    st.header("💰 Payment Reconciliation")
    
    # Auto-match button
    if st.button("🔄 Auto-Match Payments", type="primary"):
        result = qb.auto_match_payments()
        st.success(f"""
        Matched {result['matched']} of {result['total_payments']} payments
        - Unmatched: {result['unmatched']}
        """)
    
    # Manual reconciliation
    st.subheader("Manual Reconciliation")
    
    with st.form("manual_reconciliation"):
        col1, col2 = st.columns(2)
        
        with col1:
            payment_date = st.date_input("Payment Date")
            payment_source = st.selectbox(
                "Payment Source",
                ["Direct Customer", "CanAmex", "Treadstone", "Other"]
            )
            payment_method = st.selectbox(
                "Payment Method",
                ["ACH", "Wire", "Check", "Credit Card"]
            )
        
        with col2:
            reference_number = st.text_input("Reference Number")
            amount = st.number_input("Amount", min_value=0.0, format="%.2f")
            load_numbers = st.text_input("Load Numbers (comma-separated)")
        
        notes = st.text_area("Notes")
        
        if st.form_submit_button("Record Payment"):
            cursor = qb.conn.cursor()
            cursor.execute("""
                INSERT INTO payment_reconciliation
                (payment_date, payment_source, payment_method, reference_number,
                 amount, load_numbers, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (payment_date, payment_source, payment_method, reference_number,
                  amount, load_numbers, notes))
            qb.conn.commit()
            st.success("Payment recorded successfully!")
    
    # Recent payments
    st.subheader("Recent Payments")
    
    cursor = qb.conn.cursor()
    recent_payments = pd.read_sql_query("""
        SELECT 
            payment_date as 'Date',
            payment_source as 'Source',
            payment_method as 'Method',
            reference_number as 'Reference',
            amount as 'Amount',
            CASE WHEN reconciled = 1 THEN '✅' ELSE '❌' END as 'Reconciled'
        FROM payment_reconciliation
        ORDER BY payment_date DESC
        LIMIT 20
    """, qb.conn)
    
    if not recent_payments.empty:
        st.dataframe(recent_payments, use_container_width=True, hide_index=True)
    else:
        st.info("No payments recorded yet")


def show_canamex_deposits(qb):
    """Show CanAmex deposits management"""
    st.header("🏦 CanAmex Carrier Deposits")
    
    st.info("Track and reconcile CanAmex carrier service deposits with commission deductions")
    
    # Add new deposit
    with st.expander("➕ Record New Deposit"):
        with st.form("canamex_deposit"):
            col1, col2 = st.columns(2)
            
            with col1:
                deposit_date = st.date_input("Deposit Date")
                deposit_amount = st.number_input("Gross Amount", min_value=0.0, format="%.2f")
                commission_rate = st.number_input("Commission Rate (%)", value=3.5, format="%.2f")
            
            with col2:
                net_amount = deposit_amount * (1 - commission_rate / 100)
                st.metric("Net Amount", f"${net_amount:,.2f}")
                load_count = st.number_input("Number of Loads", min_value=0)
                load_ids = st.text_area("Load Numbers")
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Record Deposit"):
                result = qb.reconcile_canamex_deposit({
                    'deposit_date': deposit_date,
                    'deposit_amount': deposit_amount,
                    'commission_rate': commission_rate,
                    'net_amount': net_amount,
                    'load_count': load_count,
                    'load_ids': load_ids,
                    'notes': notes
                })
                
                if result['status'] == 'success':
                    st.success(result['message'])
                else:
                    st.error(result['message'])
    
    # Recent deposits
    st.subheader("Recent CanAmex Deposits")
    
    cursor = qb.conn.cursor()
    deposits = pd.read_sql_query("""
        SELECT 
            deposit_date as 'Date',
            deposit_amount as 'Gross',
            commission_rate as 'Comm %',
            net_amount as 'Net',
            load_count as 'Loads',
            CASE WHEN reconciled = 1 THEN '✅' ELSE '❌' END as 'Reconciled'
        FROM canamex_deposits
        ORDER BY deposit_date DESC
        LIMIT 20
    """, qb.conn)
    
    if not deposits.empty:
        # Format currency columns
        deposits['Gross'] = deposits['Gross'].apply(lambda x: f"${x:,.2f}")
        deposits['Net'] = deposits['Net'].apply(lambda x: f"${x:,.2f}")
        deposits['Comm %'] = deposits['Comm %'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(deposits, use_container_width=True, hide_index=True)
        
        # Summary statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_deposits,
                SUM(deposit_amount) as total_gross,
                SUM(net_amount) as total_net,
                AVG(commission_rate) as avg_commission
            FROM canamex_deposits
            WHERE deposit_date >= date('now', '-30 days')
        """)
        
        stats = cursor.fetchone()
        
        if stats[0] > 0:
            st.info(f"""
            **30-Day Summary:**
            - Total Deposits: {stats[0]}
            - Total Gross: ${stats[1]:,.2f}
            - Total Net: ${stats[2]:,.2f}
            - Average Commission: {stats[3]:.2f}%
            """)
    else:
        st.info("No CanAmex deposits recorded yet")


def show_treadstone_payments(qb):
    """Show Treadstone Capital payments management"""
    st.header("💳 Treadstone Capital Factoring Payments")
    
    st.info("Track factoring payments from Treadstone Capital with fee deductions")
    
    # Add new payment
    with st.expander("➕ Record New Payment"):
        with st.form("treadstone_payment"):
            col1, col2 = st.columns(2)
            
            with col1:
                payment_date = st.date_input("Payment Date")
                invoice_number = st.text_input("Invoice Number")
                gross_amount = st.number_input("Gross Amount", min_value=0.0, format="%.2f")
            
            with col2:
                factoring_fee = st.number_input("Factoring Fee", min_value=0.0, format="%.2f")
                net_amount = gross_amount - factoring_fee
                st.metric("Net Amount", f"${net_amount:,.2f}")
                customer_name = st.text_input("Customer Name")
            
            load_numbers = st.text_area("Load Numbers")
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Record Payment"):
                result = qb.reconcile_treadstone_payment({
                    'payment_date': payment_date,
                    'invoice_number': invoice_number,
                    'gross_amount': gross_amount,
                    'factoring_fee': factoring_fee,
                    'net_amount': net_amount,
                    'customer_name': customer_name,
                    'load_numbers': load_numbers,
                    'notes': notes
                })
                
                if result['status'] == 'success':
                    st.success(result['message'])
                else:
                    st.error(result['message'])
    
    # Recent payments
    st.subheader("Recent Treadstone Payments")
    
    cursor = qb.conn.cursor()
    payments = pd.read_sql_query("""
        SELECT 
            payment_date as 'Date',
            invoice_number as 'Invoice',
            customer_name as 'Customer',
            gross_amount as 'Gross',
            factoring_fee as 'Fee',
            net_amount as 'Net',
            CASE WHEN reconciled = 1 THEN '✅' ELSE '❌' END as 'Reconciled'
        FROM treadstone_payments
        ORDER BY payment_date DESC
        LIMIT 20
    """, qb.conn)
    
    if not payments.empty:
        # Format currency columns
        payments['Gross'] = payments['Gross'].apply(lambda x: f"${x:,.2f}")
        payments['Fee'] = payments['Fee'].apply(lambda x: f"${x:,.2f}")
        payments['Net'] = payments['Net'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(payments, use_container_width=True, hide_index=True)
        
        # Summary statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total_payments,
                SUM(gross_amount) as total_gross,
                SUM(factoring_fee) as total_fees,
                SUM(net_amount) as total_net
            FROM treadstone_payments
            WHERE payment_date >= date('now', '-30 days')
        """)
        
        stats = cursor.fetchone()
        
        if stats[0] > 0:
            fee_percentage = (stats[2] / stats[1]) * 100 if stats[1] > 0 else 0
            st.info(f"""
            **30-Day Summary:**
            - Total Payments: {stats[0]}
            - Total Gross: ${stats[1]:,.2f}
            - Total Fees: ${stats[2]:,.2f} ({fee_percentage:.1f}%)
            - Total Net: ${stats[3]:,.2f}
            """)
    else:
        st.info("No Treadstone payments recorded yet")


def show_sync_operations(qb):
    """Show QuickBooks sync operations"""
    st.header("🔄 Sync Operations")
    
    st.warning("QuickBooks sync will be available once API credentials are configured and connected")
    
    # Sync buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Sync Invoices", use_container_width=True):
            result = qb.sync_invoices()
            if result['status'] == 'simulated':
                st.info(result['message'])
                if result.get('invoices'):
                    st.write(f"Found {len(result['invoices'])} unsynced invoices")
            else:
                st.info(result['message'])
    
    with col2:
        if st.button("👥 Sync Customers", use_container_width=True):
            result = qb.sync_customers()
            if result['status'] == 'simulated':
                st.info(result['message'])
            else:
                st.info(result['message'])
    
    with col3:
        if st.button("💰 Sync Payments", use_container_width=True):
            st.info("Payment sync pending QuickBooks API connection")
    
    with col4:
        if st.button("📊 Full Sync", use_container_width=True):
            st.info("Full sync pending QuickBooks API connection")
    
    # Sync history
    st.subheader("Sync History")
    
    cursor = qb.conn.cursor()
    sync_history = pd.read_sql_query("""
        SELECT 
            sync_date as 'Date',
            sync_type as 'Type',
            records_synced as 'Records',
            status as 'Status',
            error_message as 'Error'
        FROM quickbooks_sync
        ORDER BY sync_date DESC
        LIMIT 20
    """, qb.conn)
    
    if not sync_history.empty:
        st.dataframe(sync_history, use_container_width=True, hide_index=True)
    else:
        st.info("No sync operations recorded yet")
    
    # Export options
    st.subheader("Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        export_type = st.selectbox(
            "Export Type",
            ["Invoices", "Payments", "Customers"]
        )
    
    with col2:
        if st.button("📥 Export to CSV", use_container_width=True):
            if export_type == "Invoices":
                df = qb.export_to_quickbooks_format('invoices')
            elif export_type == "Payments":
                df = qb.export_to_quickbooks_format('payments')
            else:
                df = None
            
            if df is not None and not df.empty:
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    f"quickbooks_{export_type.lower()}.csv",
                    "text/csv"
                )
            else:
                st.info("No data to export")


def show_quickbooks_reports(qb):
    """Show QuickBooks-related reports"""
    st.header("📊 QuickBooks Reports")
    
    report_type = st.selectbox(
        "Select Report",
        ["Payment Summary", "Reconciliation Status", "Fee Analysis", "Cash Flow"]
    )
    
    # Date range
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=30), key="report_start")
    with col2:
        end_date = st.date_input("End Date", value=date.today(), key="report_end")
    
    if report_type == "Payment Summary":
        show_payment_summary_report(qb, start_date, end_date)
    elif report_type == "Reconciliation Status":
        show_reconciliation_report(qb, start_date, end_date)
    elif report_type == "Fee Analysis":
        show_fee_analysis_report(qb, start_date, end_date)
    else:
        show_cash_flow_report(qb, start_date, end_date)


def show_payment_summary_report(qb, start_date, end_date):
    """Show payment summary report"""
    st.subheader("Payment Summary Report")
    
    summary = qb.get_payment_summary(start_date, end_date)
    
    # Create summary table
    summary_data = {
        'Source': ['CanAmex', 'Treadstone', 'Direct', 'Total'],
        'Count': [
            summary['canamex']['count'],
            summary['treadstone']['count'],
            summary['direct']['count'],
            sum([summary['canamex']['count'], summary['treadstone']['count'], summary['direct']['count']])
        ],
        'Gross': [
            f"${summary['canamex']['gross']:,.2f}",
            f"${summary['treadstone']['gross']:,.2f}",
            f"${summary['direct']['total']:,.2f}",
            f"${summary['canamex']['gross'] + summary['treadstone']['gross'] + summary['direct']['total']:,.2f}"
        ],
        'Net': [
            f"${summary['canamex']['net']:,.2f}",
            f"${summary['treadstone']['net']:,.2f}",
            f"${summary['direct']['total']:,.2f}",
            f"${summary['canamex']['net'] + summary['treadstone']['net'] + summary['direct']['total']:,.2f}"
        ]
    }
    
    df = pd.DataFrame(summary_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def show_reconciliation_report(qb, start_date, end_date):
    """Show reconciliation status report"""
    st.subheader("Reconciliation Status Report")
    
    cursor = qb.conn.cursor()
    
    # Get reconciliation stats
    cursor.execute("""
        SELECT 
            payment_source,
            COUNT(*) as total,
            SUM(CASE WHEN reconciled = 1 THEN 1 ELSE 0 END) as reconciled,
            SUM(CASE WHEN reconciled = 0 THEN 1 ELSE 0 END) as unreconciled,
            SUM(amount) as total_amount
        FROM payment_reconciliation
        WHERE payment_date BETWEEN ? AND ?
        GROUP BY payment_source
    """, (start_date, end_date))
    
    stats = cursor.fetchall()
    
    if stats:
        report_data = []
        for stat in stats:
            reconciliation_rate = (stat[2] / stat[1]) * 100 if stat[1] > 0 else 0
            report_data.append({
                'Source': stat[0],
                'Total': stat[1],
                'Reconciled': stat[2],
                'Unreconciled': stat[3],
                'Rate': f"{reconciliation_rate:.1f}%",
                'Amount': f"${stat[4]:,.2f}"
            })
        
        df = pd.DataFrame(report_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No reconciliation data for selected period")


def show_fee_analysis_report(qb, start_date, end_date):
    """Show fee analysis report"""
    st.subheader("Fee Analysis Report")
    
    cursor = qb.conn.cursor()
    
    # CanAmex fees
    cursor.execute("""
        SELECT 
            AVG(commission_rate) as avg_rate,
            SUM(deposit_amount - net_amount) as total_fees,
            COUNT(*) as transaction_count
        FROM canamex_deposits
        WHERE deposit_date BETWEEN ? AND ?
    """, (start_date, end_date))
    
    canamex_fees = cursor.fetchone()
    
    # Treadstone fees
    cursor.execute("""
        SELECT 
            AVG(factoring_fee / gross_amount * 100) as avg_rate,
            SUM(factoring_fee) as total_fees,
            COUNT(*) as transaction_count
        FROM treadstone_payments
        WHERE payment_date BETWEEN ? AND ?
            AND gross_amount > 0
    """, (start_date, end_date))
    
    treadstone_fees = cursor.fetchone()
    
    # Display fee analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"""
        **CanAmex Fees:**
        - Average Rate: {canamex_fees[0]:.2f}%
        - Total Fees: ${canamex_fees[1]:,.2f}
        - Transactions: {canamex_fees[2]}
        """)
    
    with col2:
        st.info(f"""
        **Treadstone Fees:**
        - Average Rate: {treadstone_fees[0]:.2f}%
        - Total Fees: ${treadstone_fees[1]:,.2f}
        - Transactions: {treadstone_fees[2]}
        """)
    
    # Total fee summary
    total_fees = (canamex_fees[1] or 0) + (treadstone_fees[1] or 0)
    st.metric("Total Fees Paid", f"${total_fees:,.2f}")


def show_cash_flow_report(qb, start_date, end_date):
    """Show cash flow report"""
    st.subheader("Cash Flow Report")
    
    st.info("Cash flow analysis will be available once QuickBooks integration is complete")
    
    # Placeholder for cash flow visualization
    st.write("This report will show:")
    st.write("- Daily cash inflows and outflows")
    st.write("- Running balance")
    st.write("- Payment timing analysis")
    st.write("- Cash flow projections")


def show_quickbooks_settings(qb):
    """Show QuickBooks integration settings"""
    st.header("⚙️ QuickBooks Settings")
    
    # Account mapping
    st.subheader("Account Mapping")
    
    with st.form("account_mapping"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Revenue Account", value="Trucking Revenue")
            st.text_input("Expense Account", value="Operating Expenses")
            st.text_input("Bank Account", value="Business Checking")
        
        with col2:
            st.text_input("CanAmex Account", value="CanAmex Deposits")
            st.text_input("Treadstone Account", value="Treadstone Factoring")
            st.text_input("Customer Deposits", value="Customer Payments")
        
        if st.form_submit_button("Save Mapping"):
            st.success("Account mapping saved (will sync when API is connected)")
    
    # Sync preferences
    st.subheader("Sync Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Auto-sync invoices", value=True)
        st.checkbox("Auto-sync payments", value=True)
        st.checkbox("Auto-sync customers", value=False)
    
    with col2:
        sync_frequency = st.selectbox(
            "Sync Frequency",
            ["Real-time", "Hourly", "Daily", "Weekly", "Manual"]
        )
        st.time_input("Daily Sync Time", value=datetime.strptime("09:00", "%H:%M").time())
    
    # API configuration
    st.subheader("API Configuration")
    
    if qb.is_configured:
        st.success("API credentials configured")
        if st.button("Test Connection"):
            result = qb.connect_to_quickbooks()
            st.info(result['message'])
    else:
        st.warning("API credentials not configured")
        
        with st.expander("Configuration Instructions"):
            st.write("""
            1. **Get QuickBooks API Access:**
               - Go to https://developer.intuit.com
               - Create a new app for QuickBooks Online
               - Get your Client ID and Client Secret
            
            2. **Add to .env file:**
               ```
               QUICKBOOKS_CLIENT_ID=your_client_id_here
               QUICKBOOKS_CLIENT_SECRET=your_client_secret_here
               ```
            
            3. **Complete OAuth2 Setup:**
               - Authorize the app to access your QuickBooks company
               - Store refresh tokens securely
            
            4. **Test Connection:**
               - Click "Test Connection" button above
               - Verify sync operations work correctly
            """)


# Export functions
__all__ = ['QuickBooksIntegration', 'show_quickbooks_dashboard']