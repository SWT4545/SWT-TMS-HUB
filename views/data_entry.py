"""
Data Entry View for Smith & Williams Trucking TMS
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from modules.ui_components import show_data_protection_footer
from modules.ui_enhancements import add_cancel_button, confirmation_dialog, auto_save_form
from modules.api_integrations import GoogleMapsAPI

def show_data_feeder_view():
    """Display data entry interface for loads, drivers, and customers"""
    
    st.title("📝 Data Entry Portal")
    st.markdown(f"### Data Feeder: {st.session_state.get('user_full_name', 'User')}")
    
    # Main tabs for different data entry types
    tab1, tab2, tab3, tab4 = st.tabs(["📦 New Load", "🚛 Driver Info", "🏢 Customer", "📋 Quick Entry"])
    
    with tab1:
        show_load_entry()
    
    with tab2:
        show_driver_entry()
    
    with tab3:
        show_customer_entry()
    
    with tab4:
        show_quick_entry()
    
    # Data Protection Footer
    show_data_protection_footer()

def show_load_entry():
    """Load entry form"""
    st.markdown("## Create New Load")
    
    # Initialize Google Maps API
    gmaps = GoogleMapsAPI()
    
    with st.form("new_load_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📍 Pickup Information")
            load_number = st.text_input("Load Number*", value=f"SWT{datetime.now().strftime('%Y%m%d%H%M')}")
            customer = st.selectbox("Customer*", ["Select Customer", "ABC Corp", "XYZ Industries", "Global Logistics"])
            pickup_date = st.date_input("Pickup Date*", value=date.today())
            pickup_time = st.time_input("Pickup Time*")
            pickup_address = st.text_input("Pickup Address*")
            pickup_city = st.text_input("Pickup City*")
            pickup_state = st.text_input("Pickup State*", max_chars=2)
            pickup_zip = st.text_input("Pickup ZIP")
        
        with col2:
            st.markdown("### 📍 Delivery Information")
            delivery_date = st.date_input("Delivery Date*", value=date.today())
            delivery_time = st.time_input("Delivery Time*")
            delivery_address = st.text_input("Delivery Address*")
            delivery_city = st.text_input("Delivery City*")
            delivery_state = st.text_input("Delivery State*", max_chars=2)
            delivery_zip = st.text_input("Delivery ZIP")
            
            st.markdown("### 📦 Load Details")
            commodity = st.text_input("Commodity")
            weight = st.number_input("Weight (lbs)", min_value=0)
            rate = st.number_input("Rate ($)", min_value=0.0, format="%.2f")
        
        # Calculate distance if addresses provided
        if pickup_address and pickup_city and delivery_address and delivery_city:
            origin = f"{pickup_address}, {pickup_city}, {pickup_state}"
            destination = f"{delivery_address}, {delivery_city}, {delivery_state}"
            
            distance_info = gmaps.calculate_distance(origin, destination)
            
            if 'error' not in distance_info:
                st.info(f"""
                📏 **Distance:** {distance_info.get('distance_text', 'N/A')}  
                ⏱️ **Est. Drive Time:** {distance_info.get('duration_text', 'N/A')}  
                💰 **Rate per Mile:** ${rate / distance_info.get('distance_miles', 1):.2f}/mi
                """)
        
        st.markdown("### 📝 Additional Information")
        special_instructions = st.text_area("Special Instructions", height=100)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            cancel = st.form_submit_button("❌ Cancel", use_container_width=True)
        with col2:
            save_draft = st.form_submit_button("💾 Save Draft", use_container_width=True)
        with col3:
            submitted = st.form_submit_button("✅ Create Load", type="primary", use_container_width=True)
        
        if cancel:
            st.warning("Load creation cancelled")
            st.session_state.clear()
            st.rerun()
        
        if save_draft:
            # Auto-save functionality
            form_data = {
                'load_number': load_number,
                'customer': customer,
                'pickup_date': pickup_date,
                'pickup_address': pickup_address,
                'delivery_address': delivery_address,
                'rate': rate
            }
            auto_save_form("load_entry", form_data)
            st.info("Draft saved!")
        
        if submitted:
            # Confirmation dialog
            if confirmation_dialog(f"Create load {load_number}?"):
                st.success(f"✅ Load {load_number} created successfully!")
            else:
                st.info("Load creation cancelled")

def show_driver_entry():
    """Driver information entry form"""
    st.markdown("## Driver Information")
    
    with st.form("driver_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 👤 Personal Information")
            driver_id = st.text_input("Driver ID*", value=f"DRV{datetime.now().strftime('%Y%m%d')}")
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            phone = st.text_input("Phone Number*")
            email = st.text_input("Email")
            
        with col2:
            st.markdown("### 📄 License Information")
            cdl_number = st.text_input("CDL Number*")
            cdl_state = st.text_input("CDL State*", max_chars=2)
            cdl_expiry = st.date_input("CDL Expiry Date*")
            medical_cert_expiry = st.date_input("Medical Certificate Expiry*")
            hazmat_endorsed = st.checkbox("HAZMAT Endorsed")
        
        st.markdown("### 🚛 Assignment")
        truck_number = st.selectbox("Assigned Truck", ["None", "Truck 001", "Truck 002", "Truck 003"])
        status = st.selectbox("Status", ["Active", "Inactive", "On Leave"])
        
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button("✅ Save Driver", type="primary", use_container_width=True)
        
        if submitted:
            st.success(f"✅ Driver {first_name} {last_name} saved successfully!")

def show_customer_entry():
    """Customer information entry form"""
    st.markdown("## Customer Information")
    
    with st.form("customer_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🏢 Company Information")
            customer_code = st.text_input("Customer Code*", value=f"CUST{datetime.now().strftime('%Y%m%d')}")
            company_name = st.text_input("Company Name*")
            contact_name = st.text_input("Primary Contact*")
            phone = st.text_input("Phone Number*")
            email = st.text_input("Email*")
        
        with col2:
            st.markdown("### 📍 Address")
            address = st.text_input("Street Address*")
            city = st.text_input("City*")
            state = st.text_input("State*", max_chars=2)
            zip_code = st.text_input("ZIP Code*")
            
        st.markdown("### 💰 Billing Information")
        col1, col2, col3 = st.columns(3)
        with col1:
            credit_limit = st.number_input("Credit Limit ($)", min_value=0.0, format="%.2f")
        with col2:
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "Net 45", "Net 60", "COD"])
        with col3:
            preferred_carrier = st.selectbox("Preferred Carrier", ["Any", "Company Fleet", "Owner Operator"])
        
        notes = st.text_area("Notes", height=100)
        
        col1, col2, col3 = st.columns(3)
        with col2:
            submitted = st.form_submit_button("✅ Save Customer", type="primary", use_container_width=True)
        
        if submitted:
            st.success(f"✅ Customer {company_name} saved successfully!")

def show_quick_entry():
    """Quick data entry for common tasks"""
    st.markdown("## Quick Entry")
    
    quick_action = st.selectbox("Select Quick Action", [
        "Update Load Status",
        "Assign Driver to Load",
        "Record Fuel Purchase",
        "Log Maintenance",
        "Update Truck Location"
    ])
    
    if quick_action == "Update Load Status":
        with st.form("quick_status"):
            load_number = st.text_input("Load Number*")
            new_status = st.selectbox("New Status", ["In Transit", "Delivered", "Delayed", "Cancelled"])
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Update Status", type="primary"):
                st.success(f"✅ Load {load_number} status updated to {new_status}")
    
    elif quick_action == "Assign Driver to Load":
        with st.form("quick_assign"):
            load_number = st.text_input("Load Number*")
            driver = st.selectbox("Driver", ["Select Driver", "John Smith", "Jane Doe", "Bob Johnson"])
            truck = st.selectbox("Truck", ["Select Truck", "Truck 001", "Truck 002", "Truck 003"])
            
            if st.form_submit_button("Assign", type="primary"):
                st.success(f"✅ {driver} assigned to Load {load_number}")
    
    elif quick_action == "Record Fuel Purchase":
        with st.form("quick_fuel"):
            truck = st.selectbox("Truck", ["Select Truck", "Truck 001", "Truck 002", "Truck 003"])
            gallons = st.number_input("Gallons", min_value=0.0, format="%.2f")
            price_per_gallon = st.number_input("Price per Gallon ($)", min_value=0.0, format="%.2f")
            location = st.text_input("Location")
            
            if st.form_submit_button("Record Fuel", type="primary"):
                total = gallons * price_per_gallon
                st.success(f"✅ Fuel purchase recorded: {gallons} gallons for ${total:.2f}")
    
    elif quick_action == "Log Maintenance":
        with st.form("quick_maintenance"):
            truck = st.selectbox("Truck", ["Select Truck", "Truck 001", "Truck 002", "Truck 003"])
            maintenance_type = st.selectbox("Type", ["Oil Change", "Tire Rotation", "Brake Service", "Other"])
            cost = st.number_input("Cost ($)", min_value=0.0, format="%.2f")
            description = st.text_area("Description")
            
            if st.form_submit_button("Log Maintenance", type="primary"):
                st.success(f"✅ Maintenance logged for {truck}")
    
    elif quick_action == "Update Truck Location":
        with st.form("quick_location"):
            truck = st.selectbox("Truck", ["Select Truck", "Truck 001", "Truck 002", "Truck 003"])
            city = st.text_input("Current City")
            state = st.text_input("Current State", max_chars=2)
            status = st.selectbox("Status", ["Moving", "Stopped", "Loading", "Unloading"])
            
            if st.form_submit_button("Update Location", type="primary"):
                st.success(f"✅ Location updated for {truck}: {city}, {state}")