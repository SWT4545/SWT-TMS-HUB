"""
Learning Center & Intelligent System Updates
Self-learning and auto-updating capabilities for the TMS
"""
import streamlit as st
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
from config.database import get_connection
import json
import requests
import subprocess
import sys
import os
from pathlib import Path

class LearningCenter:
    """Intelligent learning and self-updating system"""
    
    def __init__(self):
        self.conn = get_connection()
        self.init_learning_tables()
        self.knowledge_base = self.load_knowledge_base()
        
    def init_learning_tables(self):
        """Initialize learning and update tracking tables"""
        cursor = self.conn.cursor()
        
        # System learning table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_learning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learning_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            module_name TEXT,
            action_type TEXT,
            user_action TEXT,
            ai_response TEXT,
            outcome TEXT,
            success_rate REAL,
            improvement_notes TEXT
        )''')
        
        # System updates table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            version TEXT,
            module_updated TEXT,
            update_type TEXT,
            changes_made TEXT,
            auto_update BOOLEAN DEFAULT 0,
            update_source TEXT,
            status TEXT DEFAULT 'Pending'
        )''')
        
        # Knowledge base table
        cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            topic TEXT,
            content TEXT,
            learned_from TEXT,
            confidence_score REAL,
            usage_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # User patterns table
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pattern_type TEXT,
            pattern_data TEXT,
            frequency INTEGER,
            last_occurrence TIMESTAMP,
            prediction_accuracy REAL
        )''')
        
        # System optimization table
        cursor.execute('''CREATE TABLE IF NOT EXISTS system_optimizations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            optimization_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            module_name TEXT,
            optimization_type TEXT,
            before_metrics TEXT,
            after_metrics TEXT,
            improvement_percentage REAL,
            auto_applied BOOLEAN DEFAULT 0
        )''')
        
        self.conn.commit()
    
    def load_knowledge_base(self):
        """Load and return the system's knowledge base"""
        try:
            df = pd.read_sql_query("""
                SELECT category, topic, content, confidence_score 
                FROM knowledge_base 
                ORDER BY confidence_score DESC, usage_count DESC
            """, self.conn)
            return df.to_dict('records')
        except:
            return []
    
    def learn_from_interaction(self, user_input, system_response, outcome='success'):
        """Learn from user interactions to improve system"""
        cursor = self.conn.cursor()
        
        # Record the interaction
        cursor.execute("""
            INSERT INTO system_learning 
            (module_name, action_type, user_action, ai_response, outcome)
            VALUES (?, ?, ?, ?, ?)
        """, ('AI Assistant', 'interaction', user_input, system_response, outcome))
        
        # Analyze patterns
        self.analyze_user_patterns(user_input)
        
        # Update knowledge base if successful
        if outcome == 'success':
            self.update_knowledge_base(user_input, system_response)
        
        self.conn.commit()
    
    def analyze_user_patterns(self, user_input):
        """Analyze and learn from user behavior patterns"""
        # Extract patterns from user input
        patterns = {
            'time_preference': self.extract_time_preference(user_input),
            'common_actions': self.extract_common_actions(user_input),
            'data_preferences': self.extract_data_preferences(user_input)
        }
        
        # Store patterns for future predictions
        cursor = self.conn.cursor()
        for pattern_type, pattern_data in patterns.items():
            if pattern_data:
                cursor.execute("""
                    INSERT OR REPLACE INTO user_patterns 
                    (user_id, pattern_type, pattern_data, frequency, last_occurrence)
                    VALUES (?, ?, ?, 
                            COALESCE((SELECT frequency + 1 FROM user_patterns 
                                     WHERE user_id = ? AND pattern_type = ?), 1),
                            CURRENT_TIMESTAMP)
                """, (1, pattern_type, json.dumps(pattern_data), 1, pattern_type))
        
        self.conn.commit()
    
    def extract_time_preference(self, text):
        """Extract time-based preferences from user input"""
        time_keywords = {
            'morning': ['morning', 'am', 'early'],
            'afternoon': ['afternoon', 'noon', 'pm'],
            'evening': ['evening', 'night', 'late'],
            'daily': ['daily', 'every day', 'each day'],
            'weekly': ['weekly', 'every week', 'each week'],
            'monthly': ['monthly', 'every month', 'each month']
        }
        
        preferences = []
        text_lower = text.lower()
        for pref, keywords in time_keywords.items():
            if any(kw in text_lower for kw in keywords):
                preferences.append(pref)
        
        return preferences if preferences else None
    
    def extract_common_actions(self, text):
        """Extract common action patterns"""
        actions = {
            'create': ['add', 'create', 'new', 'insert'],
            'read': ['show', 'display', 'view', 'list', 'get'],
            'update': ['update', 'edit', 'modify', 'change'],
            'delete': ['delete', 'remove', 'cancel'],
            'report': ['report', 'summary', 'analytics', 'stats']
        }
        
        found_actions = []
        text_lower = text.lower()
        for action, keywords in actions.items():
            if any(kw in text_lower for kw in keywords):
                found_actions.append(action)
        
        return found_actions if found_actions else None
    
    def extract_data_preferences(self, text):
        """Extract data preferences from user input"""
        # Identify what type of data the user commonly works with
        data_types = {
            'shipments': ['load', 'shipment', 'delivery', 'pickup'],
            'expenses': ['expense', 'cost', 'spent', 'paid'],
            'fleet': ['truck', 'trailer', 'vehicle', 'equipment'],
            'financial': ['revenue', 'profit', 'income', 'money'],
            'personal': ['personal', 'property', 'family', 'health']
        }
        
        preferences = []
        text_lower = text.lower()
        for dtype, keywords in data_types.items():
            if any(kw in text_lower for kw in keywords):
                preferences.append(dtype)
        
        return preferences if preferences else None
    
    def update_knowledge_base(self, topic, content):
        """Update the knowledge base with new information"""
        cursor = self.conn.cursor()
        
        # Check if similar knowledge exists
        cursor.execute("""
            SELECT id, usage_count, confidence_score 
            FROM knowledge_base 
            WHERE topic = ?
        """, (topic,))
        
        existing = cursor.fetchone()
        
        if existing:
            # Update existing knowledge
            cursor.execute("""
                UPDATE knowledge_base 
                SET content = ?, 
                    usage_count = usage_count + 1,
                    confidence_score = MIN(1.0, confidence_score + 0.1),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (content, existing[0]))
        else:
            # Add new knowledge
            cursor.execute("""
                INSERT INTO knowledge_base 
                (category, topic, content, learned_from, confidence_score)
                VALUES (?, ?, ?, 'user_interaction', 0.5)
            """, (self.categorize_knowledge(topic), topic, content))
        
        self.conn.commit()
    
    def categorize_knowledge(self, topic):
        """Categorize knowledge automatically"""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['load', 'shipment', 'delivery', 'dispatch']):
            return 'Operations'
        elif any(word in topic_lower for word in ['expense', 'cost', 'revenue', 'profit', 'payment']):
            return 'Financial'
        elif any(word in topic_lower for word in ['truck', 'trailer', 'vehicle', 'fleet']):
            return 'Fleet'
        elif any(word in topic_lower for word in ['driver', 'cdl', 'employee']):
            return 'Personnel'
        elif any(word in topic_lower for word in ['customer', 'client', 'shipper']):
            return 'Customers'
        elif any(word in topic_lower for word in ['personal', 'property', 'family', 'health']):
            return 'Personal'
        else:
            return 'General'
    
    def check_for_updates(self):
        """Check for system updates from GitHub"""
        try:
            # Check GitHub for updates
            response = requests.get(
                'https://api.github.com/repos/SWT4545/SWT-TMS-HUB/commits/main',
                timeout=5
            )
            
            if response.status_code == 200:
                latest_commit = response.json()
                commit_date = latest_commit['commit']['author']['date']
                commit_message = latest_commit['commit']['message']
                
                # Check if we have this update
                cursor = self.conn.cursor()
                cursor.execute("""
                    SELECT id FROM system_updates 
                    WHERE version = ?
                """, (latest_commit['sha'][:7],))
                
                if not cursor.fetchone():
                    return {
                        'available': True,
                        'version': latest_commit['sha'][:7],
                        'date': commit_date,
                        'message': commit_message
                    }
            
            return {'available': False}
        except Exception as e:
            return {'available': False, 'error': str(e)}
    
    def auto_update_system(self):
        """Automatically update the system from GitHub"""
        try:
            # Pull latest changes
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            if 'Already up to date' in result.stdout:
                return {'status': 'up_to_date', 'message': 'System is already up to date'}
            elif result.returncode == 0:
                # Record the update
                cursor = self.conn.cursor()
                cursor.execute("""
                    INSERT INTO system_updates 
                    (version, module_updated, update_type, changes_made, auto_update, status)
                    VALUES (?, 'Full System', 'git_pull', ?, 1, 'Success')
                """, (datetime.now().strftime('%Y%m%d%H%M'), result.stdout))
                self.conn.commit()
                
                return {'status': 'success', 'message': 'System updated successfully', 'changes': result.stdout}
            else:
                return {'status': 'error', 'message': result.stderr}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def optimize_module(self, module_name):
        """Optimize a specific module based on usage patterns"""
        cursor = self.conn.cursor()
        
        # Analyze module usage
        cursor.execute("""
            SELECT action_type, COUNT(*) as count, AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) as success_rate
            FROM system_learning
            WHERE module_name = ?
            GROUP BY action_type
            ORDER BY count DESC
        """, (module_name,))
        
        usage_stats = cursor.fetchall()
        
        optimizations = []
        for action, count, success_rate in usage_stats:
            if success_rate < 0.8:  # If success rate is low
                optimizations.append({
                    'action': action,
                    'current_success_rate': success_rate,
                    'recommendation': f"Review and improve {action} functionality"
                })
        
        # Record optimization attempt
        if optimizations:
            cursor.execute("""
                INSERT INTO system_optimizations 
                (module_name, optimization_type, before_metrics, after_metrics, auto_applied)
                VALUES (?, 'performance', ?, 'pending', 0)
            """, (module_name, json.dumps(optimizations)))
            self.conn.commit()
        
        return optimizations
    
    def predict_user_needs(self):
        """Predict what the user might need based on patterns"""
        cursor = self.conn.cursor()
        current_hour = datetime.now().hour
        current_day = datetime.now().strftime('%A')
        
        # Get user patterns
        cursor.execute("""
            SELECT pattern_type, pattern_data, frequency
            FROM user_patterns
            WHERE frequency > 3
            ORDER BY frequency DESC, last_occurrence DESC
            LIMIT 5
        """)
        
        patterns = cursor.fetchall()
        predictions = []
        
        for pattern_type, pattern_data, frequency in patterns:
            data = json.loads(pattern_data) if pattern_data else []
            
            # Time-based predictions
            if pattern_type == 'time_preference':
                if 'morning' in data and 6 <= current_hour < 12:
                    predictions.append("Good morning! Ready to check today's shipments?")
                elif 'evening' in data and current_hour >= 17:
                    predictions.append("Evening report: Check today's completed deliveries")
            
            # Action-based predictions
            elif pattern_type == 'common_actions':
                if 'report' in data and current_day == 'Monday':
                    predictions.append("Start the week with a comprehensive business report?")
                elif 'create' in data:
                    predictions.append("Need to create new shipments or add expenses?")
            
            # Data preference predictions
            elif pattern_type == 'data_preferences':
                if 'financial' in data and current_day == 'Friday':
                    predictions.append("End of week financial summary available")
                elif 'shipments' in data:
                    predictions.append(f"You have {self.get_active_shipments_count()} active shipments")
        
        return predictions
    
    def get_active_shipments_count(self):
        """Get count of active shipments"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM shipments 
                WHERE status NOT IN ('Delivered', 'Cancelled')
            """)
            return cursor.fetchone()[0]
        except:
            return 0
    
    def generate_insights(self):
        """Generate business insights from learned patterns"""
        insights = []
        cursor = self.conn.cursor()
        
        # Revenue trends
        cursor.execute("""
            SELECT strftime('%Y-%m', pickup_date) as month, SUM(rate) as revenue
            FROM shipments
            WHERE pickup_date >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month
        """)
        
        revenue_data = cursor.fetchall()
        if len(revenue_data) >= 2:
            trend = 'increasing' if revenue_data[-1][1] > revenue_data[-2][1] else 'decreasing'
            insights.append(f"Revenue trend: {trend} (Last month: ${revenue_data[-1][1]:,.2f})")
        
        # Expense patterns
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE expense_date >= date('now', '-30 days')
            GROUP BY category
            ORDER BY total DESC
            LIMIT 1
        """)
        
        top_expense = cursor.fetchone()
        if top_expense:
            insights.append(f"Highest expense category: {top_expense[0]} (${top_expense[1]:,.2f})")
        
        # Fleet utilization
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM trucks WHERE status = 'Available') as available,
                (SELECT COUNT(*) FROM trucks) as total
        """)
        
        fleet = cursor.fetchone()
        if fleet and fleet[1] > 0:
            utilization = ((fleet[1] - fleet[0]) / fleet[1]) * 100
            insights.append(f"Fleet utilization: {utilization:.1f}%")
        
        # Success rate
        cursor.execute("""
            SELECT AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) * 100 as success_rate
            FROM system_learning
            WHERE learning_date >= date('now', '-7 days')
        """)
        
        success = cursor.fetchone()
        if success and success[0]:
            insights.append(f"System success rate (7 days): {success[0]:.1f}%")
        
        return insights


def show_learning_center():
    """Display the Learning Center interface"""
    st.title("🎓 Learning Center & Intelligent Updates")
    
    # Initialize learning center
    if 'learning_center' not in st.session_state:
        st.session_state.learning_center = LearningCenter()
    
    lc = st.session_state.learning_center
    
    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        knowledge_count = len(lc.knowledge_base)
        st.metric("Knowledge Items", knowledge_count)
    
    with col2:
        predictions = lc.predict_user_needs()
        st.metric("Predictions", len(predictions))
    
    with col3:
        update_info = lc.check_for_updates()
        st.metric("Updates", "Available" if update_info.get('available') else "Current")
    
    with col4:
        insights = lc.generate_insights()
        st.metric("Insights", len(insights))
    
    # Main tabs
    tabs = st.tabs([
        "📚 Knowledge Base",
        "🔄 System Updates",
        "📊 Learning Analytics",
        "🔮 Predictions",
        "💡 Insights",
        "⚙️ Optimization",
        "📖 Training"
    ])
    
    with tabs[0]:
        show_knowledge_base(lc)
    
    with tabs[1]:
        show_system_updates(lc)
    
    with tabs[2]:
        show_learning_analytics(lc)
    
    with tabs[3]:
        show_predictions(lc)
    
    with tabs[4]:
        show_insights(lc)
    
    with tabs[5]:
        show_optimization(lc)
    
    with tabs[6]:
        show_training(lc)


def show_knowledge_base(lc):
    """Display the knowledge base"""
    st.header("📚 System Knowledge Base")
    
    # Search knowledge
    search = st.text_input("🔍 Search knowledge base...")
    
    # Display knowledge categories
    categories = ['All', 'Operations', 'Financial', 'Fleet', 'Personnel', 'Customers', 'Personal', 'General']
    selected_category = st.selectbox("Filter by category", categories)
    
    # Load knowledge
    query = """
        SELECT category, topic, content, confidence_score, usage_count, updated_at
        FROM knowledge_base
    """
    params = []
    
    if selected_category != 'All':
        query += " WHERE category = ?"
        params.append(selected_category)
    
    if search:
        if params:
            query += " AND (topic LIKE ? OR content LIKE ?)"
        else:
            query += " WHERE (topic LIKE ? OR content LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    
    query += " ORDER BY confidence_score DESC, usage_count DESC"
    
    try:
        df = pd.read_sql_query(query, lc.conn, params=params)
        
        if not df.empty:
            for _, row in df.iterrows():
                with st.expander(f"{row['topic']} (Confidence: {row['confidence_score']:.2f})"):
                    st.write(row['content'])
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.caption(f"Category: {row['category']}")
                    with col2:
                        st.caption(f"Used: {row['usage_count']} times")
                    with col3:
                        st.caption(f"Updated: {row['updated_at']}")
        else:
            st.info("No knowledge items found")
            
    except Exception as e:
        st.error(f"Error loading knowledge base: {str(e)}")
    
    # Add new knowledge
    with st.expander("➕ Add Knowledge"):
        with st.form("add_knowledge"):
            topic = st.text_input("Topic")
            content = st.text_area("Content")
            category = st.selectbox("Category", categories[1:])
            
            if st.form_submit_button("Add to Knowledge Base"):
                if topic and content:
                    cursor = lc.conn.cursor()
                    cursor.execute("""
                        INSERT INTO knowledge_base 
                        (category, topic, content, learned_from, confidence_score)
                        VALUES (?, ?, ?, 'manual', 0.8)
                    """, (category, topic, content))
                    lc.conn.commit()
                    st.success("Knowledge added!")
                    st.rerun()


def show_system_updates(lc):
    """Display system updates section"""
    st.header("🔄 System Updates")
    
    # Check for updates
    col1, col2 = st.columns([2, 1])
    
    with col1:
        update_info = lc.check_for_updates()
        if update_info.get('available'):
            st.success(f"🆕 Update available: {update_info.get('version')}")
            st.write(f"Message: {update_info.get('message')}")
        else:
            st.info("✅ System is up to date")
    
    with col2:
        if st.button("🔄 Check for Updates"):
            update_info = lc.check_for_updates()
            if update_info.get('available'):
                if st.button("📥 Install Update"):
                    result = lc.auto_update_system()
                    if result['status'] == 'success':
                        st.success(result['message'])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(result['message'])
    
    # Update history
    st.subheader("📜 Update History")
    
    try:
        updates = pd.read_sql_query("""
            SELECT update_date, version, module_updated, update_type, status
            FROM system_updates
            ORDER BY update_date DESC
            LIMIT 10
        """, lc.conn)
        
        if not updates.empty:
            st.dataframe(updates)
        else:
            st.info("No update history available")
            
    except Exception as e:
        st.error(f"Error loading updates: {str(e)}")
    
    # Auto-update settings
    st.subheader("⚙️ Auto-Update Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        auto_update = st.checkbox("Enable Auto-Updates", value=False)
        if auto_update:
            st.warning("Auto-updates will install updates automatically when available")
    
    with col2:
        update_frequency = st.selectbox(
            "Check Frequency",
            ["Daily", "Weekly", "Monthly", "Manual"]
        )


def show_learning_analytics(lc):
    """Display learning analytics"""
    st.header("📊 Learning Analytics")
    
    # Learning metrics
    col1, col2, col3 = st.columns(3)
    
    try:
        cursor = lc.conn.cursor()
        
        with col1:
            cursor.execute("""
                SELECT COUNT(*) FROM system_learning 
                WHERE learning_date >= date('now', '-7 days')
            """)
            interactions = cursor.fetchone()[0]
            st.metric("Weekly Interactions", interactions)
        
        with col2:
            cursor.execute("""
                SELECT AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) * 100
                FROM system_learning
                WHERE learning_date >= date('now', '-7 days')
            """)
            success_rate = cursor.fetchone()[0] or 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
        
        with col3:
            cursor.execute("""
                SELECT COUNT(DISTINCT module_name) FROM system_learning
                WHERE learning_date >= date('now', '-7 days')
            """)
            active_modules = cursor.fetchone()[0]
            st.metric("Active Modules", active_modules)
        
        # Learning trends chart
        st.subheader("📈 Learning Trends")
        
        learning_df = pd.read_sql_query("""
            SELECT DATE(learning_date) as date,
                   COUNT(*) as interactions,
                   AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) * 100 as success_rate
            FROM system_learning
            WHERE learning_date >= date('now', '-30 days')
            GROUP BY DATE(learning_date)
            ORDER BY date
        """, lc.conn)
        
        if not learning_df.empty:
            import plotly.graph_objects as go
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=learning_df['date'],
                y=learning_df['interactions'],
                name='Interactions',
                mode='lines+markers'
            ))
            fig.add_trace(go.Scatter(
                x=learning_df['date'],
                y=learning_df['success_rate'],
                name='Success Rate (%)',
                mode='lines+markers',
                yaxis='y2'
            ))
            
            fig.update_layout(
                title='System Learning Over Time',
                yaxis=dict(title='Interactions'),
                yaxis2=dict(title='Success Rate (%)', overlaying='y', side='right'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Module performance
        st.subheader("🎯 Module Performance")
        
        module_df = pd.read_sql_query("""
            SELECT module_name,
                   COUNT(*) as usage_count,
                   AVG(CASE WHEN outcome = 'success' THEN 1 ELSE 0 END) * 100 as success_rate
            FROM system_learning
            GROUP BY module_name
            ORDER BY usage_count DESC
        """, lc.conn)
        
        if not module_df.empty:
            st.dataframe(module_df)
            
    except Exception as e:
        st.error(f"Error loading analytics: {str(e)}")


def show_predictions(lc):
    """Display AI predictions"""
    st.header("🔮 AI Predictions & Suggestions")
    
    # Get predictions
    predictions = lc.predict_user_needs()
    
    if predictions:
        st.subheader("Based on your patterns, you might want to:")
        for prediction in predictions:
            st.info(f"💡 {prediction}")
    else:
        st.info("No predictions available yet. Keep using the system to enable predictions.")
    
    # Pattern analysis
    st.subheader("📊 Your Usage Patterns")
    
    try:
        patterns = pd.read_sql_query("""
            SELECT pattern_type, pattern_data, frequency, last_occurrence
            FROM user_patterns
            ORDER BY frequency DESC
            LIMIT 10
        """, lc.conn)
        
        if not patterns.empty:
            for _, pattern in patterns.iterrows():
                with st.expander(f"{pattern['pattern_type']} (Used {pattern['frequency']} times)"):
                    data = json.loads(pattern['pattern_data']) if pattern['pattern_data'] else []
                    st.write(f"Pattern: {', '.join(data) if isinstance(data, list) else data}")
                    st.caption(f"Last used: {pattern['last_occurrence']}")
        else:
            st.info("No patterns detected yet")
            
    except Exception as e:
        st.error(f"Error loading patterns: {str(e)}")


def show_insights(lc):
    """Display business insights"""
    st.header("💡 Business Insights")
    
    insights = lc.generate_insights()
    
    if insights:
        for insight in insights:
            st.success(f"📊 {insight}")
    else:
        st.info("No insights available yet. More data needed for analysis.")
    
    # Custom insight generation
    st.subheader("🔍 Deep Analysis")
    
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Revenue Analysis", "Expense Analysis", "Fleet Efficiency", "Customer Analysis", "Personal Finance"]
    )
    
    if st.button("Generate Analysis"):
        with st.spinner("Analyzing..."):
            if analysis_type == "Revenue Analysis":
                show_revenue_analysis(lc)
            elif analysis_type == "Expense Analysis":
                show_expense_analysis(lc)
            elif analysis_type == "Fleet Efficiency":
                show_fleet_analysis(lc)
            elif analysis_type == "Customer Analysis":
                show_customer_analysis(lc)
            elif analysis_type == "Personal Finance":
                show_personal_analysis(lc)


def show_revenue_analysis(lc):
    """Show detailed revenue analysis"""
    try:
        revenue_df = pd.read_sql_query("""
            SELECT strftime('%Y-%m', pickup_date) as month,
                   SUM(rate) as revenue,
                   COUNT(*) as shipment_count,
                   AVG(rate) as avg_rate
            FROM shipments
            WHERE pickup_date >= date('now', '-12 months')
            GROUP BY month
            ORDER BY month
        """, lc.conn)
        
        if not revenue_df.empty:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Revenue (12mo)", f"${revenue_df['revenue'].sum():,.2f}")
            with col2:
                st.metric("Avg Rate per Load", f"${revenue_df['avg_rate'].mean():,.2f}")
            
            st.line_chart(revenue_df.set_index('month')['revenue'])
    except:
        st.error("No revenue data available")


def show_expense_analysis(lc):
    """Show detailed expense analysis"""
    try:
        expense_df = pd.read_sql_query("""
            SELECT category,
                   SUM(amount) as total,
                   COUNT(*) as count,
                   AVG(amount) as avg_amount
            FROM expenses
            WHERE expense_date >= date('now', '-30 days')
            GROUP BY category
            ORDER BY total DESC
        """, lc.conn)
        
        if not expense_df.empty:
            st.bar_chart(expense_df.set_index('category')['total'])
            st.dataframe(expense_df)
    except:
        st.error("No expense data available")


def show_fleet_analysis(lc):
    """Show fleet efficiency analysis"""
    st.info("Fleet efficiency analysis based on truck utilization and maintenance")


def show_customer_analysis(lc):
    """Show customer analysis"""
    st.info("Customer revenue and payment analysis")


def show_personal_analysis(lc):
    """Show personal finance analysis"""
    st.info("Personal net worth and expense tracking analysis")


def show_optimization(lc):
    """Display system optimization options"""
    st.header("⚙️ System Optimization")
    
    # Module selection for optimization
    modules = ['AI Assistant', 'Shipment Management', 'Fleet Management', 
               'Expense Tracking', 'User Interface', 'Database Performance']
    
    selected_module = st.selectbox("Select module to optimize", modules)
    
    if st.button("🔧 Analyze & Optimize"):
        with st.spinner(f"Analyzing {selected_module}..."):
            optimizations = lc.optimize_module(selected_module)
            
            if optimizations:
                st.warning(f"Found {len(optimizations)} optimization opportunities:")
                for opt in optimizations:
                    st.write(f"• {opt['recommendation']}")
                    st.caption(f"Current success rate: {opt['current_success_rate']:.1%}")
            else:
                st.success(f"{selected_module} is performing optimally!")
    
    # Performance metrics
    st.subheader("📊 System Performance")
    
    try:
        perf_df = pd.read_sql_query("""
            SELECT module_name,
                   optimization_type,
                   improvement_percentage,
                   optimization_date
            FROM system_optimizations
            WHERE improvement_percentage IS NOT NULL
            ORDER BY optimization_date DESC
            LIMIT 10
        """, lc.conn)
        
        if not perf_df.empty:
            st.dataframe(perf_df)
        else:
            st.info("No optimization history available")
            
    except Exception as e:
        st.error(f"Error loading optimizations: {str(e)}")


def show_training(lc):
    """Display training and help section"""
    st.header("📖 System Training & Help")
    
    # Training topics
    topics = {
        "Getting Started": """
        Welcome to the TMS Learning Center!
        
        1. **Dashboard**: View key metrics and KPIs
        2. **AI Assistant**: Use natural language commands
        3. **Management Center**: Direct access to all functions
        4. **Personal Management**: Track personal finances and goals
        """,
        
        "AI Commands": """
        The AI Assistant understands natural language:
        
        **Shipments:**
        - "Add new load from LA to Phoenix for $3500"
        - "Show all active shipments"
        - "Where is load #12345?"
        
        **Expenses:**
        - "I spent $500 on fuel"
        - "Add business expense $1000 for repairs"
        - "Show this month's expenses"
        
        **Reports:**
        - "Generate daily report"
        - "What's my net worth?"
        - "Show profit and loss"
        """,
        
        "Override & Manual Control": """
        You always have full control:
        
        1. Type "override" in AI chat for manual options
        2. Use sidebar navigation for direct access
        3. All AI actions require confirmation
        4. Access Management Center for full control
        """,
        
        "Mobile Access": """
        Access from any device:
        
        **Local Network:**
        - URL: http://172.20.10.6:8501
        - Devices must be on same WiFi
        
        **Cloud Deployment:**
        - Deploy to Streamlit Cloud
        - Access from anywhere
        - Works on cellular data
        """,
        
        "Best Practices": """
        Tips for optimal use:
        
        1. **Regular Updates**: Check Learning Center for updates
        2. **Data Entry**: Be consistent with formats
        3. **AI Training**: The more you use it, the smarter it gets
        4. **Backups**: System auto-backs up daily
        5. **Security**: Change password regularly
        """
    }
    
    selected_topic = st.selectbox("Select a topic", list(topics.keys()))
    
    st.markdown(topics[selected_topic])
    
    # FAQ section
    st.subheader("❓ Frequently Asked Questions")
    
    faqs = {
        "How do I add a new user?": "Go to Management Center → Users → Add New User",
        "How do I track personal expenses?": "Use Personal Management or tell AI 'I spent $X on Y'",
        "How do I generate reports?": "Use AI Assistant 'generate report' or go to Reports section",
        "How do I override AI actions?": "Type 'override' or use Management Center directly",
        "How do I access from mobile?": "Use the mobile URL or deploy to Streamlit Cloud"
    }
    
    for question, answer in faqs.items():
        with st.expander(question):
            st.write(answer)
    
    # Feedback
    st.subheader("💬 Feedback & Support")
    
    feedback = st.text_area("Share your feedback or report issues:")
    if st.button("Submit Feedback"):
        if feedback:
            # Store feedback in database
            cursor = lc.conn.cursor()
            cursor.execute("""
                INSERT INTO knowledge_base 
                (category, topic, content, learned_from, confidence_score)
                VALUES ('Feedback', 'User Feedback', ?, 'user', 1.0)
            """, (feedback,))
            lc.conn.commit()
            st.success("Thank you for your feedback!")
            st.balloons()