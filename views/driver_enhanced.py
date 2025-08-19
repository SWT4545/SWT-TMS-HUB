"""
Enhanced Driver View for Smith & Williams Trucking TMS
Includes GPS tracking, geofencing, document upload, and co-pilot assistance
"""
import streamlit as st
from datetime import datetime, timedelta
import time
from modules.database_enhanced import execute_query, get_db_connection
from modules.api_integrations import (
    MotiveAPI, VectorAPI, GoogleMapsAPI, GeofenceManager
)

def show_driver_view():
    """Display the enhanced driver interface with live tracking"""
    
    # Initialize APIs
    motive = MotiveAPI()
    vector = VectorAPI()
    maps = GoogleMapsAPI()
    
    # Header with driver info
    st.markdown("""
    <h1 style='text-align: center; color: white; border-bottom: 3px solid #8B0000; padding-bottom: 20px;'>
        🚚 DRIVER PORTAL
    </h1>
    """, unsafe_allow_html=True)
    
    # Display driver status bar
    display_driver_status()
    
    # Main tabs for driver functions
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📍 Current Load",
        "✅ Check-In",
        "📄 Documents",
        "⏰ HOS Status",
        "💬 Co-Pilot"
    ])
    
    with tab1:
        show_current_load()
    
    with tab2:
        show_checkin_interface()
    
    with tab3:
        show_document_upload()
    
    with tab4:
        show_hos_status()
    
    with tab5:
        show_copilot_assistant()


def display_driver_status():
    """Display driver status bar with key information"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Driver", st.session_state.get('user_full_name', 'Driver'))
    
    with col2:
        # Get active load count
        active_loads = execute_query("""
            SELECT COUNT(*) as count 
            FROM loads 
            WHERE driver_id = ? 
            AND status IN ('assigned', 'in_transit', 'at_pickup', 'at_delivery')
        """, (st.session_state.get('user_id', 1),))
        
        count = active_loads[0]['count'] if active_loads else 0
        st.metric("Active Loads", count)
    
    with col3:
        st.metric("Status", "Available" if count == 0 else "On Load")
    
    with col4:
        st.metric("Time", datetime.now().strftime("%I:%M %p"))


def show_current_load():
    """Display current load information and navigation"""
    
    st.subheader("📍 Current Load Assignment")
    
    # Get most recent assigned load
    current_load = execute_query("""
        SELECT l.*, 
               (SELECT COUNT(*) FROM delays WHERE load_id = l.id) as delay_count
        FROM loads l
        WHERE l.driver_id = ?
        AND l.status IN ('assigned', 'in_transit', 'at_pickup', 'at_delivery')
        ORDER BY l.pickup_date DESC
        LIMIT 1
    """, (st.session_state.get('user_id', 1),))
    
    if current_load:
        load = current_load[0]
        st.session_state['current_load_id'] = load['id']
        
        # Load status progress bar
        status_progress = {
            'assigned': 0.2,
            'at_pickup': 0.4,
            'in_transit': 0.6,
            'at_delivery': 0.8,
            'completed': 1.0
        }
        
        progress = status_progress.get(load['status'], 0)
        st.progress(progress, text=f"Status: {load['status'].replace('_', ' ').title()}")
        
        # Load details in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📦 Load Information")
            st.write(f"**Load ID:** {load['load_id']}")
            st.write(f"**Customer:** {load['customer']}")
            st.write(f"**Carrier:** {load['carrier']}")
            if load['bol_number']:
                st.write(f"**BOL #:** {load['bol_number']}")
            
            if load['delay_count'] > 0:
                st.warning(f"⚠️ {load['delay_count']} delay(s) reported")
        
        with col2:
            st.markdown("### 💰 Financial")
            st.write(f"**Gross Amount:** ${load['gross_amount']:,.2f}")
            if load['distance_miles']:
                st.write(f"**Distance:** {load['distance_miles']:.1f} miles")
                st.write(f"**Rate/Mile:** ${load['gross_rate_per_mile']:.2f}")
        
        # Pickup and Delivery sections
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔵 Pickup Location")
            st.write(f"**Address:** {load['pickup_address']}")
            st.write(f"**City:** {load['pickup_city']}, {load['pickup_state']} {load['pickup_zip']}")
            st.write(f"**Date:** {load['pickup_date']}")
            
            if load['pickup_arrival_time']:
                st.success(f"✅ Arrived: {load['pickup_arrival_time']}")
            if load['pickup_departure_time']:
                st.success(f"✅ Departed: {load['pickup_departure_time']}")
        
        with col2:
            st.markdown("### 🔴 Delivery Location")
            st.write(f"**Address:** {load['delivery_address']}")
            st.write(f"**City:** {load['delivery_city']}, {load['delivery_state']} {load['delivery_zip']}")
            st.write(f"**Date:** {load['delivery_date']}")
            
            if load['delivery_arrival_time']:
                st.success(f"✅ Arrived: {load['delivery_arrival_time']}")
            if load['delivery_departure_time']:
                st.success(f"✅ Departed: {load['delivery_departure_time']}")
        
        # Action buttons based on status
        st.markdown("### 🎯 Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if load['status'] == 'assigned':
                if st.button("🚀 Start Trip", type="primary", use_container_width=True):
                    update_load_status(load['id'], 'in_transit')
                    st.success("Trip started!")
                    st.rerun()
        
        with col2:
            if st.button("📍 Navigate to Pickup", use_container_width=True):
                # Open navigation (placeholder)
                st.info(f"Opening navigation to {load['pickup_address']}")
        
        with col3:
            if st.button("📍 Navigate to Delivery", use_container_width=True):
                # Open navigation (placeholder)
                st.info(f"Opening navigation to {load['delivery_address']}")
        
        # Report delay button
        if load['status'] in ['in_transit', 'at_pickup', 'at_delivery']:
            with st.expander("⚠️ Report Delay"):
                delay_reason = st.text_area("Delay Reason:")
                delay_duration = st.number_input("Estimated Delay (minutes):", min_value=0, step=15)
                
                if st.button("Submit Delay Report"):
                    if delay_reason:
                        report_delay(load['id'], delay_reason, delay_duration)
                        st.success("Delay reported successfully")
                        st.rerun()
                    else:
                        st.error("Please provide a delay reason")
    else:
        st.info("📭 No active loads assigned. Check back later or contact dispatch.")
        
        # Show recent completed loads
        show_completed_loads()


def show_checkin_interface():
    """Show check-in interface with geofencing"""
    
    st.subheader("✅ Check-In / Check-Out")
    
    if 'current_load_id' not in st.session_state:
        st.warning("No active load selected")
        return
    
    load_id = st.session_state['current_load_id']
    
    # Get load details
    load = execute_query("""
        SELECT * FROM loads WHERE id = ?
    """, (load_id,))
    
    if not load:
        st.error("Load not found")
        return
    
    load = load[0]
    
    # Simulated GPS check (in production, would use Motive API)
    st.info("🛰️ Checking GPS location...")
    
    # Check geofence for automatic detection
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Pickup Location")
        
        # Check if already checked in
        if not load['pickup_arrival_time']:
            if st.button("📍 Check In at Pickup", type="primary", use_container_width=True):
                check_in_at_location(load_id, 'pickup_arrival')
                st.success("✅ Checked in at pickup!")
                st.rerun()
        elif not load['pickup_departure_time']:
            st.success(f"✅ Arrived: {load['pickup_arrival_time']}")
            if st.button("🚛 Check Out from Pickup", type="primary", use_container_width=True):
                check_in_at_location(load_id, 'pickup_departure')
                update_load_status(load_id, 'in_transit')
                st.success("✅ Checked out from pickup!")
                st.rerun()
        else:
            st.success(f"✅ Completed pickup at {load['pickup_departure_time']}")
    
    with col2:
        st.markdown("### 🔴 Delivery Location")
        
        # Check if already checked in
        if not load['delivery_arrival_time']:
            # Only show if departed from pickup
            if load['pickup_departure_time']:
                if st.button("📍 Check In at Delivery", type="primary", use_container_width=True):
                    check_in_at_location(load_id, 'delivery_arrival')
                    update_load_status(load_id, 'at_delivery')
                    st.success("✅ Checked in at delivery!")
                    st.rerun()
            else:
                st.info("Complete pickup first")
        elif not load['delivery_departure_time']:
            st.success(f"✅ Arrived: {load['delivery_arrival_time']}")
            if st.button("✅ Complete Delivery", type="primary", use_container_width=True):
                check_in_at_location(load_id, 'delivery_departure')
                update_load_status(load_id, 'completed')
                st.success("✅ Delivery completed!")
                st.balloons()
                st.rerun()
        else:
            st.success(f"✅ Completed delivery at {load['delivery_departure_time']}")
    
    # Manual time entry option
    with st.expander("⏰ Manual Time Entry"):
        st.info("Use this if automatic check-in is not working")
        
        event_type = st.selectbox(
            "Event Type",
            ["Pickup Arrival", "Pickup Departure", "Delivery Arrival", "Delivery Departure"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            event_date = st.date_input("Date", value=datetime.now())
        with col2:
            event_time = st.time_input("Time", value=datetime.now().time())
        
        if st.button("Save Manual Entry"):
            timestamp = datetime.combine(event_date, event_time)
            
            field_map = {
                "Pickup Arrival": "pickup_arrival",
                "Pickup Departure": "pickup_departure",
                "Delivery Arrival": "delivery_arrival",
                "Delivery Departure": "delivery_departure"
            }
            
            check_in_at_location(load_id, field_map[event_type], timestamp)
            st.success(f"✅ {event_type} recorded at {timestamp}")
            st.rerun()


def show_document_upload():
    """Show document upload interface"""
    
    st.subheader("📄 Document Management")
    
    if 'current_load_id' not in st.session_state:
        st.warning("No active load selected")
        return
    
    load_id = st.session_state['current_load_id']
    
    # Get load details
    load = execute_query("""
        SELECT load_id, bol_number, bol_signed, bol_document_url 
        FROM loads WHERE id = ?
    """, (load_id,))
    
    if load:
        load = load[0]
        
        st.write(f"**Load ID:** {load['load_id']}")
        
        # BOL upload section
        st.markdown("### 📋 Bill of Lading (BOL)")
        
        if load['bol_signed']:
            st.success("✅ BOL already uploaded")
            if load['bol_document_url']:
                st.write(f"Document: {load['bol_document_url']}")
        else:
            # Upload interface
            uploaded_file = st.file_uploader(
                "Upload Signed BOL",
                type=['pdf', 'jpg', 'jpeg', 'png'],
                help="Take a photo or scan the signed BOL"
            )
            
            bol_number = st.text_input("BOL Number", value=load['bol_number'] or "")
            
            if uploaded_file and st.button("📤 Upload BOL", type="primary"):
                with st.spinner("Uploading document..."):
                    # In production, would upload to Vector API
                    # For now, just mark as uploaded
                    execute_query("""
                        UPDATE loads 
                        SET bol_signed = 1, 
                            bol_number = ?,
                            bol_document_url = ?,
                            updated_at = ?
                        WHERE id = ?
                    """, (bol_number, f"doc_{load_id}_{uploaded_file.name}", 
                         datetime.now(), load_id))
                    
                    st.success("✅ BOL uploaded successfully!")
                    st.rerun()
        
        # Other documents section
        st.markdown("### 📎 Additional Documents")
        
        other_docs = st.file_uploader(
            "Upload Other Documents",
            type=['pdf', 'jpg', 'jpeg', 'png'],
            accept_multiple_files=True,
            help="Receipts, weight tickets, etc."
        )
        
        if other_docs:
            for doc in other_docs:
                st.write(f"• {doc.name}")
            
            if st.button("📤 Upload Additional Documents"):
                st.success(f"✅ Uploaded {len(other_docs)} document(s)")


def show_hos_status():
    """Show Hours of Service status"""
    
    st.subheader("⏰ Hours of Service (HOS)")
    
    # In production, would get from Motive API
    # For now, show simulated data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Drive Time", "7h 30m", delta="3h 30m remaining")
    
    with col2:
        st.metric("On Duty Time", "10h 15m", delta="3h 45m remaining")
    
    with col3:
        st.metric("Cycle Time", "55h", delta="15h remaining")
    
    with col4:
        st.metric("Break Time", "30m", delta="Required in 2h")
    
    # HOS status chart
    st.markdown("### 📊 Today's Log")
    
    # Simulated log data
    log_data = {
        "12:00 AM - 6:00 AM": "Off Duty",
        "6:00 AM - 6:30 AM": "On Duty",
        "6:30 AM - 10:00 AM": "Driving",
        "10:00 AM - 10:30 AM": "On Duty",
        "10:30 AM - 2:00 PM": "Driving",
        "2:00 PM - Present": "On Duty"
    }
    
    for time_range, status in log_data.items():
        color = {
            "Off Duty": "🟢",
            "Sleeper": "🔵",
            "Driving": "🔴",
            "On Duty": "🟡"
        }.get(status, "⚪")
        
        st.write(f"{color} **{time_range}:** {status}")
    
    # Violation warnings
    st.markdown("### ⚠️ Warnings")
    st.info("No HOS violations detected")


def show_copilot_assistant():
    """Show AI co-pilot assistant"""
    
    st.subheader("💬 Your Co-Pilot Assistant")
    
    st.info("""
    🤖 **Co-Pilot Ready to Assist!**
    
    I can help you with:
    - Navigation and routing
    - Load information
    - Check-in reminders
    - HOS management
    - Weather updates
    - Truck stop locations
    """)
    
    # Chat interface
    if 'driver_messages' not in st.session_state:
        st.session_state.driver_messages = []
    
    # Display chat history
    for message in st.session_state.driver_messages:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Co-Pilot:** {message['content']}")
    
    # Input area
    user_input = st.text_input("Ask your co-pilot:", key="copilot_input")
    
    if st.button("Send") and user_input:
        # Add user message
        st.session_state.driver_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Generate response based on keywords
        response = generate_copilot_response(user_input)
        
        st.session_state.driver_messages.append({
            'role': 'assistant',
            'content': response
        })
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗺️ Next Rest Area"):
            response = "The next rest area is in 23 miles on I-40 East, Exit 142"
            st.info(response)
    
    with col2:
        if st.button("⛽ Nearest Fuel"):
            response = "Pilot Travel Center - 5 miles ahead, Exit 135, Diesel: $3.89/gal"
            st.info(response)
    
    with col3:
        if st.button("🌤️ Weather Ahead"):
            response = "Clear skies for the next 100 miles. Temperature: 72°F"
            st.info(response)


def show_completed_loads():
    """Show recently completed loads"""
    
    st.markdown("### 📋 Recent Completed Loads")
    
    completed = execute_query("""
        SELECT load_id, customer, delivery_date, gross_amount
        FROM loads
        WHERE driver_id = ?
        AND status = 'completed'
        ORDER BY delivery_date DESC
        LIMIT 5
    """, (st.session_state.get('user_id', 1),))
    
    if completed:
        for load in completed:
            with st.expander(f"Load {load['load_id']} - {load['delivery_date']}"):
                st.write(f"**Customer:** {load['customer']}")
                st.write(f"**Amount:** ${load['gross_amount']:,.2f}")
    else:
        st.info("No completed loads yet")


def update_load_status(load_id, new_status):
    """Update load status in database"""
    execute_query("""
        UPDATE loads 
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, datetime.now(), load_id))


def check_in_at_location(load_id, location_type, timestamp=None):
    """Check in at a location"""
    if timestamp is None:
        timestamp = datetime.now()
    
    field_map = {
        'pickup_arrival': 'pickup_arrival_time',
        'pickup_departure': 'pickup_departure_time',
        'delivery_arrival': 'delivery_arrival_time',
        'delivery_departure': 'delivery_departure_time'
    }
    
    field = field_map.get(location_type)
    if field:
        execute_query(f"""
            UPDATE loads 
            SET {field} = ?, updated_at = ?
            WHERE id = ?
        """, (timestamp, datetime.now(), load_id))


def report_delay(load_id, reason, duration):
    """Report a delay for a load"""
    execute_query("""
        INSERT INTO delays (
            load_id, delay_type, delay_reason, 
            delay_duration_minutes, reported_by
        ) VALUES (?, 'operational', ?, ?, ?)
    """, (load_id, reason, duration, st.session_state.get('user_id', 1)))


def generate_copilot_response(user_input):
    """Generate co-pilot response based on input"""
    
    input_lower = user_input.lower()
    
    if any(word in input_lower for word in ['weather', 'rain', 'snow', 'storm']):
        return "Current weather is clear with temperatures around 72°F. No severe weather warnings for your route."
    
    elif any(word in input_lower for word in ['fuel', 'gas', 'diesel']):
        return "Nearest fuel stop: Pilot Travel Center, 5 miles ahead at Exit 135. Current diesel price: $3.89/gal"
    
    elif any(word in input_lower for word in ['rest', 'break', 'sleep']):
        return "Next rest area in 23 miles. You have 2 hours of drive time before mandatory break."
    
    elif any(word in input_lower for word in ['traffic', 'accident', 'delay']):
        return "No major traffic incidents on your route. Estimated arrival time remains unchanged."
    
    elif any(word in input_lower for word in ['load', 'delivery', 'pickup']):
        return "Your current load is on schedule. Next stop: delivery at the destination address."
    
    else:
        return "I'm here to help! Ask me about weather, fuel stops, rest areas, traffic, or your current load."