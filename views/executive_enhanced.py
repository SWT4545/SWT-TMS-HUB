"""
Enhanced Executive Dashboard for Smith & Williams Trucking TMS
Includes real-time KPIs, analytics, and intelligent insights
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.database_enhanced import execute_query, get_db_connection
from modules.ai_assistants import VernonSecurityManager

def show_executive_view():
    """Display the enhanced executive dashboard with KPIs and analytics"""
    
    # Initialize Vernon for security monitoring
    vernon = VernonSecurityManager()
    
    # Header
    st.markdown("""
    <h1 style='text-align: center; color: white; border-bottom: 3px solid #8B0000; padding-bottom: 20px;'>
        🎯 EXECUTIVE COMMAND CENTER
    </h1>
    """, unsafe_allow_html=True)
    
    # Display user info
    st.markdown(f"""
    <div style='text-align: right; color: #8B0000; font-weight: bold; margin-bottom: 20px;'>
        Welcome, {st.session_state.get('user_full_name', 'Executive')} | 
        Role: {st.session_state.get('role', 'N/A').replace('_', ' ').title()}
    </div>
    """, unsafe_allow_html=True)
    
    # Main KPI Dashboard
    display_kpi_metrics()
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Real-Time Analytics", 
        "💰 Financial Overview", 
        "🚚 Fleet Status",
        "📈 Performance Trends",
        "🔒 System Security"
    ])
    
    with tab1:
        display_realtime_analytics()
    
    with tab2:
        display_financial_overview()
    
    with tab3:
        display_fleet_status()
    
    with tab4:
        display_performance_trends()
    
    with tab5:
        vernon.display_security_status()
        if vernon.verify_data_integrity():
            st.success("✅ All data integrity checks passed")


def display_kpi_metrics():
    """Display key performance indicators"""
    
    # Get current month data
    current_month = datetime.now().strftime('%Y-%m')
    
    # Calculate KPIs
    total_revenue = execute_query("""
        SELECT COALESCE(SUM(gross_amount), 0) as total 
        FROM loads 
        WHERE strftime('%Y-%m', delivery_date) = ?
    """, (current_month,))
    
    total_loads = execute_query("""
        SELECT COUNT(*) as count 
        FROM loads 
        WHERE strftime('%Y-%m', delivery_date) = ?
    """, (current_month,))
    
    avg_rate_per_mile = execute_query("""
        SELECT COALESCE(AVG(gross_rate_per_mile), 0) as avg_rate 
        FROM loads 
        WHERE strftime('%Y-%m', delivery_date) = ? 
        AND gross_rate_per_mile IS NOT NULL
    """, (current_month,))
    
    pending_payments = execute_query("""
        SELECT COALESCE(SUM(net_amount), 0) as pending 
        FROM loads 
        WHERE status = 'completed' 
        AND id NOT IN (SELECT load_id FROM payment_load_reconciliation)
    """)
    
    # Display KPIs in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        revenue = total_revenue[0]['total'] if total_revenue else 0
        st.metric(
            label="📈 Monthly Revenue",
            value=f"${revenue:,.2f}",
            delta="Target: $250,000"
        )
    
    with col2:
        loads = total_loads[0]['count'] if total_loads else 0
        st.metric(
            label="🚚 Total Loads",
            value=f"{loads}",
            delta="This Month"
        )
    
    with col3:
        rate = avg_rate_per_mile[0]['avg_rate'] if avg_rate_per_mile else 0
        st.metric(
            label="💵 Avg Rate/Mile",
            value=f"${rate:.2f}",
            delta="Industry: $2.50"
        )
    
    with col4:
        pending = pending_payments[0]['pending'] if pending_payments else 0
        st.metric(
            label="⏳ Pending Payments",
            value=f"${pending:,.2f}",
            delta="To be collected"
        )


def display_realtime_analytics():
    """Display real-time operational analytics"""
    
    st.subheader("🔴 Live Operations Dashboard")
    
    # Get active loads
    active_loads = execute_query("""
        SELECT l.*, u.full_name as driver_name
        FROM loads l
        LEFT JOIN users u ON l.driver_id = u.id
        WHERE l.status IN ('in_transit', 'at_pickup', 'at_delivery')
        ORDER BY l.pickup_date DESC
    """)
    
    if active_loads:
        st.info(f"📍 {len(active_loads)} loads currently active")
        
        # Display active loads on map (placeholder for actual map)
        for load in active_loads:
            with st.expander(f"Load {load['load_id']} - {load['status'].replace('_', ' ').title()}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.write(f"**Driver:** {load['driver_name'] or 'Unassigned'}")
                    st.write(f"**Customer:** {load['customer']}")
                with col2:
                    st.write(f"**Pickup:** {load['pickup_city']}, {load['pickup_state']}")
                    st.write(f"**Delivery:** {load['delivery_city']}, {load['delivery_state']}")
                with col3:
                    st.write(f"**Amount:** ${load['gross_amount']:,.2f}")
                    if load['status'] == 'in_transit':
                        st.progress(0.5, text="In Transit")
    else:
        st.info("No active loads at this moment")
    
    # Load distribution by carrier
    st.subheader("📊 Load Distribution")
    carrier_data = execute_query("""
        SELECT carrier, COUNT(*) as count, SUM(gross_amount) as revenue
        FROM loads
        WHERE strftime('%Y-%m', delivery_date) = strftime('%Y-%m', 'now')
        GROUP BY carrier
        ORDER BY revenue DESC
    """)
    
    if carrier_data:
        df_carriers = pd.DataFrame(carrier_data)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df_carriers, values='count', names='carrier', 
                        title="Loads by Carrier")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df_carriers, x='carrier', y='revenue',
                        title="Revenue by Carrier")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(139,0,0,0.2)')
            )
            st.plotly_chart(fig, use_container_width=True)


def display_financial_overview():
    """Display detailed financial analytics"""
    
    st.subheader("💰 Financial Performance Analysis")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                   value=datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", 
                                 value=datetime.now())
    
    # Get financial data
    financial_data = execute_query("""
        SELECT 
            DATE(delivery_date) as date,
            SUM(gross_amount) as gross_revenue,
            SUM(net_amount) as net_revenue,
            SUM(gross_amount - net_amount) as fees,
            COUNT(*) as load_count,
            AVG(gross_rate_per_mile) as avg_rate
        FROM loads
        WHERE delivery_date BETWEEN ? AND ?
        GROUP BY DATE(delivery_date)
        ORDER BY date
    """, (start_date, end_date))
    
    if financial_data:
        df = pd.DataFrame(financial_data)
        
        # Revenue trend chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['gross_revenue'],
            mode='lines+markers',
            name='Gross Revenue',
            line=dict(color='#00ff00', width=3)
        ))
        fig.add_trace(go.Scatter(
            x=df['date'], y=df['net_revenue'],
            mode='lines+markers',
            name='Net Revenue',
            line=dict(color='#8B0000', width=3)
        ))
        fig.update_layout(
            title="Revenue Trend",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(139,0,0,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_gross = df['gross_revenue'].sum()
            st.metric("Total Gross", f"${total_gross:,.2f}")
        with col2:
            total_net = df['net_revenue'].sum()
            st.metric("Total Net", f"${total_net:,.2f}")
        with col3:
            total_fees = df['fees'].sum()
            st.metric("Total Fees", f"${total_fees:,.2f}")
        with col4:
            if total_gross > 0:
                margin = (total_net / total_gross) * 100
                st.metric("Net Margin", f"{margin:.1f}%")
    
    # Payment reconciliation status
    st.subheader("💳 Payment Reconciliation Status")
    
    unreconciled = execute_query("""
        SELECT carrier, COUNT(*) as count, SUM(net_amount) as amount
        FROM loads
        WHERE status = 'completed'
        AND id NOT IN (SELECT load_id FROM payment_load_reconciliation)
        GROUP BY carrier
    """)
    
    if unreconciled:
        st.warning(f"⚠️ {len(unreconciled)} carriers have unreconciled payments")
        for item in unreconciled:
            st.write(f"• **{item['carrier']}**: {item['count']} loads, ${item['amount']:,.2f}")
    else:
        st.success("✅ All payments reconciled")


def display_fleet_status():
    """Display fleet and equipment status"""
    
    st.subheader("🚚 Fleet Management Dashboard")
    
    # Get equipment data
    equipment = execute_query("""
        SELECT * FROM equipment 
        WHERE status = 'active'
        ORDER BY equipment_type, unit_number
    """)
    
    if equipment:
        # Group by type
        trucks = [e for e in equipment if e['equipment_type'] == 'Truck']
        trailers = [e for e in equipment if e['equipment_type'] == 'Trailer']
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🚛 Active Trucks", len(trucks))
        with col2:
            st.metric("📦 Active Trailers", len(trailers))
        
        # Equipment utilization
        st.subheader("Equipment Utilization")
        
        utilization = execute_query("""
            SELECT 
                e.unit_number,
                e.equipment_type,
                COUNT(l.id) as loads_completed,
                MAX(l.delivery_date) as last_used
            FROM equipment e
            LEFT JOIN loads l ON 
                (e.equipment_type = 'Truck' AND e.id = l.truck_id) OR
                (e.equipment_type = 'Trailer' AND e.id = l.trailer_id)
            WHERE e.status = 'active'
            GROUP BY e.id
            ORDER BY loads_completed DESC
        """)
        
        if utilization:
            df_util = pd.DataFrame(utilization)
            fig = px.bar(df_util.head(10), x='unit_number', y='loads_completed',
                        color='equipment_type',
                        title="Top 10 Most Used Equipment")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No equipment data available. Add equipment in the Data Entry section.")
    
    # Driver performance
    st.subheader("👥 Driver Performance")
    
    driver_stats = execute_query("""
        SELECT 
            u.full_name,
            COUNT(l.id) as loads_completed,
            AVG(l.gross_amount) as avg_load_value,
            SUM(l.distance_miles) as total_miles
        FROM users u
        JOIN loads l ON u.id = l.driver_id
        WHERE u.role = 'driver'
        AND l.status = 'completed'
        GROUP BY u.id
        ORDER BY loads_completed DESC
        LIMIT 10
    """)
    
    if driver_stats:
        df_drivers = pd.DataFrame(driver_stats)
        st.dataframe(df_drivers, use_container_width=True)
    else:
        st.info("No driver performance data available yet.")


def display_performance_trends():
    """Display performance trends and projections"""
    
    st.subheader("📈 Performance Trends & Projections")
    
    # Monthly performance trend
    monthly_data = execute_query("""
        SELECT 
            strftime('%Y-%m', delivery_date) as month,
            COUNT(*) as loads,
            SUM(gross_amount) as revenue,
            AVG(gross_rate_per_mile) as avg_rate,
            SUM(distance_miles) as total_miles
        FROM loads
        WHERE delivery_date >= date('now', '-12 months')
        GROUP BY strftime('%Y-%m', delivery_date)
        ORDER BY month
    """)
    
    if monthly_data:
        df_monthly = pd.DataFrame(monthly_data)
        
        # Create subplots
        fig = go.Figure()
        
        # Revenue trend
        fig.add_trace(go.Bar(
            x=df_monthly['month'],
            y=df_monthly['revenue'],
            name='Monthly Revenue',
            marker_color='#8B0000'
        ))
        
        fig.update_layout(
            title="12-Month Revenue Trend",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(139,0,0,0.2)')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Calculate growth rate
            if len(df_monthly) >= 2:
                last_month = df_monthly.iloc[-1]['revenue']
                prev_month = df_monthly.iloc[-2]['revenue']
                growth = ((last_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
                st.metric("Month-over-Month Growth", f"{growth:.1f}%")
        
        with col2:
            # Average monthly revenue
            avg_monthly = df_monthly['revenue'].mean()
            st.metric("Avg Monthly Revenue", f"${avg_monthly:,.2f}")
        
        with col3:
            # Projected next month
            if len(df_monthly) >= 3:
                # Simple projection based on trend
                recent_avg = df_monthly.tail(3)['revenue'].mean()
                st.metric("Next Month Projection", f"${recent_avg * 1.05:,.2f}")
    
    # Goal tracking
    st.subheader("🎯 Goal Tracking")
    
    goals = {
        "Monthly Revenue": {"target": 250000, "current": 0},
        "Loads per Month": {"target": 100, "current": 0},
        "Avg Rate/Mile": {"target": 3.00, "current": 0}
    }
    
    # Get current month stats
    current_stats = execute_query("""
        SELECT 
            SUM(gross_amount) as revenue,
            COUNT(*) as loads,
            AVG(gross_rate_per_mile) as avg_rate
        FROM loads
        WHERE strftime('%Y-%m', delivery_date) = strftime('%Y-%m', 'now')
    """)
    
    if current_stats and current_stats[0]['revenue']:
        goals["Monthly Revenue"]["current"] = current_stats[0]['revenue']
        goals["Loads per Month"]["current"] = current_stats[0]['loads']
        goals["Avg Rate/Mile"]["current"] = current_stats[0]['avg_rate'] or 0
    
    for goal_name, goal_data in goals.items():
        progress = (goal_data["current"] / goal_data["target"]) if goal_data["target"] > 0 else 0
        progress = min(progress, 1.0)  # Cap at 100%
        
        st.write(f"**{goal_name}**")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(progress)
        with col2:
            if goal_name == "Monthly Revenue":
                st.write(f"${goal_data['current']:,.0f} / ${goal_data['target']:,.0f}")
            elif goal_name == "Avg Rate/Mile":
                st.write(f"${goal_data['current']:.2f} / ${goal_data['target']:.2f}")
            else:
                st.write(f"{goal_data['current']} / {goal_data['target']}")