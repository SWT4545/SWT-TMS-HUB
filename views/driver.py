"""
Driver Portal View for SWT TMS Hub
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.database import get_connection
from modules.ui_components import show_page_header, show_success_message, show_error_message

def show_driver_view():
    """Display driver portal with assigned loads and status updates"""
    show_page_header(
        "🚚 Driver Portal", 
        "View your assigned loads and update delivery status"
    )
    
    tabs = st.tabs(["📋 My Loads", "📍 Update Status", "📊 My Performance", "📞 Contact"])
    
    with tabs[0]:
        show_assigned_loads()
    
    with tabs[1]:
        show_status_update()
    
    with tabs[2]:
        show_driver_performance()
    
    with tabs[3]:
        show_contact_info()

def show_assigned_loads():
    """Show loads assigned to current driver"""
    st.subheader("📦 My Assigned Loads")
    
    # In a real app, you'd get the driver ID from session
    # For demo, we'll show all active dispatches
    conn = get_connection()
    
    assigned_loads = pd.read_sql_query("""
        SELECT 
            d.dispatch_number,
            s.load_number,
            s.origin_city || ', ' || s.origin_state as origin,
            s.destination_city || ', ' || s.destination_state as destination,
            s.pickup_date,
            s.pickup_time,
            s.delivery_date,
            s.delivery_time,
            s.commodity,
            s.weight,
            s.pieces,
            s.special_instructions,
            d.status as dispatch_status,
            d.carrier_rate,
            dr.first_name || ' ' || dr.last_name as driver_name,
            t.truck_number
        FROM dispatches d
        JOIN shipments s ON d.shipment_id = s.id
        JOIN drivers dr ON d.driver_id = dr.id
        LEFT JOIN trucks t ON d.truck_id = t.id
        WHERE d.status NOT IN ('Delivered', 'Completed')
        ORDER BY s.pickup_date
    """, conn)
    
    if not assigned_loads.empty:
        # Display each load as an expandable card
        for _, load in assigned_loads.iterrows():
            with st.expander(f"🚛 {load['load_number']} - {load['origin']} → {load['destination']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### 📍 Pickup Information")
                    st.write(f"**Location:** {load['origin']}")
                    st.write(f"**Date:** {load['pickup_date']}")
                    st.write(f"**Time:** {load['pickup_time']}")
                    
                    st.markdown("##### 🎯 Delivery Information")
                    st.write(f"**Location:** {load['destination']}")
                    st.write(f"**Date:** {load['delivery_date']}")
                    st.write(f"**Time:** {load['delivery_time']}")
                
                with col2:
                    st.markdown("##### 📦 Load Details")
                    st.write(f"**Commodity:** {load['commodity'] or 'Not specified'}")
                    st.write(f"**Weight:** {load['weight']:,.0f} lbs" if load['weight'] else "Weight: Not specified")
                    st.write(f"**Pieces:** {load['pieces']}" if load['pieces'] else "Pieces: Not specified")
                    st.write(f"**Rate:** ${load['carrier_rate']:,.2f}" if load['carrier_rate'] else "Rate: Not specified")
                    
                    # Current status
                    status_color = {
                        'Dispatched': '🟡',
                        'En Route to Pickup': '🟠',
                        'At Pickup': '🔵',
                        'Loaded': '🟢',
                        'In Transit': '🟣',
                        'At Delivery': '🔴',
                        'Delivered': '✅'
                    }
                    status_icon = status_color.get(load['dispatch_status'], '⚪')
                    st.write(f"**Status:** {status_icon} {load['dispatch_status']}")
                
                # Special instructions
                if load['special_instructions']:
                    st.markdown("##### ⚠️ Special Instructions")
                    st.warning(load['special_instructions'])
                
                # Quick status update buttons
                st.markdown("##### 🔄 Quick Status Update")
                status_col1, status_col2, status_col3 = st.columns(3)
                
                with status_col1:
                    if st.button(f"📍 At Pickup", key=f"pickup_{load['dispatch_number']}"):
                        update_dispatch_status(load['dispatch_number'], 'At Pickup')
                        st.rerun()
                
                with status_col2:
                    if st.button(f"🚚 Loaded", key=f"loaded_{load['dispatch_number']}"):
                        update_dispatch_status(load['dispatch_number'], 'Loaded')
                        st.rerun()
                
                with status_col3:
                    if st.button(f"✅ Delivered", key=f"delivered_{load['dispatch_number']}"):
                        update_dispatch_status(load['dispatch_number'], 'Delivered')
                        st.rerun()
    else:
        st.info("🎉 No active loads assigned. Contact dispatch for your next assignment.")
    
    conn.close()

def show_status_update():
    """Detailed status update form"""
    st.subheader("📍 Update Load Status")
    
    conn = get_connection()
    
    # Get active dispatches
    active_dispatches = pd.read_sql_query("""
        SELECT d.dispatch_number, s.load_number, d.status
        FROM dispatches d
        JOIN shipments s ON d.shipment_id = s.id
        WHERE d.status NOT IN ('Delivered', 'Completed')
        ORDER BY s.pickup_date
    """, conn)
    
    if not active_dispatches.empty:
        dispatch_options = {}
        for _, row in active_dispatches.iterrows():
            key = f"{row['load_number']} ({row['dispatch_number']}) - {row['status']}"
            dispatch_options[key] = row['dispatch_number']
        
        selected_dispatch_key = st.selectbox("Select Load", options=list(dispatch_options.keys()))
        selected_dispatch = dispatch_options[selected_dispatch_key]
        
        # Status update form
        with st.form("status_update"):
            new_status = st.selectbox(
                "New Status",
                ['Dispatched', 'En Route to Pickup', 'At Pickup', 'Loaded', 'In Transit', 'At Delivery', 'Delivered']
            )
            
            # Optional additional information
            col1, col2 = st.columns(2)
            
            with col1:
                actual_pickup_time = st.datetime_input("Actual Pickup Time (optional)", value=None)
                actual_delivery_time = st.datetime_input("Actual Delivery Time (optional)", value=None)
            
            with col2:
                detention_time = st.number_input("Detention Time (hours)", min_value=0.0, step=0.5)
                lumper_fee = st.number_input("Lumper Fee ($)", min_value=0.0, step=25.0)
            
            notes = st.text_area("Additional Notes", placeholder="Any issues, delays, or important information...")
            
            # Photo upload (placeholder)
            uploaded_photos = st.file_uploader(
                "Upload Photos (BOL, POD, etc.)", 
                accept_multiple_files=True,
                type=['jpg', 'jpeg', 'png', 'pdf']
            )
            
            if st.form_submit_button("📤 Update Status", type="primary", use_container_width=True):
                try:
                    cursor = conn.cursor()
                    
                    # Update dispatch status
                    cursor.execute("""
                        UPDATE dispatches 
                        SET status = ?, notes = COALESCE(notes, '') || ?
                        WHERE dispatch_number = ?
                    """, (new_status, f"\n[{datetime.now()}] {notes}" if notes else "", selected_dispatch))
                    
                    # Update pickup/delivery times if provided
                    if actual_pickup_time and new_status in ['At Pickup', 'Loaded']:
                        cursor.execute("""
                            UPDATE dispatches 
                            SET pickup_arrival = ?
                            WHERE dispatch_number = ?
                        """, (actual_pickup_time, selected_dispatch))
                    
                    if actual_delivery_time and new_status == 'Delivered':
                        cursor.execute("""
                            UPDATE dispatches 
                            SET delivery_arrival = ?
                            WHERE dispatch_number = ?
                        """, (actual_delivery_time, selected_dispatch))
                    
                    # Update fees if provided
                    if detention_time > 0 or lumper_fee > 0:
                        cursor.execute("""
                            UPDATE dispatches 
                            SET detention_time = ?, lumper_fee = ?
                            WHERE dispatch_number = ?
                        """, (detention_time, lumper_fee, selected_dispatch))
                    
                    # Update shipment status based on dispatch status
                    shipment_status_map = {
                        'Dispatched': 'Dispatched',
                        'En Route to Pickup': 'Dispatched',
                        'At Pickup': 'Dispatched',
                        'Loaded': 'In Transit',
                        'In Transit': 'In Transit',
                        'At Delivery': 'In Transit',
                        'Delivered': 'Delivered'
                    }
                    
                    if new_status in shipment_status_map:
                        cursor.execute("""
                            UPDATE shipments 
                            SET status = ?, updated_at = ?
                            WHERE id = (SELECT shipment_id FROM dispatches WHERE dispatch_number = ?)
                        """, (shipment_status_map[new_status], datetime.now(), selected_dispatch))
                    
                    conn.commit()
                    show_success_message(f"Status updated to: {new_status}")
                    
                    # Handle photo uploads (placeholder)
                    if uploaded_photos:
                        st.info(f"📸 {len(uploaded_photos)} photo(s) uploaded successfully")
                    
                    st.rerun()
                    
                except Exception as e:
                    show_error_message(f"Error updating status: {str(e)}")
    else:
        st.info("No active loads to update")
    
    conn.close()

def show_driver_performance():
    """Show driver performance metrics"""
    st.subheader("📊 My Performance")
    
    conn = get_connection()
    
    # Performance metrics for current driver
    # In real app, filter by actual driver ID
    performance_data = pd.read_sql_query("""
        SELECT 
            COUNT(*) as total_deliveries,
            AVG(d.carrier_rate) as avg_rate,
            SUM(d.carrier_rate) as total_earnings,
            AVG(CASE 
                WHEN d.delivery_arrival IS NOT NULL AND s.delivery_date IS NOT NULL 
                THEN julianday(d.delivery_arrival) - julianday(s.delivery_date || ' ' || s.delivery_time)
                ELSE NULL 
            END) as avg_delivery_variance
        FROM dispatches d
        JOIN shipments s ON d.shipment_id = s.id
        WHERE d.status = 'Completed'
        AND date(d.dispatched_at) >= date('now', '-30 days')
    """, conn)
    
    if not performance_data.empty and performance_data.iloc[0]['total_deliveries'] > 0:
        metrics = performance_data.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Deliveries (30 days)", int(metrics['total_deliveries']))
        
        with col2:
            st.metric("Average Rate", f"${metrics['avg_rate']:,.2f}" if metrics['avg_rate'] else "$0.00")
        
        with col3:
            st.metric("Total Earnings", f"${metrics['total_earnings']:,.2f}" if metrics['total_earnings'] else "$0.00")
        
        with col4:
            variance_days = metrics['avg_delivery_variance'] if metrics['avg_delivery_variance'] else 0
            variance_text = f"+{variance_days:.1f} days" if variance_days > 0 else f"{variance_days:.1f} days"
            st.metric("Avg Delivery Variance", variance_text)
        
        # Recent deliveries
        st.markdown("#### Recent Completed Deliveries")
        recent_deliveries = pd.read_sql_query("""
            SELECT 
                s.load_number,
                s.origin_city || ', ' || s.origin_state as origin,
                s.destination_city || ', ' || s.destination_state as destination,
                s.delivery_date,
                d.carrier_rate,
                d.status
            FROM dispatches d
            JOIN shipments s ON d.shipment_id = s.id
            WHERE d.status IN ('Delivered', 'Completed')
            ORDER BY d.delivery_arrival DESC
            LIMIT 10
        """, conn)
        
        if not recent_deliveries.empty:
            st.dataframe(recent_deliveries, use_container_width=True, hide_index=True)
        else:
            st.info("No recent deliveries found")
    else:
        st.info("No performance data available for the last 30 days")
    
    conn.close()

def show_contact_info():
    """Show emergency contacts and dispatch information"""
    st.subheader("📞 Emergency Contacts & Information")
    
    # Emergency contacts
    st.markdown("#### 🚨 Emergency Contacts")
    
    contact_col1, contact_col2 = st.columns(2)
    
    with contact_col1:
        st.markdown("""
        **Dispatch Office:**
        📞 (951) 437-5474
        📧 Dispatch@smithwilliamstrucking.com
        
        **After Hours Emergency:**
        📞 (951) 437-5474 ext. 911
        """)
    
    with contact_col2:
        st.markdown("""
        **Breakdown Assistance:**
        📞 1-800-ROADWAY
        
        **Company Main Office:**
        📞 (951) 437-5474
        📧 info@smithwilliamstrucking.com
        """)
    
    # Quick message to dispatch
    st.markdown("#### 💬 Send Message to Dispatch")
    
    with st.form("dispatch_message"):
        message_type = st.selectbox(
            "Message Type",
            ["General", "Breakdown", "Delay", "Route Change", "Emergency", "Other"]
        )
        
        current_location = st.text_input("Current Location")
        message = st.text_area("Message", placeholder="Describe your situation or question...")
        
        if st.form_submit_button("📤 Send Message", type="primary"):
            if message:
                # In real app, this would send to dispatch system
                show_success_message("Message sent to dispatch successfully!")
                st.info("Dispatch will contact you shortly via phone or Qualcomm.")
            else:
                show_error_message("Please enter a message")
    
    # Company policies reminder
    st.markdown("#### 📋 Important Reminders")
    st.info("""
    **Hours of Service:** Remember to log your driving hours and take required breaks.
    
    **Fuel Cards:** Use company fuel cards at approved locations only.
    
    **Documentation:** Always obtain signed BOL and POD for each delivery.
    
    **Safety First:** If you feel unsafe or too tired to drive, contact dispatch immediately.
    """)

def update_dispatch_status(dispatch_number, new_status):
    """Helper function to update dispatch status"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE dispatches 
            SET status = ?
            WHERE dispatch_number = ?
        """, (new_status, dispatch_number))
        
        # Update corresponding shipment status
        status_map = {
            'At Pickup': 'Dispatched',
            'Loaded': 'In Transit',
            'Delivered': 'Delivered'
        }
        
        if new_status in status_map:
            cursor.execute("""
                UPDATE shipments 
                SET status = ?, updated_at = ?
                WHERE id = (SELECT shipment_id FROM dispatches WHERE dispatch_number = ?)
            """, (status_map[new_status], datetime.now(), dispatch_number))
        
        conn.commit()
        show_success_message(f"Status updated to: {new_status}")
        
    except Exception as e:
        show_error_message(f"Error updating status: {str(e)}")
    finally:
        conn.close()