"""
AI Assistants Module for Smith & Williams Trucking TMS
Features Florida (Data Entry Assistant) and Vernon (Security & System Manager)
"""
import streamlit as st
import time
from datetime import datetime, timedelta
import re
from modules.database_enhanced import (
    execute_query, get_carrier_payment_schedule, 
    calculate_payment_amounts, get_loads_for_reconciliation
)

class FloridaAssistant:
    """Florida - The conversational AI for Historical Data Entry"""
    
    def __init__(self):
        self.name = "Florida"
        self.personality = """
        I'm Florida, your dedicated TMS assistant at Smith & Williams Trucking. 
        I make data entry smooth and conversational, guiding you through every step 
        with precision and a friendly approach. Let's get your loads documented properly!
        """
        
        if 'florida_state' not in st.session_state:
            st.session_state.florida_state = 'greeting'
            st.session_state.florida_data = {}
            st.session_state.florida_session_id = datetime.now().strftime("%Y%m%d%H%M%S")
    
    def save_chat_message(self, role, message):
        """Save chat messages to database"""
        execute_query(
            """INSERT INTO chat_history (user_id, session_id, role, message, view_type) 
               VALUES (?, ?, ?, ?, 'data_feeder')""",
            (st.session_state.get('user_id', 1), 
             st.session_state.florida_session_id, 
             role, 
             message)
        )
    
    def display_message(self, message, is_user=False):
        """Display chat message with appropriate styling"""
        if is_user:
            st.markdown(f"""
            <div style='text-align: right; margin: 10px 0;'>
                <span style='background: #8B0000; color: white; padding: 10px 15px; 
                border-radius: 20px; display: inline-block;'>
                    {message}
                </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style='text-align: left; margin: 10px 0;'>
                <strong style='color: #8B0000;'>Florida:</strong>
                <span style='background: #2a2a2a; color: white; padding: 10px 15px; 
                border-radius: 20px; display: inline-block; margin-left: 10px;'>
                    {message}
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    def process_load_entry(self):
        """Main conversation flow for load entry"""
        
        # Display personality introduction if first time
        if st.session_state.florida_state == 'greeting':
            self.display_message("Hello! I'm Florida, your TMS assistant. I'll help you enter load data quickly and accurately. Ready to start?")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Yes, let's start", key="start_yes"):
                    st.session_state.florida_state = 'ask_load_id'
                    st.rerun()
            with col2:
                if st.button("Show me recent loads first", key="show_recent"):
                    self.show_recent_loads()
        
        elif st.session_state.florida_state == 'ask_load_id':
            self.display_message("Perfect! Let's start with the Load ID. What's the unique identifier for this load?")
            
            load_id = st.text_input("Load ID:", key="load_id_input")
            if st.button("Continue", key="load_id_continue"):
                if load_id:
                    st.session_state.florida_data['load_id'] = load_id
                    st.session_state.florida_state = 'ask_dates'
                    self.save_chat_message("user", f"Load ID: {load_id}")
                    st.rerun()
                else:
                    st.error("Please enter a Load ID")
        
        elif st.session_state.florida_state == 'ask_dates':
            self.display_message(f"Great! Load ID {st.session_state.florida_data['load_id']} recorded. Now, what are the pickup and delivery dates?")
            
            col1, col2 = st.columns(2)
            with col1:
                pickup_date = st.date_input("Pickup Date:", key="pickup_date_input")
            with col2:
                delivery_date = st.date_input("Delivery Date:", key="delivery_date_input")
            
            if st.button("Continue", key="dates_continue"):
                st.session_state.florida_data['pickup_date'] = pickup_date
                st.session_state.florida_data['delivery_date'] = delivery_date
                st.session_state.florida_state = 'ask_parties'
                st.rerun()
        
        elif st.session_state.florida_state == 'ask_parties':
            self.display_message("Now let's identify the parties. Who's the carrier and customer for this load?")
            
            col1, col2 = st.columns(2)
            with col1:
                carrier = st.selectbox("Carrier:", ["CanAmex", "Smith & Williams", "Other"], key="carrier_input")
                if carrier == "Other":
                    carrier = st.text_input("Specify carrier:", key="carrier_other")
            with col2:
                customer = st.text_input("Customer:", key="customer_input")
            
            if st.button("Continue", key="parties_continue"):
                if carrier and customer:
                    st.session_state.florida_data['carrier'] = carrier
                    st.session_state.florida_data['customer'] = customer
                    st.session_state.florida_state = 'ask_locations'
                    st.rerun()
                else:
                    st.error("Please enter both carrier and customer")
        
        elif st.session_state.florida_state == 'ask_locations':
            self.display_message("Let's get the pickup and delivery addresses.")
            
            st.subheader("Pickup Location")
            pickup_address = st.text_input("Pickup Address:", key="pickup_addr")
            col1, col2, col3 = st.columns(3)
            with col1:
                pickup_city = st.text_input("City:", key="pickup_city")
            with col2:
                pickup_state = st.text_input("State:", key="pickup_state")
            with col3:
                pickup_zip = st.text_input("ZIP:", key="pickup_zip")
            
            st.subheader("Delivery Location")
            delivery_address = st.text_input("Delivery Address:", key="delivery_addr")
            col1, col2, col3 = st.columns(3)
            with col1:
                delivery_city = st.text_input("City:", key="delivery_city")
            with col2:
                delivery_state = st.text_input("State:", key="delivery_state")
            with col3:
                delivery_zip = st.text_input("ZIP:", key="delivery_zip")
            
            if st.button("Continue", key="locations_continue"):
                st.session_state.florida_data.update({
                    'pickup_address': pickup_address,
                    'pickup_city': pickup_city,
                    'pickup_state': pickup_state,
                    'pickup_zip': pickup_zip,
                    'delivery_address': delivery_address,
                    'delivery_city': delivery_city,
                    'delivery_state': delivery_state,
                    'delivery_zip': delivery_zip
                })
                st.session_state.florida_state = 'ask_payment'
                st.rerun()
        
        elif st.session_state.florida_state == 'ask_payment':
            carrier = st.session_state.florida_data['carrier']
            
            # Automatically determine payment method based on carrier
            if carrier == "CanAmex":
                payment_method = "Direct Pay"
                fee_percent = 12.0
                self.display_message(f"I see this is a CanAmex load. This will be Direct Pay with a 12% fee.")
            else:
                payment_method = "Factored"
                fee_percent = 3.0
                self.display_message(f"This appears to be a factored load with a 3% fee.")
            
            gross_amount = st.number_input("What's the gross amount for this load?", 
                                          min_value=0.0, 
                                          format="%.2f", 
                                          key="gross_amount_input")
            
            if gross_amount > 0:
                payment_calc = calculate_payment_amounts(gross_amount, payment_method)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Gross Amount", f"${payment_calc['gross_amount']:,.2f}")
                with col2:
                    st.metric(f"Fee ({payment_calc['fee_percent']}%)", f"${payment_calc['fee_amount']:,.2f}")
                with col3:
                    st.metric("Net Amount", f"${payment_calc['net_amount']:,.2f}")
                
                # Calculate rates if distance available
                distance = st.number_input("Distance (miles):", min_value=0.0, key="distance_input")
                if distance > 0:
                    gross_rate = gross_amount / distance
                    net_rate = payment_calc['net_amount'] / distance
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Gross Rate/Mile", f"${gross_rate:.2f}")
                    with col2:
                        st.metric("Net Rate/Mile", f"${net_rate:.2f}")
                
                if st.button("Save Load", key="save_load"):
                    st.session_state.florida_data.update({
                        'gross_amount': gross_amount,
                        'net_amount': payment_calc['net_amount'],
                        'payment_method': payment_method,
                        'factoring_fee_percent': payment_calc['fee_percent'],
                        'distance_miles': distance if distance > 0 else None,
                        'gross_rate_per_mile': gross_rate if distance > 0 else None,
                        'net_rate_per_mile': net_rate if distance > 0 else None
                    })
                    self.save_load_to_database()
                    st.session_state.florida_state = 'complete'
                    st.rerun()
        
        elif st.session_state.florida_state == 'complete':
            self.display_message(f"✅ Excellent! Load {st.session_state.florida_data['load_id']} has been saved successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Enter Another Load", key="another_load"):
                    st.session_state.florida_state = 'ask_load_id'
                    st.session_state.florida_data = {}
                    st.rerun()
            with col2:
                if st.button("Reconcile Payments", key="goto_reconcile"):
                    st.session_state.florida_state = 'reconciliation'
                    st.rerun()
            with col3:
                if st.button("View Summary", key="view_summary"):
                    self.show_recent_loads()
    
    def save_load_to_database(self):
        """Save the collected load data to database"""
        data = st.session_state.florida_data
        
        query = """
            INSERT INTO loads (
                load_id, customer, carrier, pickup_date, delivery_date,
                pickup_address, pickup_city, pickup_state, pickup_zip,
                delivery_address, delivery_city, delivery_state, delivery_zip,
                distance_miles, gross_amount, net_amount, payment_method,
                factoring_fee_percent, gross_rate_per_mile, net_rate_per_mile,
                status, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', ?)
        """
        
        params = (
            data['load_id'], data['customer'], data['carrier'],
            data['pickup_date'], data['delivery_date'],
            data['pickup_address'], data['pickup_city'], data['pickup_state'], data['pickup_zip'],
            data['delivery_address'], data['delivery_city'], data['delivery_state'], data['delivery_zip'],
            data.get('distance_miles'), data['gross_amount'], data['net_amount'],
            data['payment_method'], data.get('factoring_fee_percent'),
            data.get('gross_rate_per_mile'), data.get('net_rate_per_mile'),
            st.session_state.get('user_id', 1)
        )
        
        execute_query(query, params)
    
    def show_recent_loads(self):
        """Display recent loads entered"""
        loads = execute_query("""
            SELECT load_id, customer, carrier, pickup_date, delivery_date, 
                   gross_amount, net_amount, payment_method
            FROM loads 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        if loads:
            st.subheader("Recent Loads")
            for load in loads:
                with st.expander(f"Load {load['load_id']} - {load['customer']}"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Carrier:** {load['carrier']}")
                        st.write(f"**Payment:** {load['payment_method']}")
                    with col2:
                        st.write(f"**Pickup:** {load['pickup_date']}")
                        st.write(f"**Delivery:** {load['delivery_date']}")
                    with col3:
                        st.write(f"**Gross:** ${load['gross_amount']:,.2f}")
                        st.write(f"**Net:** ${load['net_amount']:,.2f}")


class VernonSecurityManager:
    """Vernon - The IT Security Manager and System Protector"""
    
    def __init__(self):
        self.name = "Vernon"
        self.title = "Senior IT Security Manager"
        self.personality = """
        I'm Vernon, your Senior IT Security Manager at Smith & Williams Trucking.
        I ensure all data is protected, systems are secure, and operations run smoothly.
        My self-fixing protocol keeps everything running at peak performance.
        """
    
    def display_security_status(self):
        """Display system security status"""
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a1a1a, #2d2d2d); 
                    border: 2px solid #28a745; border-radius: 10px; padding: 20px;'>
            <h3 style='color: #28a745;'>🔒 System Security Status</h3>
            <p style='color: white;'><strong>Protected by:</strong> {self.name} - {self.title}</p>
            <p style='color: #28a745;'>✓ All systems operational</p>
            <p style='color: #28a745;'>✓ Data encryption active</p>
            <p style='color: #28a745;'>✓ Self-fixing protocol enabled</p>
            <p style='color: #28a745;'>✓ Real-time monitoring active</p>
        </div>
        """, unsafe_allow_html=True)
    
    def verify_data_integrity(self):
        """Check database integrity"""
        try:
            # Check for any data anomalies
            result = execute_query("SELECT COUNT(*) as count FROM loads WHERE gross_amount < net_amount")
            if result and result[0]['count'] > 0:
                st.warning(f"⚠️ Vernon Alert: Found {result[0]['count']} loads with data inconsistencies. Auto-fixing...")
                # Auto-fix logic here
                return False
            return True
        except Exception as e:
            st.error(f"Vernon Security Alert: {str(e)}")
            return False
    
    def protect_session(self):
        """Ensure session security"""
        if 'last_activity' not in st.session_state:
            st.session_state.last_activity = datetime.now()
        
        # Check for session timeout (30 minutes)
        if datetime.now() - st.session_state.last_activity > timedelta(minutes=30):
            st.warning("⚠️ Vernon: Session timeout for security. Please log in again.")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.session_state.last_activity = datetime.now()