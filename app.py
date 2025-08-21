"""
===================================================================
SMITH & WILLIAMS TRUCKING - TMS HUB
Main Application Entry Point
===================================================================
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from modules.auth import show_login, check_authentication
from modules.ui_components import apply_global_styles, show_sidebar
from views.user_management import show_user_management

# Import enhanced views
from views.executive_enhanced import show_executive_view
from views.data_feeder_enhanced import show_data_feeder_view  
from views.driver_enhanced import show_driver_view

# Import additional views
from views.comprehensive_management import show_comprehensive_management_view
from views.ceo_personal_management import show_personal_management_view
from views.intelligent_assistant import show_ai_assistant_view
from views.learning_center import show_learning_center_view
from views.broker_analysis import show_broker_analysis_view
from views.database_management import show_database_management_view

# Initialize enhanced database
from modules.database_enhanced import init_enhanced_database
init_enhanced_database()

# Page Configuration
st.set_page_config(
    page_title="TMS - Smith & Williams Trucking",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
apply_global_styles()

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login()
    else:
        # Show main interface based on user role
        show_main_interface()

def show_setup_status(view_name):
    """Display setup status for views not yet implemented"""
    
    # View configurations and requirements
    view_configs = {
        'ai_assistant': {
            'title': '🤖 AI Assistant (Intelligent Assistant)',
            'description': 'Conversational AI interface for TMS operations',
            'requirements': [
                '✅ View file exists (intelligent_assistant.py)',
                '❌ AI conversation interface not implemented',
                '❌ Integration with OpenAI API needed',
                '❌ Context-aware TMS responses needed',
                '❌ User session management needed'
            ],
            'features_needed': [
                'Conversational chat interface',
                'TMS-specific knowledge base',
                'Load planning assistance',
                'Route optimization suggestions',
                'Compliance guidance',
                'Real-time data integration'
            ]
        },
        'learning_center': {
            'title': '🎓 Learning Center',
            'description': 'Training and documentation system',
            'requirements': [
                '✅ View file exists (learning_center.py)',
                '❌ Training module structure not implemented',
                '❌ Video content integration needed',
                '❌ Progress tracking system needed',
                '❌ Quiz/assessment system needed'
            ],
            'features_needed': [
                'Training module categories',
                'Video player integration',
                'Interactive tutorials',
                'Progress tracking dashboard',
                'Certification system',
                'User-specific training paths'
            ]
        },
        'comprehensive_management': {
            'title': '🎛️ Management Center',
            'description': 'Unified business operations dashboard',
            'requirements': [
                '✅ View file exists (comprehensive_management.py)',
                '❌ Multi-function dashboard not implemented',
                '❌ Workflow management needed',
                '❌ Task assignment system needed',
                '❌ Performance metrics needed'
            ],
            'features_needed': [
                'Unified operations dashboard',
                'Workflow management system',
                'Task assignment and tracking',
                'Performance KPIs',
                'Resource allocation tools',
                'Strategic planning interface'
            ]
        },
        'personal_management': {
            'title': '👔 Personal Management (CEO)',
            'description': 'Executive personal productivity suite',
            'requirements': [
                '✅ View file exists (ceo_personal_management.py)',
                '❌ Personal dashboard not implemented',
                '❌ Calendar integration needed',
                '❌ Task management needed',
                '❌ Personal metrics needed'
            ],
            'features_needed': [
                'Personal productivity dashboard',
                'Calendar and scheduling',
                'Personal task management',
                'Executive metrics',
                'Document management',
                'Communication center'
            ]
        },
        'broker_analysis': {
            'title': '📊 Broker Analysis',
            'description': 'Freight broker performance analytics',
            'requirements': [
                '✅ View file exists (broker_analysis.py)',
                '❌ Broker performance metrics not implemented',
                '❌ Rate analysis system needed',
                '❌ Broker comparison tools needed',
                '❌ Market analysis needed'
            ],
            'features_needed': [
                'Broker performance dashboards',
                'Rate comparison tools',
                'Market trend analysis',
                'Broker scorecards',
                'Contract analysis',
                'Negotiation support tools'
            ]
        },
        'database_management': {
            'title': '🗄️ Database Management',
            'description': 'System database administration tools',
            'requirements': [
                '✅ View file exists (database_management.py)',
                '❌ Database admin interface not implemented',
                '❌ Backup/restore system needed',
                '❌ Data migration tools needed',
                '❌ Performance monitoring needed'
            ],
            'features_needed': [
                'Database administration panel',
                'Backup and restore functionality',
                'Data export/import tools',
                'Performance monitoring',
                'Query builder interface',
                'Data integrity checks'
            ]
        }
    }
    
    config = view_configs.get(view_name, {
        'title': f'🚧 {view_name.replace("_", " ").title()}',
        'description': 'View configuration not found',
        'requirements': ['❌ View configuration needed'],
        'features_needed': ['Configuration and implementation needed']
    })
    
    st.markdown(f"""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #1e293b, #475569); border-radius: 20px; margin: 20px 0;'>
        <h1 style='color: white; margin: 0;'>{config['title']}</h1>
        <h3 style='color: #94a3b8; margin: 20px 0;'>{config['description']}</h3>
        <p style='color: #fbbf24; font-size: 1.2em; font-weight: 600;'>🚧 VIEW SETUP IN PROGRESS 🚧</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Current Status")
        for req in config['requirements']:
            st.markdown(f"- {req}")
    
    with col2:
        st.markdown("### 🎯 Features Needed")
        for feature in config['features_needed']:
            st.markdown(f"- {feature}")
    
    st.markdown("---")
    st.info("💡 This view is being developed. Contact the development team for implementation timeline.")

def show_main_interface():
    """Display the main interface based on user role"""
    
    # Show sidebar
    show_sidebar()
    
    # Check if user management should be shown
    if st.session_state.get('show_user_management', False) and st.session_state.role == 'super_user':
        show_user_management()
        
        # Add back button
        if st.button("⬅️ Back to Main View"):
            st.session_state.show_user_management = False
            st.rerun()
    else:
        # Main content area based on selected view
        current_view = st.session_state.get('current_view', 'executive')
        
        if current_view == 'executive':
            show_executive_view()
        elif current_view == 'data_feeder':
            show_data_feeder_view()
        elif current_view == 'driver':
            show_driver_view()
        elif current_view == 'comprehensive_management':
            show_comprehensive_management_view()
        elif current_view == 'personal_management':
            show_personal_management_view()
        elif current_view == 'ai_assistant':
            show_ai_assistant_view()
        elif current_view == 'learning_center':
            show_learning_center_view()
        elif current_view == 'broker_analysis':
            show_broker_analysis_view()
        elif current_view == 'database_management':
            show_database_management_view()
        elif current_view == 'user_management':
            show_user_management()
        else:
            # Default fallback with setup status
            show_setup_status(current_view)
    
    # User Management button - Only for super_user
    if st.session_state.role == 'super_user':
        with st.sidebar:
            st.markdown("---")
            if st.button("👥 Manage Users", use_container_width=True):
                st.session_state.show_user_management = True
                st.rerun()

if __name__ == "__main__":
    main()