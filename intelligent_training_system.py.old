"""
===================================================================
TRAINING CENTER - TRANSPORTATION MANAGEMENT SYSTEM
Smith & Williams Trucking LLC
Powered by Zelma AI
===================================================================
AI-Powered Adaptive Learning for Smith & Williams Trucking TMS

Meet Zelma - Your Intelligent Training Specialist from Chicago:
- Automatically generates training for new features
- Creates role-specific learning paths  
- Adapts to system changes in real-time
- Tracks your progress and effectiveness
- Generates process flow training
- Provides personalized recommendations
- Learns from your interactions to improve training

"Hello, I'm Zelma from Chicago! I specialize in making complex systems simple and accessible. Let's master this together."
===================================================================
"""

import streamlit as st
import pandas as pd
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
import time
import os
import re
import ast
import inspect
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Training Center - Smith & Williams",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better readability and less reflective backgrounds
st.markdown("""
<style>
    /* Hide Streamlit's default header toolbar with Deploy button */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Push content down to account for custom header */
    .stApp > div:first-child {
        padding-top: 70px !important;
    }
    
    /* Main background - softer, less reflective */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding-top: 70px;
    }
    
    /* Sidebar - S&W branded with red accent */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2a0000 0%, #1f1f1f 10%) !important;
        border-right: 2px solid #8B0000 !important;
    }
    
    /* Text contrast improvements - BOLD white text, no backgrounds */
    .stMarkdown, .stText {
        color: #ffffff !important;
        background-color: transparent !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Headers - BOLD white text, no backgrounds */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        background-color: transparent !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.9) !important;
    }
    
    /* All paragraph text - brighter and bolder */
    p {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
    }
    
    /* Labels and captions - much brighter */
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    .caption {
        color: #ffcccc !important;
        font-weight: 500 !important;
    }
    
    /* Remove selection highlights */
    ::selection {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Info boxes - S&W branded with readable text */
    .stAlert {
        background-color: rgba(45, 45, 45, 0.9) !important;
        border-left: 4px solid #8B0000 !important;
        border-right: 1px solid rgba(139, 0, 0, 0.3) !important;
        border-top: 1px solid rgba(139, 0, 0, 0.3) !important;
        border-bottom: 1px solid rgba(139, 0, 0, 0.3) !important;
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    .stAlert > div {
        color: #ffffff !important;
    }
    
    /* Buttons - S&W branded with bold text */
    .stButton > button {
        background-color: #2d2d2d !important;
        color: #ffffff !important;
        border: 2px solid #8B0000 !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8) !important;
    }
    
    .stButton > button:hover {
        background-color: #8B0000 !important;
        border: 1px solid #ff0000 !important;
        box-shadow: 0 0 10px rgba(139, 0, 0, 0.5) !important;
    }
    
    /* Primary buttons - S&W red */
    .stButton > button[kind="primary"] {
        background-color: #8B0000 !important;
        border: 1px solid #ff0000 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #660000 !important;
        border: 1px solid #ff0000 !important;
    }
    
    /* Metrics - S&W branded */
    [data-testid="metric-container"] {
        background-color: transparent !important;
        padding: 10px !important;
        border-radius: 5px !important;
        border-left: 3px solid #8B0000 !important;
        border-right: 1px solid rgba(139, 0, 0, 0.2) !important;
        border-top: 1px solid rgba(139, 0, 0, 0.2) !important;
        border-bottom: 1px solid rgba(139, 0, 0, 0.2) !important;
    }
    
    /* Remove any text backgrounds and make text bold */
    p, span, div {
        background-color: transparent !important;
    }
    
    /* Make ALL text more visible */
    * {
        -webkit-font-smoothing: antialiased !important;
        -moz-osx-font-smoothing: grayscale !important;
    }
    
    /* Sidebar text - extra bold and bright */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] p {
        color: #ffffff !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Input fields - S&W branded */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #8B0000 !important;
        border-radius: 4px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border: 2px solid #ff0000 !important;
        box-shadow: 0 0 5px rgba(139, 0, 0, 0.5) !important;
    }
    
    /* Tables - S&W branded */
    .dataframe {
        background-color: #2a2a2a !important;
        color: #ffffff !important;
        border: 1px solid #8B0000 !important;
    }
    
    /* Progress bars - S&W red */
    .stProgress > div > div > div > div {
        background-color: #8B0000 !important;
    }
    
    /* Expanders - S&W branded */
    .streamlit-expanderHeader {
        border: 1px solid #8B0000 !important;
        background-color: rgba(139, 0, 0, 0.1) !important;
    }
    
    /* Tabs - S&W branded */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #8B0000 !important;
    }
    
    /* Success/Info boxes with S&W accent */
    .stSuccess {
        border-left: 4px solid #8B0000 !important;
    }
    
    .stInfo {
        border-left: 4px solid #8B0000 !important;
    }
    
    /* Code blocks - softer */
    .stCodeBlock {
        background-color: #1f1f1f !important;
    }
</style>
""", unsafe_allow_html=True)

# ===================================================================
# DYNAMIC TRAINING ENGINE
# ===================================================================

class DynamicTrainingEngine:
    """AI-powered engine that creates and updates training automatically"""
    
    def __init__(self):
        self.system_files = ['four_tier_tms.py', 'config/COMPLETE_SYSTEM_TEMPLATE_PACKAGE.py']
        self.db_path = 'training_intelligence.db'
        self.init_training_db()  # Initialize database structure
        self.roles = self.detect_system_roles()
        self.features = self.scan_system_features()
        self.process_flows = self.extract_process_flows()
    
    def get_db_connection(self):
        """Get a new database connection for thread safety"""
        return sqlite3.connect(self.db_path, check_same_thread=False)
        
    def init_training_db(self):
        """Initialize training database for tracking"""
        conn = sqlite3.connect('training_intelligence.db')
        cursor = conn.cursor()
        
        # Training modules table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_modules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            module_name TEXT UNIQUE,
            module_type TEXT,
            target_role TEXT,
            content TEXT,
            created_date TEXT,
            last_updated TEXT,
            version INTEGER,
            auto_generated BOOLEAN,
            effectiveness_score REAL
        )""")
        
        # User progress tracking
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            module_id INTEGER,
            started_date TEXT,
            completed_date TEXT,
            score REAL,
            time_spent INTEGER,
            attempts INTEGER,
            FOREIGN KEY(module_id) REFERENCES training_modules(id)
        )""")
        
        # Feature detection table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feature_name TEXT UNIQUE,
            feature_type TEXT,
            tier INTEGER,
            description TEXT,
            discovered_date TEXT,
            training_created BOOLEAN
        )""")
        
        # Process flows table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS process_flows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process_name TEXT,
            steps TEXT,
            roles_involved TEXT,
            tier INTEGER,
            training_module_id INTEGER,
            FOREIGN KEY(training_module_id) REFERENCES training_modules(id)
        )""")
        
        conn.commit()
        conn.close()
    
    def detect_system_roles(self):
        """Automatically detect roles from the system"""
        roles = {
            'ceo': {
                'name': 'CEO',
                'permissions': 'ALL',
                'dual_mode': True,
                'tiers': [1, 2, 3, 4],
                'priority_features': ['goal_management', 'executive_reports', 'user_management', 'driver_operations']
            },
            'admin': {
                'name': 'Administrator',
                'permissions': 'ADMIN',
                'dual_mode': False,
                'tiers': [1, 2, 3],
                'priority_features': ['user_management', 'system_settings', 'reports']
            },
            'dispatcher': {
                'name': 'Dispatcher',
                'permissions': 'DISPATCH',
                'dual_mode': False,
                'tiers': [1],
                'priority_features': ['load_booking', 'driver_assignment', 'negotiation_tool', 'load_tracking']
            },
            'driver': {
                'name': 'Driver',
                'permissions': 'DRIVER',
                'dual_mode': False,
                'tiers': [1],
                'priority_features': ['load_viewing', 'document_upload', 'navigation', 'hos_tracking']
            },
            'accounting': {
                'name': 'Accounting',
                'permissions': 'ACCOUNTING',
                'dual_mode': False,
                'tiers': [2, 3],
                'priority_features': ['invoicing', 'payments', 'factoring', 'reports']
            },
            'safety': {
                'name': 'Safety Manager',
                'permissions': 'SAFETY',
                'dual_mode': False,
                'tiers': [3],
                'priority_features': ['compliance', 'driver_files', 'maintenance', 'incidents']
            }
        }
        
        # Check for new roles in the system
        try:
            if os.path.exists('four_tier_tms.py'):
                with open('four_tier_tms.py', 'r') as f:
                    content = f.read()
                    # Look for role definitions
                    role_pattern = r"role\s*[=:]\s*['\"](\w+)['\"]"
                    found_roles = re.findall(role_pattern, content, re.IGNORECASE)
                    
                    for role in found_roles:
                        if role.lower() not in roles:
                            # New role detected - create training
                            roles[role.lower()] = {
                                'name': role.capitalize(),
                                'permissions': 'CUSTOM',
                                'dual_mode': False,
                                'tiers': [1, 2],
                                'priority_features': [],
                                'auto_detected': True,
                                'needs_training': True
                            }
        except:
            pass
            
        return roles
    
    def scan_system_features(self):
        """Scan system files to detect features"""
        features = {}
        
        # Core features we know about
        known_features = {
            'load_management': {'tier': 1, 'type': 'operational', 'roles': ['dispatcher', 'ceo', 'admin']},
            'driver_assignment': {'tier': 1, 'type': 'operational', 'roles': ['dispatcher', 'ceo']},
            'document_management': {'tier': 1, 'type': 'operational', 'roles': ['driver', 'dispatcher', 'accounting']},
            'invoicing': {'tier': 2, 'type': 'financial', 'roles': ['accounting', 'ceo']},
            'goal_management': {'tier': 4, 'type': 'ai', 'roles': ['ceo']},
            'negotiation_tool': {'tier': 1, 'type': 'operational', 'roles': ['dispatcher', 'ceo']},
            'smart_load_finder': {'tier': 4, 'type': 'ai', 'roles': ['dispatcher', 'ceo']},
            'factoring': {'tier': 2, 'type': 'financial', 'roles': ['accounting', 'ceo']},
            'compliance_tracking': {'tier': 3, 'type': 'compliance', 'roles': ['safety', 'ceo']},
            'maintenance_tracking': {'tier': 2, 'type': 'operational', 'roles': ['safety', 'admin']}
        }
        
        # Scan for new features
        for file_path in self.system_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        
                        # Look for function definitions
                        func_pattern = r"def\s+(\w+)\s*\([^)]*\):"
                        functions = re.findall(func_pattern, content)
                        
                        # Look for class definitions
                        class_pattern = r"class\s+(\w+)\s*[:\(]"
                        classes = re.findall(class_pattern, content)
                        
                        # Identify potential new features
                        for func in functions:
                            if func not in features and func not in ['__init__', 'main']:
                                # Analyze function name to determine feature
                                if any(keyword in func.lower() for keyword in ['load', 'dispatch', 'book']):
                                    features[func] = {'tier': 1, 'type': 'operational', 'auto_detected': True}
                                elif any(keyword in func.lower() for keyword in ['invoice', 'payment', 'factor']):
                                    features[func] = {'tier': 2, 'type': 'financial', 'auto_detected': True}
                                elif any(keyword in func.lower() for keyword in ['report', 'compliance', 'audit']):
                                    features[func] = {'tier': 3, 'type': 'compliance', 'auto_detected': True}
                                elif any(keyword in func.lower() for keyword in ['ai', 'smart', 'auto', 'goal']):
                                    features[func] = {'tier': 4, 'type': 'ai', 'auto_detected': True}
                except:
                    pass
        
        # Merge with known features
        features.update(known_features)
        
        # Store in database
        conn = self.get_db_connection()
        cursor = conn.cursor()
        for feature_name, feature_data in features.items():
            cursor.execute("""
            INSERT OR REPLACE INTO system_features 
            (feature_name, feature_type, tier, discovered_date, training_created) 
            VALUES (?, ?, ?, ?, ?)
            """, (feature_name, feature_data.get('type', 'unknown'), 
                  feature_data.get('tier', 1), datetime.now().isoformat(), False))
        
        conn.commit()
        conn.close()
        return features
    
    def extract_process_flows(self):
        """Extract business process flows from the system"""
        process_flows = {
            'load_to_payment': {
                'name': 'Load to Payment Process',
                'steps': [
                    {'step': 1, 'action': 'Find/Book Load', 'role': 'dispatcher', 'tier': 1},
                    {'step': 2, 'action': 'Assign Driver', 'role': 'dispatcher', 'tier': 1},
                    {'step': 3, 'action': 'Upload Rate Confirmation', 'role': 'dispatcher', 'tier': 1},
                    {'step': 4, 'action': 'Pick Up Load', 'role': 'driver', 'tier': 1},
                    {'step': 5, 'action': 'Upload BOL', 'role': 'driver', 'tier': 1},
                    {'step': 6, 'action': 'Deliver Load', 'role': 'driver', 'tier': 1},
                    {'step': 7, 'action': 'Upload POD', 'role': 'driver', 'tier': 1},
                    {'step': 8, 'action': 'Generate Invoice', 'role': 'accounting', 'tier': 2},
                    {'step': 9, 'action': 'Submit to Factoring', 'role': 'accounting', 'tier': 2},
                    {'step': 10, 'action': 'Receive Payment', 'role': 'accounting', 'tier': 2}
                ],
                'critical_points': ['BOL must be signed', 'POD required for payment', '11 AM cutoff for factoring']
            },
            'driver_onboarding': {
                'name': 'Driver Onboarding Process',
                'steps': [
                    {'step': 1, 'action': 'Create Driver Profile', 'role': 'admin', 'tier': 1},
                    {'step': 2, 'action': 'Upload CDL & Medical', 'role': 'safety', 'tier': 3},
                    {'step': 3, 'action': 'Complete Safety Training', 'role': 'driver', 'tier': 3},
                    {'step': 4, 'action': 'ELD Setup', 'role': 'admin', 'tier': 1},
                    {'step': 5, 'action': 'First Load Assignment', 'role': 'dispatcher', 'tier': 1}
                ]
            },
            'goal_adjustment': {
                'name': 'Dynamic Goal Adjustment Process',
                'steps': [
                    {'step': 1, 'action': 'AI Analyzes Performance', 'role': 'system', 'tier': 4},
                    {'step': 2, 'action': 'Generate Recommendations', 'role': 'system', 'tier': 4},
                    {'step': 3, 'action': 'CEO Reviews', 'role': 'ceo', 'tier': 4},
                    {'step': 4, 'action': 'Approve/Modify Goals', 'role': 'ceo', 'tier': 4},
                    {'step': 5, 'action': 'System Updates All Modules', 'role': 'system', 'tier': 4}
                ]
            }
        }
        
        # Store process flows in database
        conn = self.get_db_connection()
        cursor = conn.cursor()
        for flow_key, flow_data in process_flows.items():
            steps_json = json.dumps(flow_data['steps'])
            roles = list(set([s['role'] for s in flow_data['steps']]))
            
            cursor.execute("""
            INSERT OR REPLACE INTO process_flows 
            (process_name, steps, roles_involved, tier) 
            VALUES (?, ?, ?, ?)
            """, (flow_data['name'], steps_json, json.dumps(roles), 1))
        
        conn.commit()
        conn.close()
        return process_flows
    
    def generate_role_specific_training(self, role):
        """Generate training specific to a role"""
        if role not in self.roles:
            return None
            
        role_data = self.roles[role]
        training_modules = []
        
        # Core modules for the role
        base_modules = {
            'orientation': f"{role_data['name']} Orientation",
            'dashboard': f"Understanding Your {role_data['name']} Dashboard",
            'daily_tasks': f"Daily Tasks for {role_data['name']}",
            'features': f"Key Features for {role_data['name']}",
            'best_practices': f"Best Practices for {role_data['name']}"
        }
        
        # Add tier-specific training
        for tier in role_data['tiers']:
            tier_module = {
                'name': f"Tier {tier} Operations for {role_data['name']}",
                'content': self.generate_tier_training(tier, role),
                'interactive': True
            }
            training_modules.append(tier_module)
        
        # Add feature-specific training
        for feature in role_data['priority_features']:
            if feature in self.features:
                feature_module = {
                    'name': f"Mastering {feature.replace('_', ' ').title()}",
                    'content': self.generate_feature_training(feature, role),
                    'interactive': True
                }
                training_modules.append(feature_module)
        
        # Add process flow training
        relevant_processes = self.get_relevant_processes(role)
        for process in relevant_processes:
            process_module = {
                'name': f"Process: {process['name']}",
                'content': self.generate_process_training(process, role),
                'interactive': True
            }
            training_modules.append(process_module)
        
        # Store in database
        conn = self.get_db_connection()
        cursor = conn.cursor()
        for module in training_modules:
            cursor.execute("""
            INSERT OR REPLACE INTO training_modules 
            (module_name, module_type, target_role, content, created_date, auto_generated) 
            VALUES (?, ?, ?, ?, ?, ?)
            """, (module['name'], 'role_specific', role, 
                  json.dumps(module.get('content', {})), 
                  datetime.now().isoformat(), True))
        
        conn.commit()
        conn.close()
        return training_modules
    
    def generate_tier_training(self, tier, role):
        """Generate tier-specific training content"""
        tier_training = {
            1: {
                'title': 'Operational Command Center',
                'topics': [
                    'Load booking and prioritization',
                    'Driver-truck assignment',
                    'Document management',
                    'Real-time tracking'
                ],
                'exercises': [
                    'Book a contract load',
                    'Assign driver to load',
                    'Upload and verify documents'
                ]
            },
            2: {
                'title': 'Financial Management',
                'topics': [
                    'Invoice generation',
                    'Payment tracking',
                    'Factoring process',
                    'Cost analysis'
                ],
                'exercises': [
                    'Generate an invoice',
                    'Submit to factoring',
                    'Track payment status'
                ]
            },
            3: {
                'title': 'Compliance & Reporting',
                'topics': [
                    'DOT compliance',
                    'Safety metrics',
                    'Executive reports',
                    'Audit trails'
                ],
                'exercises': [
                    'Run compliance report',
                    'Review safety scores',
                    'Generate P&L report'
                ]
            },
            4: {
                'title': 'AI & Automation',
                'topics': [
                    'Goal management',
                    'Smart load finding',
                    'Performance optimization',
                    'Predictive analytics'
                ],
                'exercises': [
                    'Set profit goals',
                    'Review AI recommendations',
                    'Adjust automation rules'
                ]
            }
        }
        
        return tier_training.get(tier, {})
    
    def generate_feature_training(self, feature, role):
        """Generate feature-specific training"""
        # This would be expanded with actual feature documentation
        return {
            'overview': f"Understanding {feature}",
            'steps': f"How to use {feature}",
            'tips': f"Best practices for {feature}",
            'troubleshooting': f"Common issues with {feature}"
        }
    
    def generate_process_training(self, process, role):
        """Generate process flow training"""
        return {
            'overview': process.get('name', 'Process'),
            'your_role': f"Your responsibilities in this process",
            'steps': process.get('steps', []),
            'critical_points': process.get('critical_points', [])
        }
    
    def get_relevant_processes(self, role):
        """Get processes relevant to a specific role"""
        relevant = []
        for process_key, process_data in self.process_flows.items():
            roles_in_process = [s['role'] for s in process_data['steps']]
            if role in roles_in_process:
                relevant.append(process_data)
        return relevant
    
    def detect_system_changes(self):
        """Monitor system for changes and create new training"""
        changes = []
        
        # Check file modification times
        for file_path in self.system_files:
            if os.path.exists(file_path):
                mod_time = os.path.getmtime(file_path)
                last_check = st.session_state.get('last_check', 0)
                
                if mod_time > last_check:
                    changes.append({
                        'file': file_path,
                        'type': 'modified',
                        'time': datetime.fromtimestamp(mod_time)
                    })
        
        # If changes detected, rescan features
        if changes:
            new_features = self.scan_system_features()
            new_roles = self.detect_system_roles()
            
            # Generate training for new features
            for feature in new_features:
                if feature not in st.session_state.get('known_features', []):
                    self.create_feature_training(feature)
            
            # Generate training for new roles
            for role in new_roles:
                if role not in st.session_state.get('known_roles', []):
                    self.generate_role_specific_training(role)
        
        st.session_state['last_check'] = time.time()
        return changes
    
    def create_feature_training(self, feature):
        """Create training for a new feature"""
        training_content = {
            'title': f"New Feature: {feature.replace('_', ' ').title()}",
            'description': f"Learn how to use the new {feature} feature",
            'modules': [
                {
                    'name': 'Introduction',
                    'content': f"Overview of {feature}",
                    'duration': 5
                },
                {
                    'name': 'How to Use',
                    'content': f"Step-by-step guide for {feature}",
                    'duration': 10
                },
                {
                    'name': 'Best Practices',
                    'content': f"Tips for using {feature} effectively",
                    'duration': 5
                }
            ],
            'quiz': self.generate_quiz(feature),
            'created': datetime.now().isoformat()
        }
        
        # Store in database
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO training_modules 
        (module_name, module_type, content, created_date, auto_generated) 
        VALUES (?, ?, ?, ?, ?)
        """, (f"Feature: {feature}", 'feature', json.dumps(training_content), 
              datetime.now().isoformat(), True))
        
        conn.commit()
        conn.close()
        return training_content
    
    def generate_quiz(self, topic):
        """Generate quiz questions for a topic"""
        # This would be enhanced with AI to generate relevant questions
        return [
            {
                'question': f"What is the primary purpose of {topic}?",
                'options': ['Option A', 'Option B', 'Option C', 'Option D'],
                'correct': 0
            },
            {
                'question': f"When should you use {topic}?",
                'options': ['Scenario A', 'Scenario B', 'Scenario C', 'Scenario D'],
                'correct': 1
            }
        ]
    
    def track_user_progress(self, username, module_id, score, time_spent):
        """Track user progress through training"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO user_progress 
        (username, module_id, completed_date, score, time_spent) 
        VALUES (?, ?, ?, ?, ?)
        """, (username, module_id, datetime.now().isoformat(), score, time_spent))
        
        conn.commit()
        conn.close()
    
    def get_personalized_recommendations(self, username, role):
        """Get personalized training recommendations"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Get completed modules
        cursor.execute("""
        SELECT module_id FROM user_progress 
        WHERE username = ? AND score >= 80
        """, (username,))
        completed = [row[0] for row in cursor.fetchall()]
        
        # Get all modules for role
        cursor.execute("""
        SELECT id, module_name FROM training_modules 
        WHERE target_role = ? OR target_role = 'all'
        """, (role,))
        all_modules = cursor.fetchall()
        
        # Recommend uncompleted modules
        recommendations = []
        for module_id, module_name in all_modules:
            if module_id not in completed:
                recommendations.append({
                    'id': module_id,
                    'name': module_name,
                    'priority': 'high' if 'orientation' in module_name.lower() else 'medium'
                })
        
        return recommendations
    
    def generate_analytics_dashboard(self):
        """Generate training analytics"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Get completion rates
        cursor.execute("""
        SELECT 
            tm.module_name,
            COUNT(DISTINCT up.username) as completions,
            AVG(up.score) as avg_score,
            AVG(up.time_spent) as avg_time
        FROM training_modules tm
        LEFT JOIN user_progress up ON tm.id = up.module_id
        GROUP BY tm.id
        """)
        
        analytics = cursor.fetchall()
        return analytics

# ===================================================================
# MAIN TRAINING INTERFACE
# ===================================================================

def main():
    # Initialize session state
    if 'training_engine' not in st.session_state:
        st.session_state.training_engine = DynamicTrainingEngine()
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = 'Brandon'
        st.session_state.current_role = 'ceo'
    
    if 'training_start_time' not in st.session_state:
        st.session_state.training_start_time = time.time()
    
    if 'zelma_greeted' not in st.session_state:
        st.session_state.zelma_greeted = False
    
    engine = st.session_state.training_engine
    
    # Check for system changes
    changes = engine.detect_system_changes()
    if changes:
        st.info(f"📢 Zelma: System updates detected! I've created new training content for you.")
    
    # Add custom top bar with logo
    import os
    import base64
    
    # Load logo for top bar
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logos", "swt_logo_white.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            # Add custom div for top bar with logo
            st.markdown(f"""
            <div style="position: fixed; top: 0; left: 0; right: 0; height: 70px; background-color: #8B0000; 
                        display: flex; align-items: center; justify-content: center; z-index: 999999; 
                        border-bottom: 3px solid #660000;">
                <img src="data:image/png;base64,{logo_data}" style="height: 50px; margin-right: 20px;">
                <span style="color: white; font-size: 28px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px;">
                    SMITH & WILLIAMS TRUCKING
                </span>
            </div>
            """, unsafe_allow_html=True)
    
    # Main header section
    st.markdown("""
    <div style="background-color: #8B0000; padding: 20px; margin: -60px -50px 20px -50px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid #660000;">
        <div style="display: flex; align-items: center;">
            <div>
                <h1 style="color: white; margin: 0; padding: 0; font-size: 36px;">Training Center</h1>
                <p style="color: #ffcccc; margin: 0; font-size: 14px;">AI-Powered Adaptive Learning for Smith & Williams Trucking TMS</p>
            </div>
        </div>
        <div style="text-align: right;">
            <h3 style="color: white; margin: 0; font-size: 20px;">Powered by Zelma AI</h3>
            <p style="color: #ffcccc; margin: 0; font-size: 12px;">Your Training Specialist from Chicago</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Zelma's greeting
    if not st.session_state.zelma_greeted:
        st.success(f"""
        👋 **Welcome {st.session_state.current_user}! I'm Zelma, your AI training specialist from Chicago.**
        
        I've analyzed your role as {engine.roles[st.session_state.current_role]['name']} and created a personalized learning path tailored to your needs. 
        With my Chicago work ethic and teaching expertise, we'll have you mastering this TMS system efficiently. Let's get started!
        """)
        st.session_state.zelma_greeted = True
    
    # Sidebar with S&W branding
    with st.sidebar:
        # Add actual S&W logo to sidebar (white version)
        logo_sidebar = os.path.join(os.path.dirname(__file__), "assets", "logos", "swt_logo_white.png")
        if os.path.exists(logo_sidebar):
            st.image(logo_sidebar, use_container_width=True)
            st.markdown("---")
        st.markdown("## 🏫 Training Center")
        st.markdown("### Smith & Williams Trucking")
        st.caption("*Professional Development with Zelma*")
        
        # User selection with Zelma's guidance
        user_role = st.selectbox(
            "Select Your Role",
            options=list(engine.roles.keys()),
            format_func=lambda x: engine.roles[x]['name'],
            help="Zelma says: Tell me your role so I can customize your training!"
        )
        
        st.session_state.current_role = user_role
        
        # Training mode with Zelma's recommendations
        st.markdown("### 📚 Choose Your Path")
        training_mode = st.radio(
            "What would you like to learn today?",
            ["Guided Learning", "Role-Specific Path", "Process Training", 
             "Feature Discovery", "Quick Reference", "Analytics"],
            help="Zelma recommends: Start with Guided Learning if you're new!"
        )
        
        st.markdown("---")
        
        # Progress overview with Zelma's encouragement
        st.markdown("### 🌟 Your Progress")
        st.caption("*Smith & Williams Progress Tracking*")
        recommendations = engine.get_personalized_recommendations(
            st.session_state.current_user, 
            user_role
        )
        
        total_modules = len(recommendations) + 10  # Including completed
        completed = 10  # Example
        progress = completed / total_modules if total_modules > 0 else 0
        
        st.progress(progress)
        st.metric("Modules Completed", f"{completed}/{total_modules}")
        
        # Recommendations
        if recommendations:
            st.markdown("### 💡 Zelma's Recommendations")
            st.caption("*Personalized for Smith & Williams Excellence*")
            for rec in recommendations[:3]:
                if st.button(f"📚 {rec['name'][:30]}...", key=f"rec_{rec['id']}"):
                    st.session_state.selected_module = rec['id']
    
    # Main content area
    if training_mode == "Guided Learning":
        show_guided_learning(engine)
    elif training_mode == "Role-Specific Path":
        show_role_specific_path(engine, user_role)
    elif training_mode == "Process Training":
        show_process_training(engine, user_role)
    elif training_mode == "Feature Discovery":
        show_feature_discovery(engine)
    elif training_mode == "Quick Reference":
        show_quick_reference(engine, user_role)
    elif training_mode == "Analytics":
        show_analytics(engine)

def show_guided_learning(engine):
    """Show guided learning interface with Zelma's guidance"""
    st.header("🎯 Zelma's Guided Learning Path")
    st.info("👩‍🏫 **Zelma says:** Welcome honey! I've prepared everything you need to succeed. Let's take this one step at a time, and before you know it, you'll be a TMS expert!")
    
    tabs = st.tabs(["Start Here", "Core Concepts", "Advanced Topics", "Certification"])
    
    with tabs[0]:  # Start Here
        st.subheader("Welcome to Intelligent Training")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container():
                st.markdown("### 🚀 Quick Start")
                st.info("""
                **15-Minute Orientation with Zelma**
                - Let me show you around the system
                - I'll explain your role clearly
                - We'll tour the key features together
                - Practice your first task with me
                """)
                if st.button("Start Orientation", type="primary"):
                    start_orientation(engine)
        
        with col2:
            with st.container():
                st.markdown("### 📋 Your Learning Path")
                role = st.session_state.current_role
                role_data = engine.roles[role]
                
                st.success(f"""
                **{role_data['name']} Track**
                - {len(role_data['priority_features'])} core features
                - {len(role_data['tiers'])} tier access
                - {len(engine.get_relevant_processes(role))} processes
                """)
                
                if st.button("View Full Path"):
                    st.session_state.show_path = True
        
        with col3:
            with st.container():
                st.markdown("### 🎓 Certification")
                st.warning("""
                **Get Certified**
                - Complete all modules
                - Pass assessments
                - Earn certificate
                - Track progress
                """)
                if st.button("View Requirements"):
                    show_certification_requirements(engine)
    
    with tabs[1]:  # Core Concepts
        show_core_concepts(engine)
    
    with tabs[2]:  # Advanced Topics
        show_advanced_topics(engine)
    
    with tabs[3]:  # Certification
        show_certification(engine)

def show_role_specific_path(engine, role):
    """Show role-specific training path with Zelma"""
    st.header(f"🎭 {engine.roles[role]['name']} Training Path")
    st.success(f"👩‍🏫 **Zelma says:** Alright {st.session_state.current_user}, I've customized this training just for you as a {engine.roles[role]['name']}. We're going to make sure you know everything you need to excel in your role!")
    
    # Generate role-specific training if not exists
    training_modules = engine.generate_role_specific_training(role)
    
    # Progress tracker
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Modules", len(training_modules))
    with col2:
        st.metric("Completed", "0")
    with col3:
        st.metric("In Progress", "1")
    with col4:
        st.metric("Time Invested", "0h 0m")
    
    st.markdown("---")
    
    # Training modules
    st.subheader("Your Training Modules")
    
    # Group by category
    categories = {
        'Foundation': [],
        'Core Skills': [],
        'Process Mastery': [],
        'Advanced Features': []
    }
    
    for module in training_modules:
        if 'orientation' in module['name'].lower() or 'dashboard' in module['name'].lower():
            categories['Foundation'].append(module)
        elif 'process' in module['name'].lower():
            categories['Process Mastery'].append(module)
        elif 'tier' in module['name'].lower():
            categories['Core Skills'].append(module)
        else:
            categories['Advanced Features'].append(module)
    
    for category, modules in categories.items():
        if modules:
            with st.expander(f"{category} ({len(modules)} modules)", expanded=True):
                for i, module in enumerate(modules):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        if st.button(f"📖 {module['name']}", key=f"mod_{category}_{i}"):
                            show_module_content(engine, module)
                    
                    with col2:
                        st.markdown("⏱️ 15 min")
                    
                    with col3:
                        st.markdown("🔄 Not Started")

def show_process_training(engine, role):
    """Show process flow training with Zelma"""
    st.header("🔄 Process Flow Training")
    st.info("👩‍🏫 **Zelma says:** Now honey, understanding these processes is crucial. I'm going to walk you through each step, and we'll practice until you're comfortable. Don't worry, I'll be right here with you!")
    
    relevant_processes = engine.get_relevant_processes(role)
    
    if not relevant_processes:
        st.warning("No processes found for your role.")
        return
    
    # Process selector
    process_names = [p['name'] for p in relevant_processes]
    selected_process = st.selectbox("Select Process to Learn", process_names)
    
    # Find selected process
    process = next((p for p in relevant_processes if p['name'] == selected_process), None)
    
    if process:
        st.subheader(f"Process: {process['name']}")
        
        # Interactive process flow
        st.markdown("### Interactive Process Flow")
        
        # Create flowchart
        fig = go.Figure()
        
        # Add nodes for each step
        for i, step in enumerate(process['steps']):
            # Determine if this step involves current role
            is_my_step = step['role'] == role
            
            fig.add_trace(go.Scatter(
                x=[i],
                y=[step['tier']],
                mode='markers+text',
                marker=dict(
                    size=40,
                    color='red' if is_my_step else 'gray',
                    line=dict(width=2, color='darkred' if is_my_step else 'darkgray')
                ),
                text=f"Step {step['step']}<br>{step['action']}<br>({step['role']})",
                textposition="bottom center",
                hovertemplate=f"<b>{step['action']}</b><br>Role: {step['role']}<br>Tier: {step['tier']}<extra></extra>"
            ))
        
        # Add arrows between steps
        for i in range(len(process['steps']) - 1):
            fig.add_annotation(
                x=i,
                y=process['steps'][i]['tier'],
                ax=i+1,
                ay=process['steps'][i+1]['tier'],
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="black"
            )
        
        fig.update_layout(
            title=f"{process['name']} - Your Role: {engine.roles[role]['name']}",
            showlegend=False,
            height=400,
            xaxis_title="Process Steps",
            yaxis_title="System Tier",
            yaxis=dict(range=[0.5, 4.5], dtick=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Step details
        st.markdown("### Your Responsibilities in This Process")
        
        your_steps = [s for s in process['steps'] if s['role'] == role]
        
        if your_steps:
            for step in your_steps:
                with st.expander(f"Step {step['step']}: {step['action']}", expanded=True):
                    st.markdown(f"""
                    **Your Action:** {step['action']}
                    
                    **When:** After step {step['step']-1 if step['step'] > 1 else 'Process Start'}
                    
                    **System Tier:** Tier {step['tier']}
                    
                    **Key Points:**
                    - Complete this action promptly
                    - Ensure accuracy before proceeding
                    - Notify next role when complete
                    
                    **Common Issues:**
                    - Missing information
                    - System access problems
                    - Communication gaps
                    """)
                    
                    if st.button(f"Practice Step {step['step']}", key=f"practice_{step['step']}"):
                        practice_step(engine, step)
        else:
            st.info("You don't have direct responsibilities in this process, but understanding it helps coordination.")
        
        # Critical points
        if 'critical_points' in process:
            st.warning("⚠️ **Critical Points**")
            for point in process['critical_points']:
                st.write(f"• {point}")

def show_feature_discovery(engine):
    """Show newly discovered features with Zelma"""
    st.header("🔍 Zelma's Feature Discovery")
    
    # Scan for new features
    st.info("👩‍🏫 **Zelma:** Let me check what's new in the system for you... I'm always keeping an eye out for updates!")
    features = engine.scan_system_features()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Features", len(features))
    with col2:
        auto_detected = sum(1 for f in features.values() if f.get('auto_detected'))
        st.metric("Auto-Detected", auto_detected)
    with col3:
        st.metric("Training Created", len(features))
    
    st.markdown("---")
    
    # Feature categories
    tabs = st.tabs(["Tier 1 - Operational", "Tier 2 - Financial", 
                    "Tier 3 - Compliance", "Tier 4 - AI/Automation", "New Features"])
    
    for i, tier in enumerate([1, 2, 3, 4]):
        with tabs[i]:
            tier_features = {k: v for k, v in features.items() if v.get('tier') == tier}
            
            if tier_features:
                for feature_name, feature_data in tier_features.items():
                    with st.expander(f"📦 {feature_name.replace('_', ' ').title()}", 
                                   expanded=feature_data.get('auto_detected', False)):
                        
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"""
                            **Type:** {feature_data.get('type', 'Unknown')}
                            
                            **Status:** {'🆕 Auto-Detected' if feature_data.get('auto_detected') else '✅ Known Feature'}
                            
                            **Description:** Learn how to use {feature_name.replace('_', ' ')} effectively.
                            """)
                        
                        with col2:
                            if st.button(f"Start Training", key=f"train_{feature_name}"):
                                training = engine.create_feature_training(feature_name)
                                st.success(f"Training created for {feature_name}!")
                                show_feature_training(engine, feature_name, training)
    
    with tabs[4]:  # New Features
        st.subheader("Recently Discovered Features")
        
        # Get features discovered in last 7 days
        conn = engine.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT feature_name, feature_type, tier, discovered_date 
        FROM system_features 
        WHERE datetime(discovered_date) > datetime('now', '-7 days')
        ORDER BY discovered_date DESC
        """)
        
        recent_features = cursor.fetchall()
        conn.close()
        
        if recent_features:
            for feature in recent_features:
                st.success(f"""
                🆕 **{feature[0].replace('_', ' ').title()}**
                - Type: {feature[1]}
                - Tier: {feature[2]}
                - Discovered: {feature[3][:10]}
                """)
        else:
            st.info("No new features discovered in the last 7 days.")

def show_quick_reference(engine, role):
    """Show quick reference guide with Zelma"""
    st.header("📚 Zelma's Quick Reference Guide")
    st.success("👩‍🏫 **Zelma says:** Need a quick answer? I've got you covered! Just type what you're looking for, or click one of the quick buttons below.")
    
    # Search
    search_term = st.text_input("🔍 Search for help...", placeholder="Type a keyword or question")
    
    # Quick access buttons
    st.markdown("### Quick Access")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Common Tasks", use_container_width=True):
            show_common_tasks(engine, role)
    
    with col2:
        if st.button("❓ FAQs", use_container_width=True):
            show_faqs(engine, role)
    
    with col3:
        if st.button("⚠️ Troubleshooting", use_container_width=True):
            show_troubleshooting(engine)
    
    with col4:
        if st.button("📊 Reports Guide", use_container_width=True):
            show_reports_guide(engine, role)
    
    st.markdown("---")
    
    # Role-specific quick guides
    st.subheader(f"Quick Guides for {engine.roles[role]['name']}")
    
    role_guides = {
        'ceo': {
            'Goal Management': "Set profit targets, review AI suggestions, approve changes",
            'User Management': "Create users, assign roles, manage permissions",
            'Executive Reports': "P&L, fleet utilization, driver performance",
            'Driver Mode': "Switch to driver view when operating a truck"
        },
        'dispatcher': {
            'Load Booking': "Find loads, negotiate rates, confirm bookings",
            'Driver Assignment': "Match drivers to loads, check availability",
            'Document Upload': "Rate confirmations, load details",
            'Load Tracking': "Monitor pickup/delivery, update statuses"
        },
        'driver': {
            'View Loads': "See assigned loads, get directions",
            'Upload Documents': "BOL at pickup, POD at delivery",
            'Update Status': "Mark arrival, loading, in transit, delivered",
            'HOS Tracking': "Monitor hours of service, take breaks"
        },
        'accounting': {
            'Invoice Generation': "Create invoices from completed loads",
            'Factoring': "Submit invoices by 11 AM for next-day payment",
            'Payment Tracking': "Record payments, update status",
            'Reports': "Revenue reports, aging, collections"
        }
    }
    
    guides = role_guides.get(role, {})
    
    for guide_title, guide_content in guides.items():
        with st.expander(f"📖 {guide_title}"):
            st.write(guide_content)
            if st.button(f"Learn More: {guide_title}", key=f"guide_{guide_title}"):
                show_detailed_guide(engine, guide_title, role)

def show_analytics(engine):
    """Show training analytics dashboard with Zelma"""
    st.header("📊 Zelma's Progress Report")
    st.info("👩‍🏫 **Zelma says:** Let's see how you're doing! I'm so proud of your progress. Remember, everyone learns at their own pace, and you're doing great!")
    
    # Get analytics data
    analytics = engine.generate_analytics_dashboard()
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users Trained", "12")
    with col2:
        st.metric("Avg Completion Rate", "78%")
    with col3:
        st.metric("Avg Score", "85%")
    with col4:
        st.metric("Training Hours", "156")
    
    st.markdown("---")
    
    # Detailed analytics
    tabs = st.tabs(["Module Performance", "User Progress", "Role Analytics", "Effectiveness"])
    
    with tabs[0]:  # Module Performance
        st.subheader("Module Performance Metrics")
        
        if analytics:
            # Create dataframe
            df = pd.DataFrame(analytics, columns=['Module', 'Completions', 'Avg Score', 'Avg Time'])
            df['Avg Time'] = df['Avg Time'].fillna(0).astype(int)
            df['Avg Score'] = df['Avg Score'].fillna(0).round(1)
            
            # Display chart
            fig = px.bar(df, x='Module', y='Completions', 
                        hover_data=['Avg Score', 'Avg Time'],
                        title='Module Completion Rates')
            st.plotly_chart(fig, use_container_width=True)
            
            # Display table
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tabs[1]:  # User Progress
        st.subheader("Individual User Progress")
        
        # Sample data
        users_data = {
            'User': ['Brandon', 'Driver1', 'Driver2', 'Dispatcher1'],
            'Role': ['CEO', 'Driver', 'Driver', 'Dispatcher'],
            'Modules Completed': [15, 8, 6, 10],
            'Avg Score': [92, 85, 78, 88],
            'Last Active': ['Today', 'Yesterday', '3 days ago', 'Today']
        }
        
        df_users = pd.DataFrame(users_data)
        st.dataframe(df_users, use_container_width=True, hide_index=True)
    
    with tabs[2]:  # Role Analytics
        st.subheader("Training by Role")
        
        role_data = {
            'Role': list(engine.roles.keys()),
            'Users': [5, 3, 8, 4, 2, 1],
            'Avg Completion': [85, 90, 75, 80, 70, 60],
            'Training Hours': [45, 30, 60, 35, 20, 10]
        }
        
        df_roles = pd.DataFrame(role_data)
        
        fig = px.scatter(df_roles, x='Training Hours', y='Avg Completion', 
                        size='Users', color='Role',
                        title='Role Training Effectiveness')
        st.plotly_chart(fig, use_container_width=True)
    
    with tabs[3]:  # Effectiveness
        st.subheader("Training Effectiveness")
        
        st.markdown("""
        ### Key Insights
        
        1. **Most Effective Modules:**
           - Quick Start Orientation (95% satisfaction)
           - Process Flow Training (92% satisfaction)
           - Role-Specific Paths (88% satisfaction)
        
        2. **Areas for Improvement:**
           - Advanced AI Features (needs simplification)
           - Compliance Training (add more examples)
           - Integration Training (more hands-on practice)
        
        3. **Recommendations:**
           - Add more interactive scenarios
           - Create video tutorials for complex features
           - Implement peer mentoring program
        """)

# ===================================================================
# HELPER FUNCTIONS
# ===================================================================

def start_orientation(engine):
    """Start the orientation process with Zelma"""
    with st.container():
        st.markdown("### 🎯 Zelma's 15-Minute Quick Start")
        st.info("👩‍🏫 **Zelma:** Alright sweetheart, let's get you comfortable with the system. We'll take this nice and easy, and I'll be here every step of the way.")
        
        # Progress bar
        progress = st.progress(0)
        
        # Step 1
        with st.expander("Step 1: Understanding Your Role", expanded=True):
            role = st.session_state.current_role
            role_data = engine.roles[role]
            
            st.info(f"""
            **You are: {role_data['name']}**
            
            **Your Access:**
            - Tiers: {', '.join([f"Tier {t}" for t in role_data['tiers']])}
            - Permissions: {role_data['permissions']}
            {"- Dual Mode: Executive + Driver" if role_data.get('dual_mode') else ""}
            
            **Your Key Features:**
            {chr(10).join([f"• {f.replace('_', ' ').title()}" for f in role_data['priority_features']])}
            """)
            
            if st.button("Next →", key="orient_1"):
                progress.progress(33)
        
        # Step 2
        with st.expander("Step 2: Your First Task", expanded=False):
            st.success("""
            **Let's practice your most common task:**
            
            1. Log into the system
            2. Navigate to your dashboard
            3. Complete a simple action
            4. Verify the result
            """)
            
            if st.button("Practice Now", key="orient_2"):
                progress.progress(66)
        
        # Step 3
        with st.expander("Step 3: Getting Help", expanded=False):
            st.warning("""
            **Where to get help:**
            
            • **Quick Reference:** Press F1 anytime
            • **Process Guide:** Available in sidebar
            • **Video Tutorials:** In Help menu
            • **Support:** support@swtrucking.com
            """)
            
            if st.button("Complete Orientation ✓", key="orient_3"):
                progress.progress(100)
                st.balloons()
                engine.track_user_progress(
                    st.session_state.current_user, 
                    1,  # Orientation module ID
                    100,  # Score
                    15  # Time in minutes
                )

def show_module_content(engine, module):
    """Display module content"""
    with st.container():
        st.subheader(f"📚 {module['name']}")
        
        # Module content
        if 'content' in module:
            content = module['content']
            if isinstance(content, dict):
                for section, text in content.items():
                    st.markdown(f"**{section.replace('_', ' ').title()}**")
                    st.write(text)
            else:
                st.write(content)
        
        # Interactive elements
        if module.get('interactive'):
            with st.expander("Try It Yourself"):
                st.info("Interactive exercise would go here")
                if st.button("Complete Exercise"):
                    st.success("Exercise completed!")

def practice_step(engine, step):
    """Practice a specific process step"""
    st.info(f"Practicing: {step['action']}")
    # Implementation would include actual practice scenarios

def show_feature_training(engine, feature_name, training):
    """Show training for a specific feature"""
    st.subheader(f"Training: {feature_name.replace('_', ' ').title()}")
    st.json(training)

def show_certification_requirements(engine):
    """Show certification requirements"""
    st.info("""
    **Certification Requirements:**
    - Complete all required modules
    - Pass all assessments with 80% or higher
    - Complete practical exercises
    - Demonstrate proficiency in key tasks
    """)

def show_core_concepts(engine):
    """Show core concepts training"""
    st.subheader("Core Concepts")
    st.info("Core system concepts and fundamentals")

def show_advanced_topics(engine):
    """Show advanced topics"""
    st.subheader("Advanced Topics")
    st.info("Advanced features and optimization techniques")

def show_certification(engine):
    """Show certification path"""
    st.subheader("Certification Program")
    st.info("Complete your certification to become a TMS expert")

def show_common_tasks(engine, role):
    """Show common tasks for role"""
    st.info(f"Common tasks for {engine.roles[role]['name']}")

def show_faqs(engine, role):
    """Show FAQs"""
    st.info("Frequently Asked Questions")

def show_troubleshooting(engine):
    """Show troubleshooting guide"""
    st.info("Troubleshooting common issues")

def show_reports_guide(engine, role):
    """Show reports guide"""
    st.info(f"Reports guide for {engine.roles[role]['name']}")

def show_detailed_guide(engine, guide_title, role):
    """Show detailed guide for a topic"""
    st.info(f"Detailed guide: {guide_title}")

# ===================================================================
# MAIN EXECUTION
# ===================================================================

if __name__ == "__main__":
    main()