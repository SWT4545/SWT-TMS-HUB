"""
Intelligent AI Assistant for Complete TMS and Personal Management
This assistant understands and manages ALL aspects of business and personal life
"""
import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
from config.database import get_connection
import json
import re

def show_ai_assistant_view():
    """Display AI Assistant interface - NEEDS IMPLEMENTATION"""
    st.markdown("## 🤖 AI Assistant")
    st.info("This view needs to be implemented with conversational AI interface.")
    st.markdown("### Features to implement:")
    st.markdown("- Chat interface with AI")
    st.markdown("- TMS-specific responses")
    st.markdown("- Load planning assistance")
    st.markdown("- Route optimization")
    return

class IntelligentAssistant:
    """AI Assistant that understands everything about the business and personal life"""
    
    def __init__(self):
        self.conn = get_connection()
        self.context = self.load_context()
        
    def load_context(self):
        """Load all system context for intelligent responses"""
        context = {
            'business': {
                'shipments': self.get_shipment_status(),
                'fleet': self.get_fleet_status(),
                'drivers': self.get_driver_status(),
                'expenses': self.get_expense_summary(),
                'revenue': self.get_revenue_summary(),
                'customers': self.get_customer_summary()
            },
            'personal': {
                'finance': self.get_personal_finance_summary(),
                'properties': self.get_property_summary(),
                'vehicles': self.get_vehicle_summary(),
                'credit': self.get_credit_summary(),
                'goals': self.get_goals_summary()
            }
        }
        return context
    
    def get_shipment_status(self):
        """Get current shipment status"""
        try:
            df = pd.read_sql_query("""
                SELECT status, COUNT(*) as count 
                FROM shipments 
                GROUP BY status
            """, self.conn)
            return df.to_dict('records')
        except:
            return []
    
    def get_fleet_status(self):
        """Get fleet status"""
        try:
            trucks = pd.read_sql_query("SELECT COUNT(*) as total, SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available FROM trucks", self.conn)
            return trucks.to_dict('records')[0]
        except:
            return {'total': 0, 'available': 0}
    
    def get_driver_status(self):
        """Get driver status"""
        try:
            drivers = pd.read_sql_query("SELECT COUNT(*) as total, SUM(CASE WHEN status = 'Available' THEN 1 ELSE 0 END) as available FROM drivers", self.conn)
            return drivers.to_dict('records')[0]
        except:
            return {'total': 0, 'available': 0}
    
    def get_expense_summary(self):
        """Get expense summary"""
        try:
            expenses = pd.read_sql_query("""
                SELECT SUM(amount) as total 
                FROM expenses 
                WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
            """, self.conn)
            return expenses['total'].iloc[0] or 0
        except:
            return 0
    
    def get_revenue_summary(self):
        """Get revenue summary"""
        try:
            revenue = pd.read_sql_query("""
                SELECT SUM(rate) as total 
                FROM shipments 
                WHERE strftime('%Y-%m', pickup_date) = strftime('%Y-%m', 'now')
            """, self.conn)
            return revenue['total'].iloc[0] or 0
        except:
            return 0
    
    def get_customer_summary(self):
        """Get customer summary"""
        try:
            customers = pd.read_sql_query("SELECT COUNT(*) as total FROM customers WHERE is_active = 1", self.conn)
            return customers['total'].iloc[0]
        except:
            return 0
    
    def get_personal_finance_summary(self):
        """Get personal finance summary"""
        try:
            expenses = pd.read_sql_query("""
                SELECT SUM(amount) as total 
                FROM personal_expenses 
                WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
            """, self.conn)
            
            income = pd.read_sql_query("""
                SELECT SUM(amount) as total 
                FROM personal_income 
                WHERE strftime('%Y-%m', income_date) = strftime('%Y-%m', 'now')
            """, self.conn)
            
            return {
                'monthly_expenses': expenses['total'].iloc[0] or 0,
                'monthly_income': income['total'].iloc[0] or 0
            }
        except:
            return {'monthly_expenses': 0, 'monthly_income': 0}
    
    def get_property_summary(self):
        """Get property summary"""
        try:
            properties = pd.read_sql_query("""
                SELECT COUNT(*) as count, 
                       SUM(current_value) as total_value,
                       SUM(current_value - mortgage_balance) as total_equity
                FROM properties
            """, self.conn)
            return properties.to_dict('records')[0]
        except:
            return {'count': 0, 'total_value': 0, 'total_equity': 0}
    
    def get_vehicle_summary(self):
        """Get vehicle summary"""
        try:
            vehicles = pd.read_sql_query("""
                SELECT COUNT(*) as count,
                       SUM(current_value) as total_value
                FROM personal_vehicles
            """, self.conn)
            return vehicles.to_dict('records')[0]
        except:
            return {'count': 0, 'total_value': 0}
    
    def get_credit_summary(self):
        """Get credit card summary"""
        try:
            credit = pd.read_sql_query("""
                SELECT COUNT(*) as count,
                       SUM(current_balance) as total_balance,
                       SUM(credit_limit) as total_limit
                FROM credit_cards
            """, self.conn)
            return credit.to_dict('records')[0]
        except:
            return {'count': 0, 'total_balance': 0, 'total_limit': 0}
    
    def get_goals_summary(self):
        """Get goals summary"""
        try:
            goals = pd.read_sql_query("""
                SELECT COUNT(*) as total,
                       SUM(CASE WHEN status = 'Active' THEN 1 ELSE 0 END) as active
                FROM personal_goals
            """, self.conn)
            return goals.to_dict('records')[0]
        except:
            return {'total': 0, 'active': 0}
    
    def process_command(self, command, auto_execute=False):
        """Process natural language commands with full intelligence"""
        command_lower = command.lower()
        cursor = self.conn.cursor()
        
        # Check for confirmation of pending action
        if 'confirm' in command_lower and 'pending_action' in st.session_state:
            return self.execute_pending_action()
        
        # Check for cancellation
        if 'cancel' in command_lower and 'pending_action' in st.session_state:
            st.session_state.pop('pending_action', None)
            return "❌ Action cancelled. What else can I help you with?"
        
        # Check for override mode
        if 'override' in command_lower or 'manual' in command_lower:
            return self.show_manual_override_options()
        
        # BUSINESS COMMANDS
        
        # Load/Shipment Management
        if any(word in command_lower for word in ['load', 'shipment', 'pickup', 'delivery']):
            return self.handle_shipment_command(command)
        
        # Fleet Management
        elif any(word in command_lower for word in ['truck', 'trailer', 'fleet', 'equipment']):
            return self.handle_fleet_command(command)
        
        # Driver Management
        elif any(word in command_lower for word in ['driver', 'cdl', 'medical cert']):
            return self.handle_driver_command(command)
        
        # Business Expense Management
        elif 'business expense' in command_lower or 'company expense' in command_lower:
            return self.handle_business_expense_command(command)
        
        # Customer Management
        elif any(word in command_lower for word in ['customer', 'client', 'shipper']):
            return self.handle_customer_command(command)
        
        # PERSONAL COMMANDS
        
        # Personal Expense Management
        elif 'personal expense' in command_lower or 'spent' in command_lower or 'bought' in command_lower:
            return self.handle_personal_expense_command(command)
        
        # Property Management
        elif any(word in command_lower for word in ['property', 'house', 'real estate', 'rental']):
            return self.handle_property_command(command)
        
        # Personal Vehicle Management
        elif 'personal' in command_lower and any(word in command_lower for word in ['car', 'vehicle', 'auto']):
            return self.handle_personal_vehicle_command(command)
        
        # Credit Card Management
        elif any(word in command_lower for word in ['credit card', 'cc', 'visa', 'mastercard', 'amex']):
            return self.handle_credit_card_command(command)
        
        # Bank Account Management
        elif any(word in command_lower for word in ['bank', 'checking', 'savings', 'account balance']):
            return self.handle_bank_account_command(command)
        
        # Goals Management
        elif any(word in command_lower for word in ['goal', 'target', 'objective', 'plan']):
            return self.handle_goal_command(command)
        
        # REPORTING & ANALYTICS
        
        # Financial Reports
        elif any(word in command_lower for word in ['report', 'summary', 'status', 'how much', 'total']):
            return self.handle_report_command(command)
        
        # Net Worth
        elif 'net worth' in command_lower or 'worth' in command_lower:
            return self.calculate_net_worth()
        
        # Profit/Loss
        elif any(word in command_lower for word in ['profit', 'loss', 'p&l', 'revenue']):
            return self.calculate_profit_loss()
        
        else:
            return self.provide_intelligent_response(command)
    
    def execute_pending_action(self):
        """Execute a pending action after confirmation"""
        action = st.session_state.get('pending_action')
        if not action:
            return "No pending action to confirm"
        
        action_type = action.get('type')
        data = action.get('data')
        
        try:
            cursor = self.conn.cursor()
            
            if action_type == 'create_shipment':
                cursor.execute("""
                    INSERT INTO shipments (load_number, origin_city, destination_city, 
                                         pickup_date, rate, weight, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'New')
                """, (data['load_number'], data['origin'], data['destination'],
                      data['date'], data['rate'], data['weight']))
                self.conn.commit()
                st.session_state.pop('pending_action', None)
                return f"✅ Created shipment {data['load_number']}"
            
            # Add more action types as needed
            else:
                return "Unknown action type"
                
        except Exception as e:
            st.session_state.pop('pending_action', None)
            return f"❌ Error executing action: {str(e)}"
    
    def show_manual_override_options(self):
        """Show manual override options"""
        return """🔧 MANUAL OVERRIDE MODE
━━━━━━━━━━━━━━━━━━━━━━

To manually access any system:
• Type 'management' - Open Management Center
• Type 'personal' - Open Personal Management
• Type 'users' - Manage Users
• Type 'fleet' - Manage Fleet
• Type 'expenses' - Manage Expenses
• Type 'properties' - Manage Properties

Or use the sidebar navigation for direct access to all modules.

You can always override any AI action by going directly to the Management Center."""
    
    def handle_shipment_command(self, command):
        """Handle shipment-related commands"""
        command_lower = command.lower()
        
        # Extract shipment details using patterns
        patterns = {
            'load_number': r'load\s*#?\s*(\w+)',
            'customer': r'for\s+(\w+(?:\s+\w+)*?)(?:\s+from|\s+to|\s+pickup|$)',
            'origin': r'from\s+([^,]+?)(?:\s+to|$)',
            'destination': r'to\s+([^,]+?)(?:\s+on|$)',
            'date': r'on\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'rate': r'\$?([\d,]+(?:\.\d{2})?)\s*(?:rate|$)',
            'weight': r'(\d+(?:,\d{3})*)\s*(?:lbs?|pounds?)',
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                extracted[key] = match.group(1).strip()
        
        if 'add' in command_lower or 'create' in command_lower or 'new' in command_lower:
            # Add new shipment with confirmation
            load_number = extracted.get('load_number', f"LOAD{datetime.now().strftime('%Y%m%d%H%M')}")
            
            # Show what will be created for confirmation
            confirmation = f"""📋 READY TO CREATE SHIPMENT:
━━━━━━━━━━━━━━━━━━━━━━
Load #: {load_number}
From: {extracted.get('origin', 'Not specified')}
To: {extracted.get('destination', 'Not specified')}
Date: {extracted.get('date', date.today())}
Rate: ${float(extracted.get('rate', 0)):,.2f}
Weight: {extracted.get('weight', 'Not specified')} lbs

✅ Type 'confirm' to create
❌ Type 'cancel' to abort
✏️ Or go to Management Center to edit manually"""
            
            # Store pending action in session state for confirmation
            st.session_state['pending_action'] = {
                'type': 'create_shipment',
                'data': {
                    'load_number': load_number,
                    'origin': extracted.get('origin', ''),
                    'destination': extracted.get('destination', ''),
                    'date': extracted.get('date', date.today()),
                    'rate': float(extracted.get('rate', 0)),
                    'weight': float(extracted.get('weight', 0))
                }
            }
            
            return confirmation
        
        elif 'status' in command_lower or 'where' in command_lower:
            # Check shipment status
            load_number = extracted.get('load_number')
            if load_number:
                df = pd.read_sql_query("""
                    SELECT load_number, status, origin_city, destination_city, pickup_date
                    FROM shipments
                    WHERE load_number LIKE ?
                """, self.conn, params=[f"%{load_number}%"])
                
                if not df.empty:
                    shipment = df.iloc[0]
                    return f"Load {shipment['load_number']} is {shipment['status']}. Route: {shipment['origin_city']} to {shipment['destination_city']}"
                else:
                    return f"Load {load_number} not found"
            else:
                # Show all active shipments
                df = pd.read_sql_query("""
                    SELECT load_number, status, origin_city, destination_city
                    FROM shipments
                    WHERE status NOT IN ('Delivered', 'Cancelled')
                    ORDER BY pickup_date DESC
                    LIMIT 5
                """, self.conn)
                
                if not df.empty:
                    response = "Active shipments:\n"
                    for _, row in df.iterrows():
                        response += f"• {row['load_number']}: {row['status']} ({row['origin_city']} → {row['destination_city']})\n"
                    return response
                else:
                    return "No active shipments"
        
        return "Please provide more details about the shipment"
    
    def handle_personal_expense_command(self, command):
        """Handle personal expense commands"""
        command_lower = command.lower()
        
        # Extract expense details
        patterns = {
            'amount': r'\$?([\d,]+(?:\.\d{2})?)',
            'vendor': r'(?:at|from)\s+([^,]+?)(?:\s+for|\s+on|$)',
            'category': r'for\s+([^,]+?)(?:\s+on|$)',
            'date': r'on\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        }
        
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                extracted[key] = match.group(1).strip()
        
        # Detect category from keywords
        category_keywords = {
            'Food & Dining': ['food', 'dinner', 'lunch', 'breakfast', 'restaurant', 'coffee'],
            'Shopping': ['shopping', 'clothes', 'amazon', 'store'],
            'Entertainment': ['movie', 'concert', 'game', 'entertainment'],
            'Auto & Transport': ['gas', 'fuel', 'uber', 'lyft', 'parking'],
            'Home': ['home', 'furniture', 'repair', 'maintenance'],
            'Health & Fitness': ['gym', 'doctor', 'pharmacy', 'medical'],
            'Travel': ['flight', 'hotel', 'vacation', 'trip']
        }
        
        detected_category = 'Other'
        for cat, keywords in category_keywords.items():
            if any(kw in command_lower for kw in keywords):
                detected_category = cat
                break
        
        if 'spent' in command_lower or 'bought' in command_lower or 'paid' in command_lower:
            # Add personal expense
            try:
                amount = float(extracted.get('amount', '0').replace(',', ''))
                if amount > 0:
                    cursor = self.conn.cursor()
                    cursor.execute("""
                        INSERT INTO personal_expenses 
                        (expense_date, category, vendor, amount, description)
                        VALUES (?, ?, ?, ?, ?)
                    """, (date.today(), 
                          detected_category,
                          extracted.get('vendor', ''),
                          amount,
                          command))
                    self.conn.commit()
                    return f"✅ Recorded personal expense: ${amount:.2f} for {detected_category}"
                else:
                    return "Please specify the amount spent"
            except Exception as e:
                return f"❌ Error recording expense: {str(e)}"
        
        elif 'how much' in command_lower and 'spent' in command_lower:
            # Check spending
            period = 'month' if 'month' in command_lower else 'week' if 'week' in command_lower else 'today'
            
            if period == 'month':
                query = """
                    SELECT SUM(amount) as total, category
                    FROM personal_expenses
                    WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
                    GROUP BY category
                """
            elif period == 'week':
                query = """
                    SELECT SUM(amount) as total, category
                    FROM personal_expenses
                    WHERE expense_date >= date('now', '-7 days')
                    GROUP BY category
                """
            else:
                query = """
                    SELECT SUM(amount) as total, category
                    FROM personal_expenses
                    WHERE expense_date = date('now')
                    GROUP BY category
                """
            
            df = pd.read_sql_query(query, self.conn)
            
            if not df.empty:
                total = df['total'].sum()
                response = f"Total spent this {period}: ${total:,.2f}\n\nBy category:\n"
                for _, row in df.iterrows():
                    response += f"• {row['category']}: ${row['total']:,.2f}\n"
                return response
            else:
                return f"No expenses recorded this {period}"
        
        return "Please provide expense details (amount, what for, where)"
    
    def handle_fleet_command(self, command):
        """Handle fleet-related commands"""
        command_lower = command.lower()
        
        if 'available' in command_lower:
            df = pd.read_sql_query("""
                SELECT truck_number, current_location 
                FROM trucks 
                WHERE status = 'Available'
            """, self.conn)
            
            if not df.empty:
                response = f"Available trucks ({len(df)}):\n"
                for _, row in df.iterrows():
                    response += f"• {row['truck_number']} at {row['current_location'] or 'Unknown'}\n"
                return response
            else:
                return "No trucks currently available"
        
        elif 'add truck' in command_lower:
            # Extract truck details
            match = re.search(r'truck\s*#?\s*(\w+)', command, re.IGNORECASE)
            truck_number = match.group(1) if match else f"TRUCK{datetime.now().strftime('%H%M')}"
            
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO trucks (truck_number, status)
                    VALUES (?, 'Available')
                """, (truck_number,))
                self.conn.commit()
                return f"✅ Added truck {truck_number} to fleet"
            except:
                return "❌ Error adding truck"
        
        return self.context['business']['fleet']
    
    def handle_property_command(self, command):
        """Handle property-related commands"""
        command_lower = command.lower()
        
        if 'add property' in command_lower or 'bought' in command_lower and 'property' in command_lower:
            # Extract property details
            patterns = {
                'price': r'\$?([\d,]+(?:\.\d{2})?)',
                'address': r'at\s+([^,]+?)(?:\s+for|$)',
            }
            
            extracted = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, command, re.IGNORECASE)
                if match:
                    extracted[key] = match.group(1).strip()
            
            try:
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO properties (property_name, purchase_price, current_value, purchase_date)
                    VALUES (?, ?, ?, ?)
                """, (extracted.get('address', 'New Property'),
                      float(extracted.get('price', '0').replace(',', '')),
                      float(extracted.get('price', '0').replace(',', '')),
                      date.today()))
                self.conn.commit()
                return f"✅ Added property to portfolio"
            except Exception as e:
                return f"❌ Error adding property: {str(e)}"
        
        elif 'properties' in command_lower or 'real estate' in command_lower:
            summary = self.get_property_summary()
            return f"""Property Portfolio:
• Properties: {summary['count']}
• Total Value: ${summary['total_value']:,.2f}
• Total Equity: ${summary['total_equity']:,.2f}"""
        
        return "Please provide property details"
    
    def calculate_net_worth(self):
        """Calculate total net worth"""
        try:
            # Assets
            properties = pd.read_sql_query("SELECT SUM(current_value - mortgage_balance) as equity FROM properties", self.conn)
            vehicles = pd.read_sql_query("SELECT SUM(current_value - loan_balance) as equity FROM personal_vehicles", self.conn)
            bank = pd.read_sql_query("SELECT SUM(current_balance) as total FROM bank_accounts", self.conn)
            investments = pd.read_sql_query("SELECT SUM(quantity * current_price) as total FROM investments", self.conn)
            
            # Liabilities
            credit_cards = pd.read_sql_query("SELECT SUM(current_balance) as debt FROM credit_cards", self.conn)
            
            assets = (properties['equity'].iloc[0] or 0) + \
                    (vehicles['equity'].iloc[0] or 0) + \
                    (bank['total'].iloc[0] or 0) + \
                    (investments['total'].iloc[0] or 0)
            
            liabilities = credit_cards['debt'].iloc[0] or 0
            
            net_worth = assets - liabilities
            
            return f"""💰 NET WORTH SUMMARY
━━━━━━━━━━━━━━━━━━━━
ASSETS:
• Real Estate Equity: ${properties['equity'].iloc[0] or 0:,.2f}
• Vehicle Equity: ${vehicles['equity'].iloc[0] or 0:,.2f}
• Bank Accounts: ${bank['total'].iloc[0] or 0:,.2f}
• Investments: ${investments['total'].iloc[0] or 0:,.2f}
Total Assets: ${assets:,.2f}

LIABILITIES:
• Credit Card Debt: ${liabilities:,.2f}

NET WORTH: ${net_worth:,.2f}"""
        except Exception as e:
            return f"Error calculating net worth: {str(e)}"
    
    def calculate_profit_loss(self):
        """Calculate business profit/loss"""
        try:
            # Revenue
            revenue = pd.read_sql_query("""
                SELECT SUM(rate) as total 
                FROM shipments 
                WHERE strftime('%Y-%m', pickup_date) = strftime('%Y-%m', 'now')
                AND status NOT IN ('Cancelled')
            """, self.conn)
            
            # Expenses
            expenses = pd.read_sql_query("""
                SELECT SUM(amount) as total 
                FROM expenses 
                WHERE strftime('%Y-%m', expense_date) = strftime('%Y-%m', 'now')
            """, self.conn)
            
            total_revenue = revenue['total'].iloc[0] or 0
            total_expenses = expenses['total'].iloc[0] or 0
            profit = total_revenue - total_expenses
            margin = (profit / total_revenue * 100) if total_revenue > 0 else 0
            
            return f"""📊 MONTHLY P&L (BUSINESS)
━━━━━━━━━━━━━━━━━━━━
Revenue: ${total_revenue:,.2f}
Expenses: ${total_expenses:,.2f}
━━━━━━━━━━━━━━━━━━━━
Net Profit: ${profit:,.2f}
Margin: {margin:.1f}%"""
        except Exception as e:
            return f"Error calculating P&L: {str(e)}"
    
    def handle_report_command(self, command):
        """Generate various reports"""
        command_lower = command.lower()
        
        if 'daily' in command_lower:
            return self.generate_daily_report()
        elif 'weekly' in command_lower:
            return self.generate_weekly_report()
        elif 'monthly' in command_lower:
            return self.generate_monthly_report()
        else:
            return self.generate_summary_report()
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        return f"""📊 COMPREHENSIVE SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━

🚛 BUSINESS OPERATIONS:
• Active Shipments: {len([s for s in self.context['business']['shipments'] if s.get('status') not in ['Delivered', 'Cancelled']])}
• Available Trucks: {self.context['business']['fleet']['available']}/{self.context['business']['fleet']['total']}
• Available Drivers: {self.context['business']['drivers']['available']}/{self.context['business']['drivers']['total']}
• Active Customers: {self.context['business']['customers']}

💰 FINANCIAL (This Month):
• Business Revenue: ${self.context['business']['revenue']:,.2f}
• Business Expenses: ${self.context['business']['expenses']:,.2f}
• Personal Income: ${self.context['personal']['finance']['monthly_income']:,.2f}
• Personal Expenses: ${self.context['personal']['finance']['monthly_expenses']:,.2f}

🏠 PERSONAL ASSETS:
• Properties: {self.context['personal']['properties']['count']}
• Property Value: ${self.context['personal']['properties']['total_value']:,.2f}
• Vehicles: {self.context['personal']['vehicles']['count']}
• Credit Cards: {self.context['personal']['credit']['count']}
• CC Debt: ${self.context['personal']['credit']['total_balance']:,.2f}

🎯 GOALS:
• Active Goals: {self.context['personal']['goals']['active']}
• Total Goals: {self.context['personal']['goals']['total']}"""
    
    def provide_intelligent_response(self, command):
        """Provide intelligent contextual responses"""
        command_lower = command.lower()
        
        # Greetings
        if any(word in command_lower for word in ['hello', 'hi', 'hey']):
            return f"""Hello Brandon! Here's your quick overview:
            
Business: {self.context['business']['fleet']['available']} trucks available, {len([s for s in self.context['business']['shipments'] if s.get('status') == 'In Transit'])} loads in transit
Personal: Monthly net: ${self.context['personal']['finance']['monthly_income'] - self.context['personal']['finance']['monthly_expenses']:,.2f}

What would you like to manage today?"""
        
        # Help
        elif 'help' in command_lower:
            return """I can help you manage everything! Try:

BUSINESS:
• "Add new load from LA to Phoenix for $3500"
• "Show available trucks"
• "Add business expense $500 for fuel"
• "Show this month's revenue"

PERSONAL:
• "I spent $200 at Costco"
• "Add property at 123 Main St for $500,000"
• "What's my net worth?"
• "Show my credit card debt"

REPORTS:
• "Generate daily report"
• "Show profit and loss"
• "Summary of everything"

What would you like to do?"""
        
        else:
            return "I can help you manage your business and personal life. Try asking about shipments, expenses, properties, or say 'help' for more options."


def show_intelligent_assistant():
    """Show the intelligent assistant interface"""
    st.title("🤖 Intelligent TMS & Life Assistant")
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = IntelligentAssistant()
    
    assistant = st.session_state.assistant
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Business Revenue", f"${assistant.context['business']['revenue']:,.0f}")
    with col2:
        st.metric("Available Trucks", f"{assistant.context['business']['fleet']['available']}")
    with col3:
        st.metric("Personal Net", f"${assistant.context['personal']['finance']['monthly_income'] - assistant.context['personal']['finance']['monthly_expenses']:,.0f}")
    with col4:
        st.metric("Active Goals", f"{assistant.context['personal']['goals']['active']}")
    
    # Chat interface
    st.markdown("---")
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello Brandon! I'm your intelligent assistant. I can manage everything - business operations, personal expenses, properties, goals, and more. What would you like to do today?"}
        ]
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Tell me what you need..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        response = assistant.process_command(prompt)
        
        # Add assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
        
        # Refresh context after each command
        assistant.context = assistant.load_context()
    
    # Quick action buttons
    st.markdown("---")
    st.subheader("Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Daily Report"):
            response = assistant.generate_summary_report()
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("💰 Net Worth"):
            response = assistant.calculate_net_worth()
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📈 P&L Report"):
            response = assistant.calculate_profit_loss()
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("🔄 Refresh"):
            assistant.context = assistant.load_context()
            st.success("Context refreshed!")
            st.rerun()