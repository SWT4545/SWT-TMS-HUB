"""
Data Entry View for SWT TMS Hub
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.database import get_connection
from modules.ui_components import show_page_header, show_success_message, show_error_message

def show_data_feeder_view():
    """Display data entry interface for shipments and customers"""
    show_page_header(
        "📝 Data Entry & Management", 
        "Add and manage shipments, customers, and operational data"
    )
    
    tabs = st.tabs(["📦 New Shipment", "🏢 Customers", "🚛 Fleet", "👥 Drivers"])
    
    with tabs[0]:
        show_shipment_entry()
    
    with tabs[1]:
        show_customer_management()
    
    with tabs[2]:
        show_fleet_management()
    
    with tabs[3]:
        show_driver_management()

def show_shipment_entry():
    """Shipment entry form"""
    st.subheader("Create New Shipment")
    
    with st.form("new_shipment"):
        # Basic shipment info
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📋 Shipment Details")
            load_number = st.text_input(
                "Load Number*", 
                value=f"L{datetime.now().strftime('%Y%m%d%H%M')}"
            )
            
            # Get customers for dropdown
            conn = get_connection()
            customers = pd.read_sql_query(
                "SELECT id, company_name FROM customers WHERE is_active = 1", 
                conn
            )
            
            if not customers.empty:
                customer_options = dict(zip(customers['company_name'], customers['id']))
                customer_name = st.selectbox("Customer*", options=list(customer_options.keys()))
                customer_id = customer_options[customer_name]
            else:
                st.warning("No customers available. Please add customers first.")
                customer_id = None
            
            commodity = st.text_input("Commodity")
            weight = st.number_input("Weight (lbs)", min_value=0.0, step=100.0)
            pieces = st.number_input("Pieces", min_value=0, step=1)
            equipment_type = st.selectbox(
                "Equipment Type", 
                ["Dry Van", "Reefer", "Flatbed", "Step Deck", "RGN", "Tanker"]
            )
        
        with col2:
            st.markdown("##### 💰 Rate Information")
            rate = st.number_input("Rate ($)*", min_value=0.0, step=100.0)
            miles = st.number_input("Miles", min_value=0, step=1)
            fuel_surcharge = st.number_input("Fuel Surcharge (%)", min_value=0.0, max_value=100.0, step=0.1)
            special_instructions = st.text_area("Special Instructions")
        
        st.markdown("---")
        
        # Origin and destination
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 📍 Origin")
            origin_address = st.text_input("Address*")
            origin_city = st.text_input("City*")
            origin_state = st.text_input("State*", max_chars=2, placeholder="CA")
            origin_zip = st.text_input("ZIP Code")
            pickup_date = st.date_input("Pickup Date*", value=datetime.now().date())
            pickup_time = st.time_input("Pickup Time", value=datetime.now().time())
        
        with col2:
            st.markdown("##### 🎯 Destination")
            dest_address = st.text_input("Address*", key="dest_addr")
            dest_city = st.text_input("City*", key="dest_city")
            dest_state = st.text_input("State*", max_chars=2, placeholder="NY", key="dest_state")
            dest_zip = st.text_input("ZIP Code", key="dest_zip")
            delivery_date = st.date_input("Delivery Date*", value=datetime.now().date() + timedelta(days=1))
            delivery_time = st.time_input("Delivery Time", key="del_time")
        
        # Submit button
        submitted = st.form_submit_button("✅ Create Shipment", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            required_fields = [
                (load_number, "Load Number"),
                (customer_id, "Customer"),
                (origin_city, "Origin City"),
                (origin_state, "Origin State"),
                (dest_city, "Destination City"),
                (dest_state, "Destination State"),
                (rate, "Rate")
            ]
            
            missing_fields = [field[1] for field in required_fields if not field[0]]
            
            if missing_fields:
                show_error_message(f"Missing required fields: {', '.join(missing_fields)}")
            else:
                # Insert shipment
                try:
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO shipments 
                        (load_number, customer_id, origin_address, origin_city, origin_state, origin_zip,
                         destination_address, destination_city, destination_state, destination_zip,
                         pickup_date, pickup_time, delivery_date, delivery_time,
                         weight, pieces, commodity, equipment_type, rate, miles, special_instructions)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (load_number, customer_id, origin_address, origin_city, origin_state, origin_zip,
                         dest_address, dest_city, dest_state, dest_zip,
                         pickup_date, str(pickup_time), delivery_date, str(delivery_time),
                         weight, pieces, commodity, equipment_type, rate, miles, special_instructions))
                    conn.commit()
                    show_success_message(f"Shipment {load_number} created successfully!")
                    st.balloons()
                except Exception as e:
                    show_error_message(f"Error creating shipment: {str(e)}")
            
            conn.close()

def show_customer_management():
    """Customer management interface"""
    st.subheader("Customer Management")
    
    # View/Edit customers
    conn = get_connection()
    customers = pd.read_sql_query("""
        SELECT customer_code, company_name, contact_name, phone, email, 
               city, state, is_active, created_at
        FROM customers 
        ORDER BY company_name
    """, conn)
    
    if not customers.empty:
        st.markdown("#### Existing Customers")
        st.dataframe(customers, use_container_width=True, hide_index=True)
    
    # Add new customer
    st.markdown("#### Add New Customer")
    
    with st.form("new_customer"):
        col1, col2 = st.columns(2)
        
        with col1:
            customer_code = st.text_input("Customer Code*", placeholder="CUST001")
            company_name = st.text_input("Company Name*")
            contact_name = st.text_input("Contact Name")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
        
        with col2:
            address = st.text_input("Address")
            city = st.text_input("City")
            state = st.text_input("State", max_chars=2)
            zip_code = st.text_input("ZIP Code")
            credit_limit = st.number_input("Credit Limit ($)", min_value=0.0, step=1000.0)
            payment_terms = st.selectbox("Payment Terms", ["Net 30", "Net 15", "COD", "Prepaid"])
        
        if st.form_submit_button("➕ Add Customer", type="primary"):
            if customer_code and company_name:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO customers 
                        (customer_code, company_name, contact_name, phone, email,
                         address, city, state, zip_code, credit_limit, payment_terms)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (customer_code, company_name, contact_name, phone, email,
                         address, city, state, zip_code, credit_limit, payment_terms))
                    conn.commit()
                    show_success_message(f"Customer {company_name} added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error_message(f"Error adding customer: {str(e)}")
            else:
                show_error_message("Customer Code and Company Name are required")
    
    conn.close()

def show_fleet_management():
    """Fleet management interface"""
    st.subheader("Fleet Management")
    
    conn = get_connection()
    
    # Show existing trucks
    trucks = pd.read_sql_query("""
        SELECT t.truck_number, t.make, t.model, t.year, t.status,
               c.carrier_name, t.current_location, t.is_active
        FROM trucks t
        LEFT JOIN carriers c ON t.carrier_id = c.id
        ORDER BY t.truck_number
    """, conn)
    
    if not trucks.empty:
        st.markdown("#### Fleet Status")
        st.dataframe(trucks, use_container_width=True, hide_index=True)
    
    # Add new truck
    st.markdown("#### Add New Truck")
    
    with st.form("new_truck"):
        col1, col2 = st.columns(2)
        
        with col1:
            truck_number = st.text_input("Truck Number*", placeholder="T001")
            make = st.text_input("Make")
            model = st.text_input("Model")
            year = st.number_input("Year", min_value=1990, max_value=datetime.now().year + 1)
            vin = st.text_input("VIN")
        
        with col2:
            license_plate = st.text_input("License Plate")
            status = st.selectbox("Status", ["Available", "In Transit", "Out of Service", "Maintenance"])
            current_location = st.text_input("Current Location")
            last_inspection = st.date_input("Last Inspection Date")
        
        if st.form_submit_button("🚛 Add Truck", type="primary"):
            if truck_number:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO trucks 
                        (truck_number, make, model, year, vin, license_plate, 
                         status, current_location, last_inspection)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (truck_number, make, model, year, vin, license_plate,
                         status, current_location, last_inspection))
                    conn.commit()
                    show_success_message(f"Truck {truck_number} added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error_message(f"Error adding truck: {str(e)}")
            else:
                show_error_message("Truck Number is required")
    
    conn.close()

def show_driver_management():
    """Driver management interface"""
    st.subheader("Driver Management")
    
    conn = get_connection()
    
    # Show existing drivers
    drivers = pd.read_sql_query("""
        SELECT d.driver_code, d.first_name, d.last_name, d.cdl_number,
               d.phone, d.status, c.carrier_name, d.is_active
        FROM drivers d
        LEFT JOIN carriers c ON d.carrier_id = c.id
        ORDER BY d.last_name, d.first_name
    """, conn)
    
    if not drivers.empty:
        st.markdown("#### Driver Roster")
        st.dataframe(drivers, use_container_width=True, hide_index=True)
    
    # Add new driver
    st.markdown("#### Add New Driver")
    
    with st.form("new_driver"):
        col1, col2 = st.columns(2)
        
        with col1:
            driver_code = st.text_input("Driver Code*", placeholder="D001")
            first_name = st.text_input("First Name*")
            last_name = st.text_input("Last Name*")
            phone = st.text_input("Phone")
            email = st.text_input("Email")
        
        with col2:
            cdl_number = st.text_input("CDL Number")
            cdl_state = st.text_input("CDL State", max_chars=2)
            cdl_expiry = st.date_input("CDL Expiry Date")
            medical_cert_expiry = st.date_input("Medical Cert Expiry")
            home_terminal = st.text_input("Home Terminal")
        
        if st.form_submit_button("👨‍🚚 Add Driver", type="primary"):
            if driver_code and first_name and last_name:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""INSERT INTO drivers 
                        (driver_code, first_name, last_name, cdl_number, cdl_state,
                         cdl_expiry, medical_cert_expiry, phone, email, home_terminal)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (driver_code, first_name, last_name, cdl_number, cdl_state,
                         cdl_expiry, medical_cert_expiry, phone, email, home_terminal))
                    conn.commit()
                    show_success_message(f"Driver {first_name} {last_name} added successfully!")
                    st.rerun()
                except Exception as e:
                    show_error_message(f"Error adding driver: {str(e)}")
            else:
                show_error_message("Driver Code, First Name, and Last Name are required")
    
    conn.close()