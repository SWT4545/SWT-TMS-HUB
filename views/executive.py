"""
Executive Dashboard View for SWT TMS Hub
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from config.database import get_connection
from modules.ui_components import show_page_header, show_metric_card, format_currency

def show_executive_view():
    """Display executive dashboard with KPIs and analytics"""
    show_page_header(
        "📊 Executive Dashboard", 
        "Real-time business metrics and performance indicators"
    )
    
    # Date range selector
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        start_date = st.date_input("From Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("To Date", datetime.now())
    with col3:
        st.write("")
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    # Get database connection
    conn = get_connection()
    
    # Key Performance Indicators
    st.subheader("📈 Key Performance Indicators")
    
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        active_loads = pd.read_sql_query("""
            SELECT COUNT(*) as count 
            FROM shipments 
            WHERE status IN ('Assigned', 'Dispatched', 'In Transit')
        """, conn).iloc[0]['count']
        st.metric("Active Loads", active_loads, delta="+3 today")
    
    with kpi_col2:
        revenue_mtd = pd.read_sql_query("""
            SELECT COALESCE(SUM(rate), 0) as total 
            FROM shipments 
            WHERE date(pickup_date) >= date('now', 'start of month')
            AND status = 'Delivered'
        """, conn).iloc[0]['total']
        st.metric("Revenue MTD", format_currency(revenue_mtd), delta="+12%")
    
    with kpi_col3:
        pending_invoices = pd.read_sql_query("""
            SELECT COALESCE(SUM(total_amount), 0) as total 
            FROM invoices 
            WHERE status IN ('Pending', 'Sent')
        """, conn).iloc[0]['total']
        st.metric("Pending A/R", format_currency(pending_invoices))
    
    with kpi_col4:
        delivered_today = pd.read_sql_query("""
            SELECT COUNT(*) as count 
            FROM shipments 
            WHERE status = 'Delivered' 
            AND date(updated_at) = date('now')
        """, conn).iloc[0]['count']
        st.metric("Delivered Today", delivered_today, delta="+5%")
    
    with kpi_col5:
        profit_margin = pd.read_sql_query("""
            SELECT 
                COALESCE(SUM(s.rate), 0) as revenue,
                COALESCE(SUM(d.carrier_rate + COALESCE(d.fuel_advance, 0)), 0) as costs
            FROM shipments s
            LEFT JOIN dispatches d ON s.id = d.shipment_id
            WHERE date(s.pickup_date) BETWEEN date(?) AND date(?)
        """, conn, params=(start_date, end_date))
        
        revenue = profit_margin.iloc[0]['revenue']
        costs = profit_margin.iloc[0]['costs']
        margin = ((revenue - costs) / revenue * 100) if revenue > 0 else 0
        st.metric("Profit Margin", f"{margin:.1f}%")
    
    st.markdown("---")
    
    # Charts and Analytics
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.subheader("Revenue Trend (Last 30 Days)")
        revenue_trend = pd.read_sql_query("""
            SELECT 
                date(pickup_date) as date,
                SUM(rate) as revenue
            FROM shipments
            WHERE date(pickup_date) >= date('now', '-30 days')
            AND status = 'Delivered'
            GROUP BY date(pickup_date)
            ORDER BY date
        """, conn)
        
        if not revenue_trend.empty:
            st.line_chart(revenue_trend.set_index('date')['revenue'])
        else:
            st.info("No revenue data available")
    
    with chart_col2:
        st.subheader("Load Status Distribution")
        status_data = pd.read_sql_query("""
            SELECT status, COUNT(*) as count 
            FROM shipments 
            WHERE date(created_at) BETWEEN date(?) AND date(?)
            GROUP BY status
        """, conn, params=(start_date, end_date))
        
        if not status_data.empty:
            st.bar_chart(status_data.set_index('status')['count'])
        else:
            st.info("No status data available")
    
    # Performance Metrics
    st.subheader("📊 Performance Analytics")
    
    perf_col1, perf_col2 = st.columns(2)
    
    with perf_col1:
        st.markdown("#### Top Performing Lanes")
        top_lanes = pd.read_sql_query("""
            SELECT 
                origin_city || ', ' || origin_state || ' → ' || 
                destination_city || ', ' || destination_state as lane,
                COUNT(*) as shipments,
                AVG(rate) as avg_rate,
                SUM(rate) as total_revenue
            FROM shipments
            WHERE date(pickup_date) BETWEEN date(?) AND date(?)
            GROUP BY origin_city, origin_state, destination_city, destination_state
            HAVING COUNT(*) > 1
            ORDER BY total_revenue DESC
            LIMIT 5
        """, conn, params=(start_date, end_date))
        
        if not top_lanes.empty:
            st.dataframe(top_lanes, use_container_width=True, hide_index=True)
        else:
            st.info("No lane data available")
    
    with perf_col2:
        st.markdown("#### Financial Summary")
        financial_summary = pd.read_sql_query("""
            SELECT 
                'Revenue' as metric,
                COALESCE(SUM(rate), 0) as amount
            FROM shipments 
            WHERE date(pickup_date) BETWEEN date(?) AND date(?)
            UNION ALL
            SELECT 
                'Invoiced' as metric,
                COALESCE(SUM(total_amount), 0) as amount
            FROM invoices 
            WHERE date(invoice_date) BETWEEN date(?) AND date(?)
            UNION ALL
            SELECT 
                'Collected' as metric,
                COALESCE(SUM(total_amount), 0) as amount
            FROM invoices 
            WHERE status = 'Paid' 
            AND date(paid_date) BETWEEN date(?) AND date(?)
        """, conn, params=(start_date, end_date, start_date, end_date, start_date, end_date))
        
        if not financial_summary.empty:
            for _, row in financial_summary.iterrows():
                st.metric(row['metric'], format_currency(row['amount']))
        else:
            st.info("No financial data available")
    
    # Recent Activity
    st.subheader("🕐 Recent Activity")
    recent_activity = pd.read_sql_query("""
        SELECT 
            load_number,
            origin_city || ', ' || origin_state as origin,
            destination_city || ', ' || destination_state as destination,
            pickup_date,
            status,
            rate
        FROM shipments
        ORDER BY created_at DESC
        LIMIT 10
    """, conn)
    
    if not recent_activity.empty:
        st.dataframe(recent_activity, use_container_width=True, hide_index=True)
        
        # Export option
        csv = recent_activity.to_csv(index=False)
        st.download_button(
            "📥 Export Recent Activity",
            csv,
            f"recent_activity_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv"
        )
    else:
        st.info("No recent activity")
    
    conn.close()