"""
Enhanced Historical Data Feeder View with Florida AI Assistant
Includes conversational load entry and intelligent payment reconciliation
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from modules.ai_assistants import FloridaAssistant
from modules.database_enhanced import (
    execute_query, get_loads_for_reconciliation, 
    calculate_payment_amounts, get_carrier_payment_schedule
)
from modules.api_integrations import GoogleMapsAPI

def show_data_feeder_view():
    """Display the enhanced data feeder interface with Florida AI"""
    
    # Initialize Florida AI
    florida = FloridaAssistant()
    
    # Header with Florida branding
    st.markdown("""
    <h1 style='text-align: center; color: white; border-bottom: 3px solid #8B0000; padding-bottom: 20px;'>
        📝 HISTORICAL DATA FEEDER
    </h1>
    <div style='text-align: center; color: #8B0000; font-weight: bold; margin-bottom: 20px;'>
        Powered by Florida - Your Intelligent TMS Assistant
    </div>
    """, unsafe_allow_html=True)
    
    # Main navigation tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Conversational Load Entry",
        "💰 Payment Reconciliation", 
        "📊 Bulk Import",
        "📈 Data Analytics"
    ])
    
    with tab1:
        show_conversational_entry(florida)
    
    with tab2:
        show_payment_reconciliation()
    
    with tab3:
        show_bulk_import()
    
    with tab4:
        show_data_analytics()


def show_conversational_entry(florida):
    """Show the conversational load entry interface"""
    
    # Chat interface container
    chat_container = st.container()
    
    with chat_container:
        # Display Florida's personality intro
        with st.expander("About Florida - Your TMS Assistant", expanded=False):
            st.info(florida.personality)
        
        # Main conversation flow
        florida.process_load_entry()
        
        # Quick actions sidebar
        with st.sidebar:
            st.subheader("⚡ Quick Actions")
            
            if st.button("🔄 Start New Load Entry"):
                st.session_state.florida_state = 'ask_load_id'
                st.session_state.florida_data = {}
                st.rerun()
            
            if st.button("📋 View Recent Entries"):
                st.session_state.florida_state = 'greeting'
                florida.show_recent_loads()
            
            if st.button("💰 Go to Reconciliation"):
                st.session_state.florida_state = 'reconciliation'
                st.rerun()
            
            # Show current session data
            if st.session_state.get('florida_data'):
                st.subheader("📝 Current Load Data")
                for key, value in st.session_state.florida_data.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")


def show_payment_reconciliation():
    """Show the intelligent payment reconciliation interface"""
    
    st.subheader("💰 Intelligent Payment Reconciliation")
    
    # Payment entry form
    with st.expander("➕ Record New Payment", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            payment_amount = st.number_input("Payment Amount ($)", min_value=0.0, format="%.2f")
        
        with col2:
            payment_date = st.date_input("Payment Date", value=datetime.now())
        
        with col3:
            paying_entity = st.selectbox(
                "Paying Entity",
                ["CanAmex", "Factoring Company", "Direct Customer", "Other"]
            )
            if paying_entity == "Other":
                paying_entity = st.text_input("Specify Entity")
        
        reference_number = st.text_input("Reference/Check Number (Optional)")
        notes = st.text_area("Notes (Optional)")
        
        if st.button("🔍 Find Matching Loads", type="primary"):
            if payment_amount > 0 and paying_entity:
                # Get payment schedule for carrier
                schedule = get_carrier_payment_schedule(paying_entity)
                
                # Find potential loads for reconciliation
                loads = get_loads_for_reconciliation(paying_entity, payment_date, payment_amount)
                
                if loads:
                    st.success(f"Found {len(loads)} potential loads for reconciliation")
                    
                    # Store in session for reconciliation
                    st.session_state['reconciliation_data'] = {
                        'payment_amount': payment_amount,
                        'payment_date': payment_date,
                        'paying_entity': paying_entity,
                        'reference_number': reference_number,
                        'notes': notes,
                        'loads': loads
                    }
                    
                    # Display intelligent recommendations
                    st.info(f"""
                    🤖 **Florida's Recommendation:**
                    Based on {paying_entity}'s payment schedule:
                    - Payment Type: {schedule['method'] if schedule else 'Unknown'}
                    - Fee Structure: {schedule['fee_percent'] if schedule else 'N/A'}%
                    - Payment Cycle: {schedule['cycle'] if schedule else 'N/A'}
                    """)
                    
                    show_reconciliation_interface(loads, payment_amount)
                else:
                    st.warning("No unreconciled loads found for this entity and date range")
            else:
                st.error("Please enter payment amount and paying entity")
    
    # Show existing unreconciled payments
    show_unreconciled_payments()


def show_reconciliation_interface(loads, payment_amount):
    """Interface for selecting loads to reconcile"""
    
    st.subheader("Select Loads to Reconcile")
    
    # Create selection table
    selected_loads = []
    total_selected = 0.0
    
    for load in loads:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
        
        with col1:
            selected = st.checkbox("", key=f"select_{load['id']}")
            if selected:
                selected_loads.append(load)
                total_selected += load['net_amount']
        
        with col2:
            st.write(f"**{load['load_id']}**")
        
        with col3:
            st.write(f"{load['customer']}")
        
        with col4:
            st.write(f"${load['net_amount']:,.2f}")
        
        with col5:
            st.write(f"{load['delivery_date']}")
    
    # Show reconciliation summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Payment Amount", f"${payment_amount:,.2f}")
    with col2:
        st.metric("Selected Total", f"${total_selected:,.2f}")
    with col3:
        difference = payment_amount - total_selected
        st.metric("Difference", f"${difference:,.2f}",
                 delta="Match!" if abs(difference) < 0.01 else f"${abs(difference):.2f} off")
    
    # Reconcile button
    if st.button("✅ Reconcile Selected Loads", type="primary"):
        if abs(difference) < 0.01:  # Within penny tolerance
            reconcile_payment(selected_loads)
            st.success("✅ Payment successfully reconciled!")
            st.balloons()
            # Clear session data
            del st.session_state['reconciliation_data']
            st.rerun()
        else:
            st.error(f"⚠️ Selected loads don't match payment amount. Difference: ${abs(difference):.2f}")


def reconcile_payment(loads):
    """Save payment reconciliation to database"""
    
    data = st.session_state.get('reconciliation_data', {})
    
    # Save payment record
    payment_id = execute_query("""
        INSERT INTO payments (
            payment_amount, payment_date, paying_entity,
            reference_number, notes, reconciled, reconciled_date, created_by
        ) VALUES (?, ?, ?, ?, ?, 1, ?, ?)
    """, (
        data['payment_amount'], data['payment_date'], data['paying_entity'],
        data['reference_number'], data['notes'], datetime.now(),
        st.session_state.get('user_id', 1)
    ))
    
    # Save reconciliation records
    for load in loads:
        execute_query("""
            INSERT INTO payment_load_reconciliation (
                payment_id, load_id, reconciled_amount, reconciled_by
            ) VALUES (?, ?, ?, ?)
        """, (
            payment_id, load['id'], load['net_amount'],
            st.session_state.get('user_id', 1)
        ))


def show_unreconciled_payments():
    """Display unreconciled payments and loads"""
    
    st.subheader("📋 Unreconciled Items")
    
    # Get unreconciled loads by carrier
    unreconciled = execute_query("""
        SELECT 
            carrier,
            COUNT(*) as load_count,
            SUM(net_amount) as total_amount,
            MIN(delivery_date) as oldest_date
        FROM loads
        WHERE status = 'completed'
        AND id NOT IN (SELECT load_id FROM payment_load_reconciliation)
        GROUP BY carrier
        ORDER BY total_amount DESC
    """)
    
    if unreconciled:
        for item in unreconciled:
            with st.expander(f"{item['carrier']} - {item['load_count']} loads - ${item['total_amount']:,.2f}"):
                # Show individual loads
                loads = execute_query("""
                    SELECT load_id, customer, delivery_date, net_amount
                    FROM loads
                    WHERE carrier = ?
                    AND status = 'completed'
                    AND id NOT IN (SELECT load_id FROM payment_load_reconciliation)
                    ORDER BY delivery_date
                """, (item['carrier'],))
                
                df = pd.DataFrame(loads)
                st.dataframe(df, use_container_width=True)
                
                # Quick reconcile button
                if st.button(f"Reconcile {item['carrier']}", key=f"reconcile_{item['carrier']}"):
                    st.session_state['quick_reconcile_carrier'] = item['carrier']
                    st.rerun()
    else:
        st.success("✅ All payments are reconciled!")


def show_bulk_import():
    """Show bulk import interface"""
    
    st.subheader("📊 Bulk Load Import")
    
    st.info("""
    Upload a CSV or Excel file with the following columns:
    - load_id, customer, carrier, pickup_date, delivery_date
    - pickup_address, pickup_city, pickup_state, pickup_zip
    - delivery_address, delivery_city, delivery_state, delivery_zip
    - gross_amount, payment_method (Direct Pay/Factored)
    """)
    
    uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx'])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.write(f"Preview ({len(df)} rows):")
            st.dataframe(df.head(), use_container_width=True)
            
            # Validate columns
            required_columns = ['load_id', 'customer', 'carrier', 'gross_amount']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"Missing required columns: {', '.join(missing_columns)}")
            else:
                # Process and calculate net amounts
                if st.button("Process & Import", type="primary"):
                    with st.spinner("Processing loads..."):
                        success_count = 0
                        error_count = 0
                        
                        for _, row in df.iterrows():
                            try:
                                # Calculate payment amounts
                                payment_calc = calculate_payment_amounts(
                                    row['gross_amount'],
                                    row.get('payment_method', 'Factored')
                                )
                                
                                # Insert load
                                execute_query("""
                                    INSERT INTO loads (
                                        load_id, customer, carrier, 
                                        pickup_date, delivery_date,
                                        pickup_address, pickup_city, pickup_state, pickup_zip,
                                        delivery_address, delivery_city, delivery_state, delivery_zip,
                                        gross_amount, net_amount, payment_method,
                                        factoring_fee_percent, status, created_by
                                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', ?)
                                """, (
                                    row['load_id'], row['customer'], row['carrier'],
                                    row.get('pickup_date'), row.get('delivery_date'),
                                    row.get('pickup_address'), row.get('pickup_city'),
                                    row.get('pickup_state'), row.get('pickup_zip'),
                                    row.get('delivery_address'), row.get('delivery_city'),
                                    row.get('delivery_state'), row.get('delivery_zip'),
                                    row['gross_amount'], payment_calc['net_amount'],
                                    row.get('payment_method', 'Factored'),
                                    payment_calc['fee_percent'],
                                    st.session_state.get('user_id', 1)
                                ))
                                success_count += 1
                            except Exception as e:
                                error_count += 1
                                st.error(f"Error importing load {row['load_id']}: {str(e)}")
                        
                        st.success(f"✅ Imported {success_count} loads successfully!")
                        if error_count > 0:
                            st.warning(f"⚠️ {error_count} loads failed to import")
                        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")


def show_data_analytics():
    """Show data analytics for entered loads"""
    
    st.subheader("📈 Data Entry Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                   value=datetime.now() - timedelta(days=30),
                                   key="analytics_start")
    with col2:
        end_date = st.date_input("End Date", 
                                 value=datetime.now(),
                                 key="analytics_end")
    
    # Get entry statistics
    stats = execute_query("""
        SELECT 
            DATE(created_at) as entry_date,
            COUNT(*) as loads_entered,
            SUM(gross_amount) as total_value,
            COUNT(DISTINCT carrier) as unique_carriers,
            COUNT(DISTINCT customer) as unique_customers
        FROM loads
        WHERE DATE(created_at) BETWEEN ? AND ?
        GROUP BY DATE(created_at)
        ORDER BY entry_date DESC
    """, (start_date, end_date))
    
    if stats:
        df_stats = pd.DataFrame(stats)
        
        # Entry trend chart
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_stats['entry_date'],
            y=df_stats['loads_entered'],
            name='Loads Entered',
            marker_color='#8B0000'
        ))
        
        fig.update_layout(
            title="Daily Load Entry Trend",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(139,0,0,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_loads = df_stats['loads_entered'].sum()
            st.metric("Total Loads Entered", f"{total_loads:,}")
        with col2:
            total_value = df_stats['total_value'].sum()
            st.metric("Total Value", f"${total_value:,.2f}")
        with col3:
            avg_daily = df_stats['loads_entered'].mean()
            st.metric("Avg Daily Entries", f"{avg_daily:.1f}")
        with col4:
            if total_loads > 0:
                avg_value = total_value / total_loads
                st.metric("Avg Load Value", f"${avg_value:,.2f}")
    else:
        st.info("No data entry statistics available for the selected period")