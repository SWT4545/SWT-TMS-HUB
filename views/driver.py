"""
Driver Portal View for Smith & Williams Trucking TMS
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from modules.ui_components import show_data_protection_footer

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
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Current Load", 
        "📅 Schedule", 
        "🗺️ Route Info", 
        "📄 Documents", 
        "💰 Earnings"
    ])
    
    with tab1:
        show_current_load()
    
    with tab2:
        show_driver_schedule()
    
    with tab3:
        show_route_info()
    
    with tab4:
        show_documents()
    
    with tab5:
        show_earnings()
    
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