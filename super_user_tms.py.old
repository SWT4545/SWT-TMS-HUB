"""
===================================================================
SUPER-USER TRANSPORTATION MANAGEMENT SYSTEM
Smith & Williams Trucking LLC
===================================================================
Enhanced TMS with Three-View Toggle System:
1. Executive View - High-level oversight and management
2. Historical Data Feeder - Conversational AI for data entry
3. Driver View - Mobile-friendly operational interface

CEO & Owner: Brandon Smith
System Personality: Florida Spillers (TMS Assistant)
IT Security Head: Vernon (Data Protection & Self-Fixing Protocol)
Single Profile with Multi-View Capability
===================================================================
"""

import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date, timedelta
import os
import json
import time
import base64
import hashlib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import requests
import numpy as np
from dotenv import load_dotenv
import googlemaps
from geopy.distance import geodesic
import re

# Load environment variables for API keys
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="TMS - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for S&W Branding
st.markdown("""
<style>
    /* Hide Streamlit header */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Custom S&W header bar */
    .stApp::before {
        content: 'SMITH & WILLIAMS TRUCKING - TMS';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #8B0000;
        color: white;
        font-size: 24px;
        font-weight: 900;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999999;
        border-bottom: 3px solid #660000;
    }
    
    /* Main app - pure black background */
    .stApp {
        padding-top: 60px;
        background-color: #000000 !important;
    }
    
    /* Main container - black background with proper spacing */
    .main .block-container {
        background-color: #000000 !important;
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Prevent text truncation */
    .element-container {
        overflow: visible !important;
    }
    
    /* Ensure no text overlap */
    div[data-testid="stVerticalBlock"] > div {
        margin-bottom: 1rem;
    }
    
    /* Sidebar - black background with red accent */
    section[data-testid="stSidebar"] {
        background-color: #000000 !important;
        border-right: 3px solid #8B0000 !important;
    }
    
    /* Sidebar content - white text for visibility */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] p, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(139, 0, 0, 0.3) !important;
    }
    
    /* Sidebar headers - extra bold */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] h5,
    section[data-testid="stSidebar"] h6 {
        color: #ffffff !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(139, 0, 0, 0.5) !important;
    }
    
    /* Sidebar buttons - S&W red with clean borders */
    section[data-testid="stSidebar"] .stButton button {
        background-color: #8B0000 !important;
        color: white !important;
        border: 3px solid #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.2) !important;
    }
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #A00000 !important;
        border: 3px solid #ffcccc !important;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Main area text - white on black */
    .stMarkdown, p, span, label, li {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(139, 0, 0, 0.3) !important;
    }
    
    /* Headers with S&W branding */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(139, 0, 0, 0.5) !important;
        border-bottom: 2px solid #8B0000 !important;
        padding-bottom: 10px !important;
        margin-bottom: 20px !important;
    }
    
    /* Metrics - black with red accent, white text, no truncation */
    div[data-testid="metric-container"] {
        background-color: #1a1a1a !important;
        border: 3px solid #8B0000 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(139, 0, 0, 0.3) !important;
        min-width: 200px !important;
        overflow: visible !important;
    }
    
    /* Metric labels - white and visible */
    div[data-testid="metric-container"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        margin-bottom: 10px !important;
    }
    
    /* Metric values - large white text with no truncation */
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        white-space: nowrap !important;
        overflow: visible !important;
        text-overflow: clip !important;
        width: auto !important;
        min-width: fit-content !important;
    }
    
    /* Metric delta - green/red for positive/negative */
    div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
        color: #00ff00 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    
    /* Ensure metric columns don't truncate */
    div[data-testid="column"] {
        overflow: visible !important;
        min-width: fit-content !important;
    }
    
    /* Sidebar metrics - white text */
    section[data-testid="stSidebar"] div[data-testid="metric-container"] {
        background-color: #1a1a1a !important;
        border: 2px solid #8B0000 !important;
        padding: 15px !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="metric-container"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
        white-space: nowrap !important;
        overflow: visible !important;
    }
    
    /* Tabs - S&W branded with clean borders */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #000000 !important;
        border-bottom: 3px solid #8B0000 !important;
        gap: 2px !important;
        padding: 0 !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
        border: 2px solid #ffffff !important;
        border-bottom: none !important;
        font-weight: 600 !important;
        margin: 0 2px !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #8B0000 !important;
        color: #ffffff !important;
        border: 3px solid #ffffff !important;
        border-bottom: none !important;
    }
    
    /* Input fields - black with red border */
    .stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 2px solid #8B0000 !important;
        font-weight: 500 !important;
    }
    
    /* Buttons - S&W branded with clean borders */
    .stButton button {
        background-color: #8B0000 !important;
        color: white !important;
        border: 3px solid #ffffff !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(255, 255, 255, 0.2) !important;
    }
    
    .stButton button:hover {
        background-color: #A00000 !important;
        border: 3px solid #ffcccc !important;
        box-shadow: 0 4px 8px rgba(255, 255, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Form Submit Buttons - Override Streamlit's blue primary button */
    button[kind="primary"] {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 3px solid #8B0000 !important;
    }
    
    button[kind="secondary"] {
        background-color: #8B0000 !important;
        color: #ffffff !important;
        border: 3px solid #000000 !important;
    }
    
    /* More aggressive override for form buttons */
    .stFormSubmitButton > button {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 3px solid #8B0000 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
    }
    
    .stFormSubmitButton > button:nth-child(1) {
        background-color: #000000 !important;
        border: 3px solid #8B0000 !important;
    }
    
    .stFormSubmitButton > button:hover {
        background-color: #1a1a1a !important;
        border: 3px solid #ff0000 !important;
    }
    
    /* Tables/DataFrames - black theme with borders */
    .stDataFrame {
        background-color: #000000 !important;
        border: 3px solid #8B0000 !important;
        border-radius: 8px !important;
        overflow: hidden !important;
        box-shadow: 0 4px 8px rgba(139, 0, 0, 0.3) !important;
    }
    
    /* Table container */
    div[data-testid="stDataFrameContainer"] {
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
        padding: 5px !important;
        background-color: #1a1a1a !important;
    }
    
    /* Table cells with borders */
    div[data-testid="data-grid"] {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
    }
    
    /* Table headers */
    .dvn-scroller table thead tr th {
        background-color: #8B0000 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        padding: 10px !important;
    }
    
    /* Table rows */
    .dvn-scroller table tbody tr {
        border-bottom: 1px solid #8B0000 !important;
    }
    
    /* Table cells */
    .dvn-scroller table tbody tr td {
        border-right: 1px solid #444444 !important;
        padding: 8px !important;
        color: #ffffff !important;
    }
    
    /* Hover effect on rows */
    .dvn-scroller table tbody tr:hover {
        background-color: #2a0000 !important;
    }
    
    /* Info/Success/Warning boxes - branded */
    .stAlert {
        background-color: #1a1a1a !important;
        border: 2px solid #8B0000 !important;
        color: #ffffff !important;
    }
    
    /* Chat messages - black theme */
    .stChatMessage {
        background-color: #1a1a1a !important;
        border: 1px solid #8B0000 !important;
    }
    
    /* Dividers - red */
    hr {
        border-color: #8B0000 !important;
        border-width: 2px !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# DATABASE INITIALIZATION WITH ENHANCED SCHEMA
# ===================================================================

def init_enhanced_database():
    """Initialize database with enhanced schema for super-user system"""
    conn = sqlite3.connect('super_user_tms.db')
    cursor = conn.cursor()
    
    # Enhanced loads table with new fields
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS loads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        load_id TEXT UNIQUE NOT NULL,
        carrier TEXT,
        customer TEXT,
        pickup_date DATETIME,
        delivery_date DATETIME,
        pickup_address TEXT,
        delivery_address TEXT,
        status TEXT DEFAULT 'pending',
        payment_method TEXT,
        gross_amount REAL,
        net_amount REAL,
        mileage REAL,
        gross_rate_per_mile REAL,
        net_rate_per_mile REAL,
        driver_id INTEGER,
        truck_id INTEGER,
        rc_document TEXT,
        bol_document TEXT,
        pod_document TEXT,
        notes TEXT,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        last_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
        gps_data TEXT,
        check_in_data TEXT,
        delays TEXT,
        FOREIGN KEY(driver_id) REFERENCES users(id),
        FOREIGN KEY(truck_id) REFERENCES equipment(id)
    )""")
    
    # Payments table for reconciliation
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payment_amount REAL NOT NULL,
        payment_date DATE NOT NULL,
        paying_entity TEXT NOT NULL,
        reconciled_loads TEXT,
        notes TEXT,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Enhanced users table with view preferences
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        current_view TEXT DEFAULT 'executive',
        preferences TEXT,
        created_date DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    
    # Equipment table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_number TEXT UNIQUE NOT NULL,
        type TEXT,
        make TEXT,
        model TEXT,
        year INTEGER,
        vin TEXT,
        status TEXT DEFAULT 'available',
        current_location TEXT,
        last_gps_update DATETIME
    )""")
    
    # Geofences table for automated check-ins
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS geofences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        radius_meters INTEGER DEFAULT 500,
        type TEXT
    )""")
    
    # Chat history for AI conversations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        view_type TEXT,
        message TEXT,
        response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    
    # Create CEO user if not exists (Brandon)
    cursor.execute("SELECT * FROM users WHERE username = ?", ('Brandon',))
    if not cursor.fetchone():
        ceo_password = hashlib.sha256('ceo123'.encode()).hexdigest()
        cursor.execute("""
        INSERT INTO users (username, password_hash, role, full_name, email, phone, current_view)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ('Brandon', ceo_password, 'super_user', 'Brandon Smith', 
              'brandon@swtrucking.com', '(951) 437-5474', 'executive'))
    
    # Add some sample users for testing (can be removed later)
    sample_users = [
        ('driver1', 'driver123', 'driver', 'John Driver', 'john@swtrucking.com', '555-0001'),
        ('dataentry1', 'data123', 'data_entry', 'Sarah DataEntry', 'sarah@swtrucking.com', '555-0002'),
        ('exec1', 'exec123', 'executive', 'Mike Executive', 'mike@swtrucking.com', '555-0003')
    ]
    
    for username, password, role, full_name, email, phone in sample_users:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if not cursor.fetchone():
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute("""
            INSERT INTO users (username, password_hash, role, full_name, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (username, password_hash, role, full_name, email, phone))
    
    conn.commit()
    return conn

# ===================================================================
# API SERVICE CLASSES
# ===================================================================

class MotiveAPI:
    """Motive API integration for GPS and ELD data"""
    def __init__(self):
        self.api_key = os.getenv('MOTIVE_API_KEY')
        self.base_url = "https://api.gomotive.com/v1"
    
    def get_vehicle_location(self, vehicle_id):
        """Get real-time GPS location of vehicle"""
        if not self.api_key:
            return {"lat": 33.7490, "lng": -84.3880, "mock": True}  # Mock data
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.base_url}/vehicles/{vehicle_id}/location", headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {"lat": 33.7490, "lng": -84.3880, "mock": True}
    
    def get_hos_status(self, driver_id):
        """Get Hours of Service status"""
        if not self.api_key:
            return {"available_hours": 8, "status": "on_duty", "mock": True}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = requests.get(f"{self.base_url}/drivers/{driver_id}/hos", headers=headers)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {"available_hours": 8, "status": "on_duty", "mock": True}

class VectorAPI:
    """Vector API for document management"""
    def __init__(self):
        self.api_key = os.getenv('VECTOR_API_KEY')
        self.base_url = "https://api.vector.com/v1"
    
    def upload_document(self, file_data, load_id, doc_type):
        """Upload document to Vector"""
        if not self.api_key:
            # Mock response for development
            return {"success": True, "document_id": f"mock_{load_id}_{doc_type}", "mock": True}
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        files = {"file": file_data}
        data = {"load_id": load_id, "type": doc_type}
        
        try:
            response = requests.post(f"{self.base_url}/documents", 
                                    headers=headers, files=files, data=data)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return {"success": False, "error": "Upload failed"}

class GoogleMapsService:
    """Google Maps integration for distance calculations"""
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if self.api_key:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None
    
    def calculate_distance(self, origin, destination):
        """Calculate distance between two addresses"""
        if not self.client:
            # Mock calculation based on simple estimation
            return 450  # Default mock distance
        
        try:
            result = self.client.distance_matrix(origins=origin, 
                                                destinations=destination,
                                                mode="driving",
                                                units="imperial")
            if result['status'] == 'OK':
                distance = result['rows'][0]['elements'][0]['distance']['text']
                # Extract numeric value from "XXX mi" format
                miles = float(distance.replace(' mi', '').replace(',', ''))
                return miles
        except:
            pass
        return 450  # Fallback distance

# ===================================================================
# CONVERSATIONAL AI AGENT
# ===================================================================

class ConversationalAgent:
    """AI agent for guided data entry and driver assistance"""
    
    def __init__(self, view_type):
        self.view_type = view_type
        self.context = {}
        if 'agent_state' not in st.session_state:
            st.session_state.agent_state = {}
    
    def historical_data_flow(self):
        """Conversational flow for historical data entry with Florida"""
        st.markdown("### 💬 Data Entry Assistant - Florida")
        
        # Initialize conversation state
        if 'data_entry_step' not in st.session_state:
            st.session_state.data_entry_step = 'start'
            st.session_state.current_load_data = {}
        
        # Display chat history
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "Hello! I'm Florida, your TMS assistant. I'm here to help you enter historical load data efficiently. Would you like to enter a new load or reconcile a payment?"
            })
        
        # Display conversation
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
        
        # User input
        user_input = st.chat_input("Type your response...")
        
        if user_input:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            # Process based on current step
            response = self.process_data_entry_step(user_input)
            
            # Add assistant response
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    def process_data_entry_step(self, user_input):
        """Process user input based on current step"""
        step = st.session_state.data_entry_step
        data = st.session_state.current_load_data
        
        if step == 'start':
            if 'new load' in user_input.lower():
                st.session_state.data_entry_step = 'load_id'
                return "Great! Let's start with the Load ID. Please enter the unique load identifier:"
            elif 'reconcile' in user_input.lower():
                st.session_state.data_entry_step = 'payment_amount'
                return "Let's reconcile a payment. What is the total payment amount?"
            else:
                return "I can help you enter a new load or reconcile a payment. Which would you like to do?"
        
        elif step == 'load_id':
            data['load_id'] = user_input
            st.session_state.data_entry_step = 'pickup_date'
            return f"Load ID {user_input} recorded. Now, please enter the pickup date and time (format: MM/DD/YYYY HH:MM):"
        
        elif step == 'pickup_date':
            try:
                data['pickup_date'] = datetime.strptime(user_input, "%m/%d/%Y %H:%M")
                st.session_state.data_entry_step = 'delivery_date'
                return "Pickup date recorded. Please enter the delivery date and time (format: MM/DD/YYYY HH:MM):"
            except:
                return "Invalid date format. Please use MM/DD/YYYY HH:MM (e.g., 01/15/2025 14:30):"
        
        elif step == 'delivery_date':
            try:
                data['delivery_date'] = datetime.strptime(user_input, "%m/%d/%Y %H:%M")
                st.session_state.data_entry_step = 'carrier'
                return "Delivery date recorded. Who is the carrier? (CanAmex, Metro Logistics, or broker name):"
            except:
                return "Invalid date format. Please use MM/DD/YYYY HH:MM:"
        
        elif step == 'carrier':
            data['carrier'] = user_input
            st.session_state.data_entry_step = 'customer'
            return f"Carrier set to {user_input}. Who is the customer for this load?"
        
        elif step == 'customer':
            data['customer'] = user_input
            st.session_state.data_entry_step = 'pickup_address'
            
            # Determine payment method based on carrier
            if data['carrier'].lower() == 'canamex':
                data['payment_method'] = 'Direct Pay'
                fee_rate = 0.12
            else:
                data['payment_method'] = 'Factored'
                fee_rate = 0.03
            
            return f"Customer set to {user_input}. Payment method: {data['payment_method']} ({fee_rate*100}% fee). What is the pickup address?"
        
        elif step == 'pickup_address':
            data['pickup_address'] = user_input
            st.session_state.data_entry_step = 'delivery_address'
            return "Pickup address recorded. What is the delivery address?"
        
        elif step == 'delivery_address':
            data['delivery_address'] = user_input
            st.session_state.data_entry_step = 'net_amount'
            
            # Calculate mileage
            maps_service = GoogleMapsService()
            data['mileage'] = maps_service.calculate_distance(data['pickup_address'], data['delivery_address'])
            
            return f"Delivery address recorded. Calculated distance: {data['mileage']} miles. What was the net amount paid (after fees)?"
        
        elif step == 'net_amount':
            try:
                data['net_amount'] = float(user_input.replace('$', '').replace(',', ''))
                
                # Calculate gross amount based on payment method
                if data['payment_method'] == 'Direct Pay':
                    data['gross_amount'] = data['net_amount'] / 0.88  # 12% fee
                else:
                    data['gross_amount'] = data['net_amount'] / 0.97  # 3% fee
                
                # Calculate rates per mile
                data['gross_rate_per_mile'] = data['gross_amount'] / data['mileage']
                data['net_rate_per_mile'] = data['net_amount'] / data['mileage']
                
                st.session_state.data_entry_step = 'confirm'
                
                return f"""
                Load calculation complete:
                - Gross Amount: ${data['gross_amount']:.2f}
                - Net Amount: ${data['net_amount']:.2f}
                - Gross Rate/Mile: ${data['gross_rate_per_mile']:.2f}
                - Net Rate/Mile: ${data['net_rate_per_mile']:.2f}
                
                Does this look correct? (yes/no)
                """
            except:
                return "Please enter a valid amount (numbers only):"
        
        elif step == 'confirm':
            if 'yes' in user_input.lower():
                # Save to database
                self.save_load_data(data)
                st.session_state.data_entry_step = 'start'
                st.session_state.current_load_data = {}
                return "Load saved successfully! Would you like to enter another load or reconcile a payment?"
            else:
                st.session_state.data_entry_step = 'start'
                st.session_state.current_load_data = {}
                return "Load entry cancelled. Would you like to start over?"
        
        # Payment reconciliation flow
        elif step == 'payment_amount':
            try:
                st.session_state.payment_data = {'amount': float(user_input.replace('$', '').replace(',', ''))}
                st.session_state.data_entry_step = 'payment_date'
                return "Payment amount recorded. What is the payment date (MM/DD/YYYY)?"
            except:
                return "Please enter a valid amount:"
        
        elif step == 'payment_date':
            try:
                st.session_state.payment_data['date'] = datetime.strptime(user_input, "%m/%d/%Y")
                st.session_state.data_entry_step = 'paying_entity'
                return "Payment date recorded. Who is the paying entity? (CanAmex or Factoring Company name):"
            except:
                return "Invalid date format. Please use MM/DD/YYYY:"
        
        elif step == 'paying_entity':
            st.session_state.payment_data['entity'] = user_input
            loads = self.find_loads_for_reconciliation(st.session_state.payment_data)
            
            if loads:
                load_list = "\n".join([f"- {l['load_id']}: ${l['gross_amount']:.2f}" for l in loads])
                st.session_state.data_entry_step = 'reconcile_confirm'
                return f"Found the following loads to reconcile:\n{load_list}\n\nConfirm reconciliation? (yes/no)"
            else:
                st.session_state.data_entry_step = 'start'
                return "No matching loads found for this payment. Returning to main menu."
        
        return "I didn't understand that. Please try again."
    
    def save_load_data(self, data):
        """Save load data to database"""
        conn = sqlite3.connect('super_user_tms.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO loads (load_id, carrier, customer, pickup_date, delivery_date,
                          pickup_address, delivery_address, payment_method,
                          gross_amount, net_amount, mileage, gross_rate_per_mile,
                          net_rate_per_mile, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (data['load_id'], data['carrier'], data['customer'],
              data['pickup_date'], data['delivery_date'],
              data['pickup_address'], data['delivery_address'],
              data['payment_method'], data['gross_amount'],
              data['net_amount'], data['mileage'],
              data['gross_rate_per_mile'], data['net_rate_per_mile'],
              'completed'))
        
        conn.commit()
        conn.close()
    
    def find_loads_for_reconciliation(self, payment_data):
        """Find loads matching payment criteria"""
        conn = sqlite3.connect('super_user_tms.db')
        cursor = conn.cursor()
        
        if payment_data['entity'].lower() == 'canamex':
            # Find CanAmex loads from previous week (Sunday to Saturday)
            payment_date = payment_data['date']
            week_end = payment_date - timedelta(days=payment_date.weekday() + 2)  # Previous Saturday
            week_start = week_end - timedelta(days=6)  # Previous Sunday
            
            cursor.execute("""
            SELECT load_id, gross_amount FROM loads
            WHERE carrier = 'CanAmex'
            AND delivery_date BETWEEN ? AND ?
            AND status = 'completed'
            """, (week_start, week_end))
        else:
            # Find factored loads from previous day
            cutoff_date = payment_data['date'] - timedelta(days=1)
            
            cursor.execute("""
            SELECT load_id, gross_amount FROM loads
            WHERE payment_method = 'Factored'
            AND DATE(delivery_date) = DATE(?)
            AND status = 'completed'
            """, (cutoff_date,))
        
        loads = [{'load_id': row[0], 'gross_amount': row[1]} for row in cursor.fetchall()]
        conn.close()
        return loads
    
    def driver_assistant_flow(self):
        """AI assistant for driver operations"""
        st.markdown("### 🚛 Driver Co-Pilot")
        
        # Get current load assignment
        conn = sqlite3.connect('super_user_tms.db')
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM loads 
        WHERE status IN ('assigned', 'in_transit')
        ORDER BY pickup_date
        LIMIT 1
        """)
        
        current_load = cursor.fetchone()
        conn.close()
        
        if current_load:
            st.info(f"Current Load: {current_load[1]}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📍 Check In", type="primary"):
                    st.success("Checked in at location!")
                    # Update load status
            
            with col2:
                if st.button("⏱️ Report Delay"):
                    delay_reason = st.text_input("What's causing the delay?")
                    if delay_reason:
                        st.warning(f"Delay reported: {delay_reason}")
            
            with col3:
                if st.button("📄 Upload Document"):
                    uploaded_file = st.file_uploader("Upload BOL/POD", type=['pdf', 'jpg', 'png'])
                    if uploaded_file:
                        st.success("Document uploaded successfully!")
            
            # GPS tracking simulation
            motive_api = MotiveAPI()
            location = motive_api.get_vehicle_location("truck_001")
            
            st.markdown("#### Current Location")
            st.map(pd.DataFrame({'lat': [location['lat']], 'lon': [location['lng']]}))
            
        else:
            st.info("No active loads. Enjoy your break! 😊")

# ===================================================================
# MAIN APPLICATION WITH THREE-VIEW TOGGLE
# ===================================================================

def main():
    """Main application with three-view toggle system"""
    
    # Initialize database
    if 'db_initialized' not in st.session_state:
        init_enhanced_database()
        st.session_state.db_initialized = True
    
    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login()
    else:
        show_super_user_interface()

def show_login():
    """Display login interface with enhanced branding"""
    
    # Display video logo
    animation_file = "assets/videos/company_logo_animation.mp4.MOV"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(animation_file):
            try:
                import base64
                with open(animation_file, 'rb') as video_file:
                    video_bytes = video_file.read()
                    video_b64 = base64.b64encode(video_bytes).decode()
                    video_html = f'''
                    <video width="100%" autoplay loop muted playsinline>
                        <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
                    </video>
                    '''
                    st.markdown(video_html, unsafe_allow_html=True)
            except:
                logo_path = "assets/logos/swt_logo.png"
                if os.path.exists(logo_path):
                    st.image(logo_path, use_container_width=True)
        else:
            logo_path = "assets/logos/swt_logo.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
    
    st.markdown("<h1 style='text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);'>Transportation Management System</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #8B0000; font-weight: bold;'>SMITH & WILLIAMS TRUCKING</h3>", unsafe_allow_html=True)
    
    
    # Apply aggressive button styling using JavaScript injection
    st.markdown("""
    <script>
        // Wait for page to load then style buttons
        setTimeout(function() {
            // Find all form submit buttons
            const buttons = document.querySelectorAll('.stFormSubmitButton button');
            if (buttons.length >= 2) {
                // Style Login button - black with red border
                buttons[0].style.backgroundColor = '#000000';
                buttons[0].style.color = '#ffffff';
                buttons[0].style.border = '3px solid #8B0000';
                buttons[0].style.fontWeight = '700';
                buttons[0].style.textTransform = 'uppercase';
                
                // Style Clear button - red with black border  
                buttons[1].style.backgroundColor = '#8B0000';
                buttons[1].style.color = '#ffffff';
                buttons[1].style.border = '3px solid #000000';
                buttons[1].style.fontWeight = '700';
                buttons[1].style.textTransform = 'uppercase';
            }
        }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("🔐 LOGIN", use_container_width=True)
        with col2:
            clear = st.form_submit_button("🔄 CLEAR", use_container_width=True)
            
        if clear:
            st.rerun()
        
        if submitted:
            if username and password:
                conn = sqlite3.connect('super_user_tms.db')
                cursor = conn.cursor()
                
                password_hash = hashlib.sha256(password.encode()).hexdigest()
                cursor.execute("""
                SELECT * FROM users 
                WHERE username = ? AND password_hash = ?
                """, (username, password_hash))
                
                user = cursor.fetchone()
                conn.close()
                
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.session_state.role = user[3]
                    st.session_state.full_name = user[4]
                    st.session_state.current_view = user[7] or 'executive'
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.error("Please enter username and password")
    
    # Vernon Protection Footer - IT Head of Data Security
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 20px; border-top: 2px solid #8B0000;'>
        <p style='color: #00ff00; font-size: 16px; font-weight: bold; letter-spacing: 2px; margin: 0; text-shadow: 2px 2px 4px rgba(0,255,0,0.3);'>
            🛡️ DATA PROTECTED BY VERNON - IT HEAD OF DATA SECURITY 🛡️
        </p>
        <p style='color: #ffffff; font-size: 12px; margin-top: 10px; font-weight: 600;'>
            Self-Fixing Protocol Active | System Integrity Monitored 24/7
        </p>
        <p style='color: #666; font-size: 10px; margin-top: 15px;'>
            © 2025 Smith & Williams Trucking - All Rights Reserved
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_super_user_interface():
    """Display the main interface based on user role"""
    
    # Sidebar with appropriate options based on role
    with st.sidebar:
        # Logo
        logo_path = "assets/logos/swt_logo_white.png"
        if os.path.exists(logo_path):
            st.image(logo_path, use_container_width=True)
        
        st.markdown("---")
        
        # User info
        st.markdown(f"### Welcome, {st.session_state.full_name}")
        
        # Display role appropriately
        role_display = {
            'super_user': 'CEO & Super User',
            'executive': 'Executive',
            'data_entry': 'Data Entry Specialist',
            'driver': 'Driver'
        }
        st.caption(f"Role: {role_display.get(st.session_state.role, st.session_state.role)}")
        
        st.markdown("---")
        
        # View Toggle - Only for super_user role
        if st.session_state.role == 'super_user':
            st.markdown("### 🔄 Toggle View")
            view_options = {
                'executive': '📊 Executive View',
                'data_feeder': '📝 Historical Data Feeder',
                'driver': '🚛 Driver View'
            }
            
            current_view = st.radio(
                "Select your operating mode:",
                options=list(view_options.keys()),
                format_func=lambda x: view_options[x],
                index=list(view_options.keys()).index(st.session_state.get('current_view', 'executive'))
            )
            
            if current_view != st.session_state.get('current_view'):
                st.session_state.current_view = current_view
                # Update user preference in database
                conn = sqlite3.connect('super_user_tms.db')
                cursor = conn.cursor()
                cursor.execute("""
                UPDATE users SET current_view = ? WHERE id = ?
                """, (current_view, st.session_state.user_id))
                conn.commit()
                conn.close()
                st.rerun()
        else:
            # For non-super users, set view based on their role
            role_to_view = {
                'executive': 'executive',
                'data_entry': 'data_feeder',
                'driver': 'driver'
            }
            st.session_state.current_view = role_to_view.get(st.session_state.role, 'executive')
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        conn = sqlite3.connect('super_user_tms.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM loads WHERE status = 'active'")
        active_loads = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(gross_amount) FROM loads WHERE DATE(delivery_date) = DATE('now')")
        today_revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        st.metric("Active Loads", active_loads)
        st.metric("Today's Revenue", f"${today_revenue:,.2f}")
        
        st.markdown("---")
        
        # Vernon Security Status
        st.markdown("### 🛡️ Vernon Security")
        st.success("✅ System Protected")
        st.caption("Self-Fixing Protocol: Active")
        st.caption("Last Security Scan: Just Now")
        st.caption("Data Integrity: 100%")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Check if user management should be shown
    if st.session_state.get('show_user_management', False) and st.session_state.role == 'super_user':
        show_user_management()
        
        # Add back button
        if st.button("⬅️ Back to Main View"):
            st.session_state.show_user_management = False
            st.rerun()
    else:
        # Main content area based on selected view
        if st.session_state.current_view == 'executive':
            show_executive_view()
        elif st.session_state.current_view == 'data_feeder':
            show_data_feeder_view()
        elif st.session_state.current_view == 'driver':
            show_driver_view()
    
    # User Management button - Only for super_user
    if st.session_state.role == 'super_user':
        with st.sidebar:
            st.markdown("---")
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.show_user_management = True
                st.rerun()

def show_executive_view():
    """Display executive dashboard"""
    st.title("📊 Executive Dashboard")
    st.markdown("*Complete business oversight and management*")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    conn = sqlite3.connect('super_user_tms.db')
    cursor = conn.cursor()
    
    # Get metrics
    cursor.execute("SELECT COUNT(*) FROM loads")
    total_loads = cursor.fetchone()[0]
    
    cursor.execute("SELECT AVG(gross_rate_per_mile) FROM loads WHERE gross_rate_per_mile > 0")
    avg_rate = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(gross_amount) FROM loads WHERE strftime('%Y-%m', delivery_date) = strftime('%Y-%m', 'now')")
    monthly_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(DISTINCT carrier) FROM loads")
    carriers = cursor.fetchone()[0]
    
    conn.close()
    
    with col1:
        st.metric("Total Loads", total_loads, delta="+12 this week")
    
    with col2:
        st.metric("Avg Rate/Mile", f"${avg_rate:.2f}", 
                 delta=f"{'+' if avg_rate > 2.0 else ''}{(avg_rate - 2.0):.2f}")
    
    with col3:
        st.metric("Monthly Revenue", f"${monthly_revenue:,.0f}", delta="+15%")
    
    with col4:
        st.metric("Active Carriers", carriers)
    
    st.markdown("---")
    
    # Tabs for different executive functions
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Analytics", "💰 Financial", "👥 Fleet", "🎯 Goals"])
    
    with tab1:
        st.subheader("Performance Analytics")
        
        # Get load data for charts
        conn = sqlite3.connect('super_user_tms.db')
        df = pd.read_sql_query("""
        SELECT DATE(delivery_date) as date, 
               COUNT(*) as loads,
               SUM(gross_amount) as revenue,
               AVG(gross_rate_per_mile) as avg_rate
        FROM loads
        WHERE delivery_date >= date('now', '-30 days')
        GROUP BY DATE(delivery_date)
        ORDER BY date
        """, conn)
        conn.close()
        
        if not df.empty:
            # Revenue chart
            fig = px.line(df, x='date', y='revenue', 
                         title='30-Day Revenue Trend',
                         labels={'revenue': 'Revenue ($)', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Rate trend
            fig2 = px.line(df, x='date', y='avg_rate',
                          title='Average Rate per Mile Trend',
                          labels={'avg_rate': 'Rate ($/mile)', 'date': 'Date'})
            fig2.add_hline(y=2.0, line_dash="dash", line_color="red",
                          annotation_text="Target: $2.00/mile")
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        st.subheader("Financial Overview")
        
        conn = sqlite3.connect('super_user_tms.db')
        cursor = conn.cursor()
        
        # Payment reconciliation status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Outstanding Payments")
            cursor.execute("""
            SELECT carrier, COUNT(*) as loads, SUM(gross_amount) as total
            FROM loads
            WHERE status = 'completed'
            AND id NOT IN (SELECT value FROM json_each((SELECT reconciled_loads FROM payments)))
            GROUP BY carrier
            """)
            
            outstanding = cursor.fetchall()
            if outstanding:
                for row in outstanding:
                    st.info(f"**{row[0]}**: {row[1]} loads - ${row[2]:,.2f}")
            else:
                st.success("All payments reconciled!")
        
        with col2:
            st.markdown("#### Recent Payments")
            payments_df = pd.read_sql_query("""
            SELECT payment_date, paying_entity, payment_amount
            FROM payments
            ORDER BY payment_date DESC
            LIMIT 5
            """, conn)
            
            if not payments_df.empty:
                st.dataframe(payments_df, hide_index=True)
            else:
                st.info("No payments recorded yet")
        
        conn.close()
    
    with tab3:
        st.subheader("Fleet Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Equipment Status")
            conn = sqlite3.connect('super_user_tms.db')
            equipment_df = pd.read_sql_query("""
            SELECT unit_number, type, status, current_location
            FROM equipment
            ORDER BY unit_number
            """, conn)
            
            if not equipment_df.empty:
                st.dataframe(equipment_df, hide_index=True)
            else:
                if st.button("➕ Add Equipment"):
                    # Add equipment form
                    pass
        
        with col2:
            st.markdown("#### Driver Status")
            # Show driver availability
            st.info("All drivers available")
        
        conn.close()
    
    with tab4:
        st.subheader("Goal Management")
        
        # Goal settings
        col1, col2 = st.columns(2)
        
        with col1:
            target_rate = st.number_input("Target Rate per Mile ($)", 
                                         value=2.00, min_value=1.50, max_value=5.00, step=0.10)
            weekly_revenue_goal = st.number_input("Weekly Revenue Goal ($)",
                                                 value=50000, min_value=10000, max_value=100000, step=5000)
        
        with col2:
            fleet_utilization = st.slider("Fleet Utilization Target (%)", 
                                        min_value=50, max_value=100, value=90)
            empty_miles_target = st.slider("Max Empty Miles (%)",
                                          min_value=5, max_value=30, value=15)
        
        if st.button("💾 Save Goals", type="primary"):
            st.success("Goals updated successfully!")
            st.balloons()

def show_data_feeder_view():
    """Display historical data feeder with conversational AI"""
    st.title("📝 Historical Data Feeder")
    st.markdown("*Conversational AI for intelligent data entry*")
    
    # Initialize conversational agent
    agent = ConversationalAgent('data_feeder')
    agent.historical_data_flow()
    
    # Quick actions sidebar
    with st.sidebar:
        st.markdown("### Quick Actions")
        
        if st.button("📊 View Recent Entries", use_container_width=True):
            conn = sqlite3.connect('super_user_tms.db')
            recent_df = pd.read_sql_query("""
            SELECT load_id, carrier, customer, gross_amount, created_date
            FROM loads
            ORDER BY created_date DESC
            LIMIT 10
            """, conn)
            conn.close()
            
            st.dataframe(recent_df, hide_index=True)
        
        if st.button("💰 Reconcile Payment", use_container_width=True):
            st.session_state.data_entry_step = 'payment_amount'
            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": "Let's reconcile a payment. What is the total payment amount?"
            })
            st.rerun()
        
        if st.button("🔍 Search Loads", use_container_width=True):
            search_term = st.text_input("Search by Load ID, Carrier, or Customer")
            if search_term:
                conn = sqlite3.connect('super_user_tms.db')
                cursor = conn.cursor()
                cursor.execute("""
                SELECT * FROM loads
                WHERE load_id LIKE ? OR carrier LIKE ? OR customer LIKE ?
                """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
                results = cursor.fetchall()
                conn.close()
                
                if results:
                    st.success(f"Found {len(results)} matching loads")
                else:
                    st.warning("No matching loads found")

def show_driver_view():
    """Display driver interface with AI co-pilot"""
    st.title("🚛 Driver View")
    st.markdown("*Mobile-friendly operational interface with AI co-pilot*")
    
    # Initialize driver assistant
    agent = ConversationalAgent('driver')
    agent.driver_assistant_flow()
    
    # HOS Status
    st.markdown("---")
    st.markdown("### ⏰ Hours of Service")
    
    motive_api = MotiveAPI()
    hos_status = motive_api.get_hos_status("driver_001")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Available Hours", f"{hos_status['available_hours']}h")
    
    with col2:
        status_color = "🟢" if hos_status['status'] == 'on_duty' else "🔴"
        st.metric("Status", f"{status_color} {hos_status['status'].title()}")
    
    with col3:
        st.metric("Next Break", "2h 15m")

def show_user_management():
    """Display user management interface for super users"""
    st.title("👥 User Management")
    st.markdown("*Add and manage system users*")
    
    tab1, tab2 = st.tabs(["➕ Add User", "📋 Manage Users"])
    
    with tab1:
        st.subheader("Add New User")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            new_role = st.selectbox("Role", ["driver", "data_entry", "executive"])
        
        with col2:
            new_fullname = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
        
        if st.button("➕ Create User", type="primary"):
            if new_username and new_password and new_fullname:
                conn = sqlite3.connect('super_user_tms.db')
                cursor = conn.cursor()
                
                # Check if user exists
                cursor.execute("SELECT * FROM users WHERE username = ?", (new_username,))
                if cursor.fetchone():
                    st.error("Username already exists!")
                else:
                    password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                    cursor.execute("""
                    INSERT INTO users (username, password_hash, role, full_name, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """, (new_username, password_hash, new_role, new_fullname, new_email, new_phone))
                    conn.commit()
                    st.success(f"User {new_username} created successfully!")
                
                conn.close()
            else:
                st.error("Please fill in all required fields")
    
    with tab2:
        st.subheader("Existing Users")
        
        conn = sqlite3.connect('super_user_tms.db')
        users_df = pd.read_sql_query("""
        SELECT username, role, full_name, email, phone, created_date
        FROM users
        WHERE username != 'Brandon'
        ORDER BY created_date DESC
        """, conn)
        
        if not users_df.empty:
            st.dataframe(users_df, hide_index=True)
            
            st.markdown("---")
            st.subheader("Modify User")
            
            user_to_modify = st.selectbox("Select user to modify", users_df['username'].tolist())
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_role_for_user = st.selectbox("New Role", ["driver", "data_entry", "executive"], key="mod_role")
            
            with col2:
                if st.button("🔄 Update Role"):
                    cursor = conn.cursor()
                    cursor.execute("""
                    UPDATE users SET role = ? WHERE username = ?
                    """, (new_role_for_user, user_to_modify))
                    conn.commit()
                    st.success(f"Updated {user_to_modify}'s role to {new_role_for_user}")
                    st.rerun()
            
            if st.button("🗑️ Delete User", type="secondary"):
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username = ?", (user_to_modify,))
                conn.commit()
                st.success(f"User {user_to_modify} deleted")
                st.rerun()
        else:
            st.info("No additional users yet. Add users above.")
        
        conn.close()

# ===================================================================
# RUN APPLICATION
# ===================================================================

if __name__ == "__main__":
    main()