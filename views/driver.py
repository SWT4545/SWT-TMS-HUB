"""
Driver Portal View for Smith & Williams Trucking TMS
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from modules.ui_components import show_data_protection_footer
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.motive_integration import MotiveIntegration, show_motive_dashboard

def show_driver_view():
    """Display driver portal with loads, routes, and documents"""
    
    st.title("🚛 Driver Portal")
    st.markdown(f"### Welcome, {st.session_state.get('user_full_name', 'Driver')}")
    
    # Driver Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Miles This Week", "2,345", "+12%")
    with col2:
        st.metric("Loads Completed", "8", "+2")
    with col3:
        st.metric("On-Time %", "95%", "+5%")
    with col4:
        st.metric("Safety Score", "98", "")
    
    st.markdown("---")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📋 Current Load", 
        "📍 GPS/ELD",
        "📅 Schedule", 
        "🗺️ Route Info", 
        "📄 Documents", 
        "💰 Earnings",
        "⏱️ HOS Status"
    ])
    
    with tab1:
        show_current_load()
    
    with tab2:
        show_gps_eld_integration()
    
    with tab3:
        show_driver_schedule()
    
    with tab4:
        show_route_info()
    
    with tab5:
        show_documents()
    
    with tab6:
        show_earnings()
    
    with tab7:
        show_hos_status()
    
    # Data Protection Footer
    show_data_protection_footer()

def show_current_load():
    """Display current load information"""
    st.markdown("## Current Load Details")
    
    # Load Status Card
    status_color = "#10b981"  # Green for in transit
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 10px; border-left: 5px solid {status_color};'>
        <h3 style='color: #DC2626; margin: 0;'>Load #SWT20250119001</h3>
        <p style='color: {status_color}; font-weight: 600; margin: 0.5rem 0;'>STATUS: IN TRANSIT</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Pickup")
        st.info("""
        **ABC Manufacturing**  
        123 Industrial Blvd  
        Memphis, TN 38101  
        
        **Date:** January 19, 2025  
        **Time:** 08:00 AM  
        **Status:** ✅ Completed
        """)
        
        st.markdown("### 📦 Load Information")
        st.write("**Commodity:** Electronics")
        st.write("**Weight:** 42,000 lbs")
        st.write("**Pieces:** 24 pallets")
        st.write("**Equipment:** 53' Dry Van")
    
    with col2:
        st.markdown("### 📍 Delivery")
        st.warning("""
        **XYZ Distribution Center**  
        456 Commerce Way  
        Atlanta, GA 30301  
        
        **Date:** January 20, 2025  
        **Time:** 02:00 PM  
        **Status:** ⏳ Pending
        """)
        
        st.markdown("### 📱 Contact Information")
        st.write("**Dispatcher:** John Smith")
        st.write("**Phone:** (901) 555-0123")
        st.write("**Customer Contact:** Jane Doe")
        st.write("**Customer Phone:** (404) 555-0456")
    
    st.markdown("### 🚦 Update Load Status")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📍 Arrived at Delivery", use_container_width=True):
            st.success("Status updated: Arrived at delivery location")
    
    with col2:
        if st.button("📦 Unloading", use_container_width=True):
            st.success("Status updated: Unloading in progress")
    
    with col3:
        if st.button("✅ Delivered", use_container_width=True):
            st.success("Load marked as delivered!")
    
    # Special Instructions
    with st.expander("📝 Special Instructions"):
        st.warning("""
        - Delivery appointment required - call ahead
        - Dock door #12
        - Bring load bars
        - Temperature sensitive - maintain 65-75°F
        """)

def show_driver_schedule():
    """Display driver's schedule"""
    st.markdown("## 📅 Your Schedule")
    
    # Schedule filter
    col1, col2 = st.columns([2, 1])
    with col1:
        schedule_view = st.selectbox("View", ["This Week", "Next Week", "This Month"])
    with col2:
        st.write("")  # Spacer
        if st.button("🔄 Refresh"):
            st.rerun()
    
    # Schedule data
    schedule_data = pd.DataFrame({
        'Date': ['Jan 19', 'Jan 20', 'Jan 21', 'Jan 22', 'Jan 23'],
        'Load #': ['SWT001', 'SWT002', 'SWT003', 'OFF', 'SWT004'],
        'Origin': ['Memphis, TN', 'Atlanta, GA', 'Nashville, TN', '-', 'Memphis, TN'],
        'Destination': ['Atlanta, GA', 'Nashville, TN', 'Memphis, TN', '-', 'Dallas, TX'],
        'Miles': [380, 245, 210, 0, 452],
        'Status': ['In Transit', 'Scheduled', 'Scheduled', 'Day Off', 'Scheduled']
    })
    
    # Style the dataframe
    def style_status(val):
        if val == 'In Transit':
            return 'background-color: #fef3c7'
        elif val == 'Day Off':
            return 'background-color: #dbeafe'
        return ''
    
    styled_df = schedule_data.style.applymap(style_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Weekly summary
    st.markdown("### 📊 Week Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Miles", "1,287")
    with col2:
        st.metric("Total Loads", "4")
    with col3:
        st.metric("Estimated Earnings", "$1,545")

def show_route_info():
    """Display route information"""
    st.markdown("## 🗺️ Route Information")
    
    # Current route
    st.markdown("### Current Route: Memphis, TN → Atlanta, GA")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Distance", "380 miles")
    with col2:
        st.metric("Estimated Time", "6h 15min")
    with col3:
        st.metric("ETA", "2:15 PM")
    
    # Route milestones
    st.markdown("### 📍 Route Milestones")
    milestones = pd.DataFrame({
        'Milestone': ['Start - Memphis, TN', 'Rest Stop - Tupelo, MS', 'Fuel - Birmingham, AL', 'Destination - Atlanta, GA'],
        'Distance': ['0 mi', '101 mi', '237 mi', '380 mi'],
        'Time': ['8:00 AM', '9:45 AM', '11:30 AM', '2:15 PM'],
        'Status': ['✅ Completed', '✅ Completed', '🔄 Next Stop', '⏳ Pending']
    })
    st.dataframe(milestones, use_container_width=True, hide_index=True)
    
    # Fuel stops
    with st.expander("⛽ Recommended Fuel Stops"):
        st.info("""
        **Love's Travel Stop** - Birmingham, AL (Mile 237)
        - Current Price: $3.89/gal
        - Amenities: Showers, Restaurant, Parking
        
        **Pilot Flying J** - Meridian, MS (Mile 154)
        - Current Price: $3.92/gal
        - Amenities: Showers, Subway, Parking
        """)
    
    # Weather alerts
    with st.expander("🌤️ Weather Conditions"):
        st.warning("""
        **Current Conditions:** Clear
        **Temperature:** 42°F
        **Wind:** 8 mph NW
        
        ⚠️ **Alert:** Light rain expected near Atlanta after 3 PM
        """)

def show_documents():
    """Display and manage driver documents"""
    st.markdown("## 📄 Documents")
    
    tab1, tab2, tab3 = st.tabs(["Required Documents", "Load Documents", "Upload"])
    
    with tab1:
        st.markdown("### Required Documents Status")
        
        docs_data = pd.DataFrame({
            'Document': ['CDL', 'Medical Certificate', 'HAZMAT Endorsement', 'Insurance Card', 'Vehicle Registration'],
            'Status': ['✅ Valid', '✅ Valid', '⚠️ Expires Soon', '✅ Valid', '✅ Valid'],
            'Expiry Date': ['12/31/2026', '06/15/2025', '02/28/2025', '12/31/2025', '03/31/2025']
        })
        
        st.dataframe(docs_data, use_container_width=True, hide_index=True)
        
        st.warning("⚠️ Your HAZMAT Endorsement expires in 40 days. Please renew soon.")
    
    with tab2:
        st.markdown("### Current Load Documents")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download BOL", use_container_width=True):
                st.info("Downloading Bill of Lading...")
        with col2:
            if st.button("📥 Download Rate Confirmation", use_container_width=True):
                st.info("Downloading Rate Confirmation...")
        
        st.markdown("### Recent Documents")
        recent_docs = pd.DataFrame({
            'Date': ['Jan 18', 'Jan 17', 'Jan 16'],
            'Load #': ['SWT999', 'SWT998', 'SWT997'],
            'Type': ['POD', 'BOL', 'POD'],
            'Action': ['View', 'View', 'View']
        })
        st.dataframe(recent_docs, use_container_width=True, hide_index=True)
    
    with tab3:
        st.markdown("### Upload Documents")
        
        doc_type = st.selectbox("Document Type", [
            "Proof of Delivery (POD)",
            "Bill of Lading (BOL)",
            "Lumper Receipt",
            "Scale Ticket",
            "Fuel Receipt",
            "Other"
        ])
        
        load_number = st.text_input("Load Number (if applicable)")
        
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'jpg', 'png', 'jpeg'])
        
        if uploaded_file is not None:
            st.success(f"✅ File '{uploaded_file.name}' ready to upload")
            if st.button("Upload Document", type="primary"):
                st.success("Document uploaded successfully!")

def show_earnings():
    """Display driver earnings and settlements"""
    st.markdown("## 💰 Earnings & Settlements")
    
    # Current period earnings
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Week", "$1,545", "+$245")
    with col2:
        st.metric("Current Month", "$6,230", "+$1,230")
    with col3:
        st.metric("YTD Earnings", "$12,460", "")
    
    st.markdown("---")
    
    # Detailed earnings breakdown
    st.markdown("### 📊 This Week's Breakdown")
    
    earnings_data = pd.DataFrame({
        'Date': ['Jan 15', 'Jan 16', 'Jan 17', 'Jan 18', 'Jan 19'],
        'Load #': ['SWT995', 'SWT996', 'SWT997', 'SWT998', 'SWT999'],
        'Miles': [320, 285, 412, 268, 380],
        'Rate/Mile': ['$1.20', '$1.25', '$1.18', '$1.22', '$1.20'],
        'Total': ['$384', '$356', '$486', '$327', '$456'],
        'Status': ['Paid', 'Paid', 'Pending', 'Pending', 'In Progress']
    })
    
    st.dataframe(earnings_data, use_container_width=True, hide_index=True)
    
    # Additional earnings
    with st.expander("➕ Additional Earnings"):
        add_earnings = pd.DataFrame({
            'Type': ['Detention', 'Layover', 'Extra Stop', 'Hand Unload'],
            'Amount': ['$50', '$75', '$40', '$100'],
            'Date': ['Jan 16', 'Jan 17', 'Jan 18', 'Jan 19']
        })
        st.dataframe(add_earnings, use_container_width=True, hide_index=True)
    
    # Deductions
    with st.expander("➖ Deductions"):
        deductions = pd.DataFrame({
            'Type': ['Fuel Advance', 'Insurance', 'ELD Service'],
            'Amount': ['-$200', '-$45', '-$35'],
            'Date': ['Jan 15', 'Jan 15', 'Jan 15']
        })
        st.dataframe(deductions, use_container_width=True, hide_index=True)
    
    # Settlement summary
    st.markdown("### 💳 Next Settlement")
    st.info("""
    **Settlement Date:** January 22, 2025  
    **Estimated Amount:** $1,265  
    **Payment Method:** Direct Deposit  
    **Bank:** On file ending in ...4567
    """)
    
    if st.button("📄 View Settlement Statement"):
        st.info("Loading settlement statement...")

def show_gps_eld_integration():
    """Display GPS/ELD integration from Motive"""
    st.markdown("## 📍 GPS/ELD Integration (Motive)")
    
    # Initialize Motive integration
    motive = MotiveIntegration()
    
    # Get current location and HOS data
    location = motive.fetch_current_location()
    hos = motive.fetch_hos_status()
    
    # Quick status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if location:
            st.metric("Current Speed", f"{location.get('speed', 0):.1f} mph")
        else:
            st.metric("Current Speed", "0 mph")
    
    with col2:
        if hos:
            st.metric("Duty Status", hos.get('duty_status', 'Off Duty'))
        else:
            st.metric("Duty Status", "Off Duty")
    
    with col3:
        if location:
            st.metric("Odometer", f"{location.get('odometer', 0):,.0f} mi")
        else:
            st.metric("Odometer", "Loading...")
    
    with col4:
        if location:
            fuel = location.get('fuel_level', 50)
            st.metric("Fuel Level", f"{fuel:.0f}%")
        else:
            st.metric("Fuel Level", "Loading...")
    
    st.markdown("---")
    
    # Location details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Current Location")
        if location:
            st.info(f"""
            **Address:** {location.get('address', 'Unknown')}  
            **City:** {location.get('city', 'Unknown')}  
            **State:** {location.get('state', 'Unknown')}  
            **Coordinates:** {location.get('latitude', 0):.6f}, {location.get('longitude', 0):.6f}  
            **Heading:** {location.get('heading', 0)}°  
            **Engine Hours:** {location.get('engine_hours', 0):,.1f}
            """)
        else:
            st.info("Location data loading...")
        
        if st.button("🔄 Refresh Location", key="refresh_gps"):
            new_location = motive.fetch_current_location()
            if new_location:
                st.success("Location updated!")
                st.rerun()
    
    with col2:
        st.markdown("### ⏱️ Hours of Service")
        if hos:
            # Calculate hours from minutes
            drive_hours = hos.get('drive_time_remaining', 0) / 60
            shift_hours = hos.get('shift_time_remaining', 0) / 60
            cycle_hours = hos.get('cycle_time_remaining', 0) / 60
            
            st.write(f"**Drive Time Remaining:** {drive_hours:.1f} hours")
            st.progress(min(drive_hours / 11, 1.0))
            
            st.write(f"**Shift Time Remaining:** {shift_hours:.1f} hours")
            st.progress(min(shift_hours / 14, 1.0))
            
            st.write(f"**Cycle Time Remaining:** {cycle_hours:.1f} hours")
            st.progress(min(cycle_hours / 70, 1.0))
            
            if hos.get('break_time_remaining', 0) > 0:
                st.warning(f"⚠️ Break required in {hos['break_time_remaining']} minutes")
        else:
            st.info("HOS data loading...")
    
    # Vehicle diagnostics
    st.markdown("### 🚛 Vehicle Diagnostics")
    
    diagnostics = motive.get_vehicle_diagnostics()
    
    if diagnostics:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            oil_pressure = diagnostics.get('oil_pressure', 35)
            st.metric("Oil Pressure", f"{oil_pressure:.1f} psi")
            if oil_pressure < 25 or oil_pressure > 45:
                st.warning("Check oil pressure!")
        
        with col2:
            coolant_temp = diagnostics.get('coolant_temp', 195)
            st.metric("Coolant Temp", f"{coolant_temp:.0f}°F")
            if coolant_temp > 210:
                st.warning("High temperature!")
        
        with col3:
            battery = diagnostics.get('battery_voltage', 14.0)
            st.metric("Battery", f"{battery:.1f}V")
            if battery < 13.0:
                st.warning("Low voltage!")
        
        with col4:
            fuel_economy = diagnostics.get('fuel_economy', 6.5)
            st.metric("Fuel Economy", f"{fuel_economy:.1f} mpg")
        
        # DEF level
        def_level = diagnostics.get('def_level', 50)
        st.write(f"**DEF Level:** {def_level:.0f}%")
        st.progress(def_level / 100)
        if def_level < 20:
            st.warning("⚠️ Low DEF level - refill soon!")
        
        # Engine light
        if diagnostics.get('engine_light'):
            st.error("🔴 Check Engine Light ON - Contact maintenance")
        else:
            st.success("✅ No engine warnings")
    
    # Trip summary for today
    st.markdown("### 📊 Today's Trip Summary")
    
    summary = motive.get_trip_summary(date.today(), date.today())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Miles Driven", f"{summary.get('total_miles', 0):,.0f}")
    
    with col2:
        st.metric("Fuel Used", f"{summary.get('total_fuel', 0):.1f} gal")
    
    with col3:
        drive_time = summary.get('total_drive_time', 0) / 60
        st.metric("Drive Time", f"{drive_time:.1f} hrs")
    
    with col4:
        idle_time = summary.get('total_idle_time', 0) / 60
        st.metric("Idle Time", f"{idle_time:.1f} hrs")
    
    # Sync button
    if st.button("🔄 Sync with Active Loads", type="primary"):
        synced = motive.sync_with_shipments()
        st.success(f"Synced {synced} active shipments with GPS data")

def show_hos_status():
    """Display detailed Hours of Service status"""
    st.markdown("## ⏱️ Hours of Service Status")
    
    # Initialize Motive integration
    motive = MotiveIntegration()
    hos = motive.fetch_hos_status()
    
    if hos:
        # Current status
        status_color = {
            'Driving': '#ef4444',
            'On Duty': '#f59e0b', 
            'Off Duty': '#10b981',
            'Sleeper': '#3b82f6'
        }.get(hos.get('duty_status', 'Off Duty'), '#6b7280')
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 10px; border-left: 5px solid {status_color};'>
            <h3 style='color: {status_color}; margin: 0;'>Current Status: {hos.get('duty_status', 'Off Duty')}</h3>
            <p style='margin: 0.5rem 0;'>Duration: {hos.get('duty_status_duration', 0)} minutes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Time remaining gauges
        st.markdown("### ⏰ Time Remaining")
        
        col1, col2 = st.columns(2)
        
        with col1:
            drive_hours = hos.get('drive_time_remaining', 0) / 60
            st.markdown("#### Driving Time")
            st.write(f"**{drive_hours:.1f} hours** remaining of 11 hours")
            st.progress(min(drive_hours / 11, 1.0))
            
            shift_hours = hos.get('shift_time_remaining', 0) / 60
            st.markdown("#### Shift Time")
            st.write(f"**{shift_hours:.1f} hours** remaining of 14 hours")
            st.progress(min(shift_hours / 14, 1.0))
        
        with col2:
            cycle_hours = hos.get('cycle_time_remaining', 0) / 60
            st.markdown("#### Cycle Time (70/8)")
            st.write(f"**{cycle_hours:.1f} hours** remaining of 70 hours")
            st.progress(min(cycle_hours / 70, 1.0))
            
            break_mins = hos.get('break_time_remaining', 0)
            if break_mins > 0:
                st.markdown("#### Break Required")
                st.write(f"**{break_mins} minutes** until break required")
                st.progress(max(1 - (break_mins / 30), 0))
                st.warning("⚠️ Plan for upcoming break")
        
        # Status change buttons
        st.markdown("### 🔄 Change Duty Status")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🚗 Driving", use_container_width=True, disabled=(hos.get('duty_status') == 'Driving')):
                st.success("Status changed to: Driving")
        
        with col2:
            if st.button("👷 On Duty", use_container_width=True, disabled=(hos.get('duty_status') == 'On Duty')):
                st.success("Status changed to: On Duty")
        
        with col3:
            if st.button("🏠 Off Duty", use_container_width=True, disabled=(hos.get('duty_status') == 'Off Duty')):
                st.success("Status changed to: Off Duty")
        
        with col4:
            if st.button("🛏️ Sleeper", use_container_width=True, disabled=(hos.get('duty_status') == 'Sleeper')):
                st.success("Status changed to: Sleeper Berth")
        
        # Recent status log
        st.markdown("### 📜 Recent Status Changes")
        
        cursor = motive.conn.cursor()
        cursor.execute("""
            SELECT duty_status, timestamp, duty_status_duration
            FROM motive_hos_data
            WHERE driver_id = ?
            ORDER BY timestamp DESC
            LIMIT 8
        """, (motive.driver_info['motive_driver_id'],))
        
        logs = cursor.fetchall()
        
        if logs:
            log_data = []
            for log in logs:
                log_data.append({
                    'Status': log[0],
                    'Start Time': datetime.fromisoformat(str(log[1])).strftime('%m/%d %I:%M %p'),
                    'Duration': f"{log[2]} min" if log[2] else "Current"
                })
            
            st.dataframe(pd.DataFrame(log_data), use_container_width=True, hide_index=True)
        else:
            # Show sample data
            sample_data = pd.DataFrame({
                'Status': ['Off Duty', 'Driving', 'On Duty', 'Driving', 'Off Duty'],
                'Start Time': ['01/20 06:00 AM', '01/20 07:00 AM', '01/20 11:30 AM', 
                              '01/20 12:00 PM', '01/20 05:00 PM'],
                'Duration': ['60 min', '270 min', '30 min', '300 min', 'Current']
            })
            st.dataframe(sample_data, use_container_width=True, hide_index=True)
        
        # Violations check
        st.markdown("### ⚠️ Violation Check")
        
        if hos.get('current_violation'):
            st.error(f"🚨 Active Violation: {hos['current_violation']}")
            st.write("Take immediate action to resolve this violation")
        else:
            st.success("✅ No violations - You're in compliance!")
        
        # Tips
        with st.expander("💡 HOS Tips & Reminders"):
            st.info("""
            **Daily Limits:**
            - Maximum 11 hours driving
            - Maximum 14 hours on duty
            - Mandatory 30-minute break after 8 hours driving
            - 10 hours off duty required before starting new shift
            
            **Weekly Limits:**
            - Maximum 60 hours in 7 days
            - Maximum 70 hours in 8 days
            - 34-hour restart resets weekly hours
            
            **Best Practices:**
            - Plan breaks during loading/unloading
            - Use sleeper berth for split breaks
            - Monitor your hours throughout the day
            - Keep paper logs as backup
            """)
    else:
        st.warning("Unable to fetch HOS data. Using last known status.")