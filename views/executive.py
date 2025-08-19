"""
Executive Dashboard View for Smith & Williams Trucking TMS
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from modules.ui_components import create_metric_card, show_data_protection_footer

def show_executive_view():
    """Display executive dashboard with KPIs and analytics"""
    
    st.title("📊 Executive Dashboard")
    st.markdown(f"### Welcome, {st.session_state.get('user_full_name', 'Executive')}")
    st.markdown(f"*Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*")
    
    # KPI Metrics Row
    st.markdown("## 📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(create_metric_card("Total Revenue", "$1,245,890", "+12.5%"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_metric_card("Active Loads", "47", "+5"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(create_metric_card("On-Time Delivery", "94.7%", "+2.3%"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(create_metric_card("Fleet Utilization", "87%", "-3%", "inverse"), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts Section
    st.markdown("## 📊 Performance Analytics")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Revenue Trends", "Load Analysis", "Fleet Performance", "Customer Metrics"])
    
    with tab1:
        # Revenue Chart
        dates = pd.date_range(start='2025-01-01', periods=30, freq='D')
        revenue_data = pd.DataFrame({
            'Date': dates,
            'Revenue': [45000 + i*1000 + (i%7)*2000 for i in range(30)],
            'Target': [50000] * 30
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=revenue_data['Date'],
            y=revenue_data['Revenue'],
            mode='lines+markers',
            name='Actual Revenue',
            line=dict(color='#DC2626', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=revenue_data['Date'],
            y=revenue_data['Target'],
            mode='lines',
            name='Target',
            line=dict(color='#8B0000', width=2, dash='dash')
        ))
        fig.update_layout(
            title='Daily Revenue Trend',
            xaxis_title='Date',
            yaxis_title='Revenue ($)',
            hovermode='x unified',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Load Status Distribution
        load_status = pd.DataFrame({
            'Status': ['Delivered', 'In Transit', 'Dispatched', 'Pending', 'Cancelled'],
            'Count': [156, 47, 23, 12, 5],
            'Color': ['#10b981', '#3b82f6', '#f59e0b', '#6b7280', '#ef4444']
        })
        
        fig = px.pie(
            load_status,
            values='Count',
            names='Status',
            title='Load Status Distribution',
            color='Status',
            color_discrete_map={status: color for status, color in zip(load_status['Status'], load_status['Color'])}
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Fleet Utilization
        fleet_data = pd.DataFrame({
            'Truck': [f'Truck {i}' for i in range(1, 11)],
            'Utilization': [92, 87, 95, 78, 88, 91, 85, 93, 76, 89]
        })
        
        fig = px.bar(
            fleet_data,
            x='Truck',
            y='Utilization',
            title='Fleet Utilization by Truck',
            color='Utilization',
            color_continuous_scale=['#8B0000', '#DC2626', '#10b981']
        )
        fig.update_layout(
            xaxis_title='Truck',
            yaxis_title='Utilization (%)',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        # Top Customers
        customer_data = pd.DataFrame({
            'Customer': ['ABC Corp', 'XYZ Industries', 'Global Logistics', 'Prime Shipping', 'Fast Freight'],
            'Revenue': [245000, 198000, 176000, 145000, 123000]
        })
        
        fig = px.bar(
            customer_data,
            x='Revenue',
            y='Customer',
            orientation='h',
            title='Top 5 Customers by Revenue',
            color_discrete_sequence=['#DC2626']
        )
        fig.update_layout(
            xaxis_title='Revenue ($)',
            yaxis_title='Customer'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("## ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Generate Report", use_container_width=True):
            st.info("Report generation initiated...")
    
    with col2:
        if st.button("📧 Email Summary", use_container_width=True):
            st.info("Preparing email summary...")
    
    with col3:
        if st.button("📥 Export Data", use_container_width=True):
            st.info("Exporting dashboard data...")
    
    # Data Protection Footer
    show_data_protection_footer()