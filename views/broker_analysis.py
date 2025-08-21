"""
Broker Analysis Module for Smith & Williams Trucking TMS
Analyzes broker relationships and identifies business opportunities
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config.database import get_connection
import plotly.express as px
import plotly.graph_objects as go

def show_broker_analysis_view():
    """Display Broker Analysis interface"""
    show_broker_analysis()
    return

def show_broker_analysis():
    """Main broker analysis interface"""
    st.title("📊 Broker Analysis & Business Development")
    
    conn = get_connection()
    
    # Ensure we have the broker data columns
    ensure_broker_columns(conn)
    
    # Main tabs
    tabs = st.tabs([
        "🏢 Broker Overview",
        "💰 Revenue Analysis", 
        "📈 Performance Metrics",
        "🎯 Lead Generation",
        "📊 Lane Analysis"
    ])
    
    with tabs[0]:
        show_broker_overview(conn)
    
    with tabs[1]:
        show_revenue_analysis(conn)
    
    with tabs[2]:
        show_performance_metrics(conn)
    
    with tabs[3]:
        show_lead_generation(conn)
    
    with tabs[4]:
        show_lane_analysis(conn)

def ensure_broker_columns(conn):
    """Ensure database has necessary broker-related columns"""
    cursor = conn.cursor()
    
    # Add broker-related columns to shipments table if they don't exist
    try:
        cursor.execute("""
            ALTER TABLE shipments ADD COLUMN load_board_broker TEXT
        """)
        conn.commit()
    except:
        pass  # Column already exists
    
    try:
        cursor.execute("""
            ALTER TABLE shipments ADD COLUMN broker_phone TEXT
        """)
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute("""
            ALTER TABLE shipments ADD COLUMN broker_email TEXT
        """)
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute("""
            ALTER TABLE shipments ADD COLUMN broker_mc_number TEXT
        """)
        conn.commit()
    except:
        pass
    
    # Create broker analysis table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS broker_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            broker_name TEXT UNIQUE,
            total_loads INTEGER DEFAULT 0,
            total_revenue DECIMAL(12,2) DEFAULT 0,
            avg_rate_per_mile DECIMAL(10,4) DEFAULT 0,
            avg_gross_per_load DECIMAL(10,2) DEFAULT 0,
            first_load_date DATE,
            last_load_date DATE,
            payment_history TEXT,
            credit_score INTEGER,
            preferred_lanes TEXT,
            notes TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def show_broker_overview(conn):
    """Display broker overview and key metrics"""
    st.header("🏢 Broker Overview")
    
    # Get CanAmex carrier data
    try:
        # First, check what carrier data we have
        carrier_query = """
            SELECT DISTINCT carrier_id, 
                   COUNT(*) as load_count
            FROM shipments
            WHERE carrier_id IS NOT NULL 
               OR load_board_broker IS NOT NULL
            GROUP BY carrier_id
        """
        
        carriers_df = pd.read_sql_query(carrier_query, conn)
        
        # Main broker analysis query
        broker_query = """
            SELECT 
                COALESCE(load_board_broker, 'Direct Customer') as broker_name,
                COUNT(*) as total_loads,
                SUM(rate) as total_revenue,
                AVG(rate) as avg_rate,
                AVG(CASE WHEN miles > 0 THEN rate/miles ELSE 0 END) as avg_rate_per_mile,
                MAX(pickup_date) as last_load_date,
                MIN(pickup_date) as first_load_date
            FROM shipments
            WHERE status NOT IN ('Cancelled')
            GROUP BY load_board_broker
            ORDER BY total_revenue DESC
        """
        
        brokers_df = pd.read_sql_query(broker_query, conn)
        
        if not brokers_df.empty:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_brokers = len(brokers_df[brokers_df['broker_name'] != 'Direct Customer'])
                st.metric("Total Brokers", total_brokers)
            
            with col2:
                total_broker_revenue = brokers_df[brokers_df['broker_name'] != 'Direct Customer']['total_revenue'].sum()
                st.metric("Broker Revenue", f"${total_broker_revenue:,.2f}")
            
            with col3:
                avg_broker_rate = brokers_df[brokers_df['broker_name'] != 'Direct Customer']['avg_rate'].mean()
                st.metric("Avg Broker Rate", f"${avg_broker_rate:,.2f}")
            
            with col4:
                top_broker = brokers_df.iloc[0]['broker_name'] if not brokers_df.empty else "N/A"
                st.metric("Top Broker", top_broker)
            
            # Broker table
            st.subheader("Broker Performance Table")
            
            # Format the dataframe
            display_df = brokers_df.copy()
            display_df['total_revenue'] = display_df['total_revenue'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "$0.00")
            display_df['avg_rate'] = display_df['avg_rate'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "$0.00")
            display_df['avg_rate_per_mile'] = display_df['avg_rate_per_mile'].apply(lambda x: f"${x:.3f}" if pd.notna(x) else "$0.000")
            
            # Add action buttons
            for idx, broker in brokers_df.iterrows():
                if broker['broker_name'] != 'Direct Customer':
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                    
                    with col1:
                        st.write(broker['broker_name'])
                    with col2:
                        st.write(f"{broker['total_loads']} loads")
                    with col3:
                        st.write(f"${broker['total_revenue']:,.0f}")
                    with col4:
                        st.write(f"${broker['avg_rate_per_mile']:.3f}/mi")
                    with col5:
                        if st.button("📋 Details", key=f"broker_{idx}"):
                            show_broker_details(conn, broker['broker_name'])
            
        else:
            st.info("No broker data available. Start adding loads with broker information to see analysis.")
            
    except Exception as e:
        st.error(f"Error loading broker data: {str(e)}")
    
    # Add new broker
    with st.expander("➕ Add Broker Information"):
        with st.form("add_broker"):
            col1, col2 = st.columns(2)
            
            with col1:
                broker_name = st.text_input("Broker Name*")
                mc_number = st.text_input("MC Number")
                phone = st.text_input("Phone")
            
            with col2:
                email = st.text_input("Email")
                credit_score = st.number_input("Credit Score", min_value=0, max_value=850)
                preferred_lanes = st.text_area("Preferred Lanes")
            
            notes = st.text_area("Notes")
            
            if st.form_submit_button("Save Broker"):
                if broker_name:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT OR REPLACE INTO broker_analysis 
                        (broker_name, credit_score, notes, preferred_lanes)
                        VALUES (?, ?, ?, ?)
                    """, (broker_name, credit_score if credit_score > 0 else None, notes, preferred_lanes))
                    conn.commit()
                    st.success(f"Broker {broker_name} saved!")
                    st.rerun()

def show_revenue_analysis(conn):
    """Show detailed revenue analysis by broker"""
    st.header("💰 Revenue Analysis by Broker")
    
    # Time filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=date.today() - timedelta(days=90))
    with col2:
        end_date = st.date_input("End Date", value=date.today())
    
    # Revenue trend query
    revenue_query = """
        SELECT 
            DATE(pickup_date) as date,
            load_board_broker as broker,
            SUM(rate) as daily_revenue,
            COUNT(*) as load_count
        FROM shipments
        WHERE pickup_date BETWEEN ? AND ?
            AND status NOT IN ('Cancelled')
            AND load_board_broker IS NOT NULL
        GROUP BY DATE(pickup_date), load_board_broker
        ORDER BY date
    """
    
    try:
        revenue_df = pd.read_sql_query(revenue_query, conn, params=[start_date, end_date])
        
        if not revenue_df.empty:
            # Revenue over time chart
            fig = px.line(revenue_df, x='date', y='daily_revenue', color='broker',
                         title='Revenue Trend by Broker',
                         labels={'daily_revenue': 'Revenue ($)', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Broker comparison
            broker_summary = revenue_df.groupby('broker').agg({
                'daily_revenue': 'sum',
                'load_count': 'sum'
            }).sort_values('daily_revenue', ascending=False)
            
            # Pie chart of revenue distribution
            fig2 = px.pie(values=broker_summary['daily_revenue'], 
                         names=broker_summary.index,
                         title='Revenue Distribution by Broker')
            st.plotly_chart(fig2, use_container_width=True)
            
            # Detailed table
            st.subheader("Revenue Summary")
            summary_display = broker_summary.copy()
            summary_display['avg_per_load'] = summary_display['daily_revenue'] / summary_display['load_count']
            summary_display['daily_revenue'] = summary_display['daily_revenue'].apply(lambda x: f"${x:,.2f}")
            summary_display['avg_per_load'] = summary_display['avg_per_load'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(summary_display)
            
        else:
            st.info("No revenue data available for selected period.")
            
    except Exception as e:
        st.error(f"Error loading revenue data: {str(e)}")

def show_performance_metrics(conn):
    """Show broker performance metrics"""
    st.header("📈 Broker Performance Metrics")
    
    # Performance query
    performance_query = """
        SELECT 
            load_board_broker as broker,
            COUNT(*) as total_loads,
            SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) as delivered_loads,
            AVG(JULIANDAY(delivery_date) - JULIANDAY(pickup_date)) as avg_transit_days,
            SUM(rate) as total_revenue,
            AVG(rate) as avg_rate,
            AVG(miles) as avg_miles,
            AVG(CASE WHEN miles > 0 THEN rate/miles ELSE 0 END) as rpm
        FROM shipments
        WHERE load_board_broker IS NOT NULL
            AND status NOT IN ('Cancelled')
        GROUP BY load_board_broker
        HAVING total_loads > 5
        ORDER BY total_revenue DESC
    """
    
    try:
        perf_df = pd.read_sql_query(performance_query, conn)
        
        if not perf_df.empty:
            # Create performance score
            perf_df['delivery_rate'] = (perf_df['delivered_loads'] / perf_df['total_loads'] * 100)
            perf_df['performance_score'] = (
                perf_df['delivery_rate'] * 0.3 +
                (perf_df['rpm'] / perf_df['rpm'].max() * 100) * 0.4 +
                (perf_df['total_revenue'] / perf_df['total_revenue'].max() * 100) * 0.3
            )
            
            # Sort by performance score
            perf_df = perf_df.sort_values('performance_score', ascending=False)
            
            # Display top performers
            st.subheader("🏆 Top Performing Brokers")
            
            for idx, broker in perf_df.head(5).iterrows():
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns(5)
                    
                    with col1:
                        st.metric("Broker", broker['broker'])
                    with col2:
                        st.metric("Score", f"{broker['performance_score']:.1f}")
                    with col3:
                        st.metric("Delivery Rate", f"{broker['delivery_rate']:.1f}%")
                    with col4:
                        st.metric("RPM", f"${broker['rpm']:.3f}")
                    with col5:
                        st.metric("Revenue", f"${broker['total_revenue']:,.0f}")
                    
                    st.divider()
            
            # Performance comparison chart
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                name='Performance Score',
                x=perf_df['broker'][:10],
                y=perf_df['performance_score'][:10],
                yaxis='y',
                marker_color='lightblue'
            ))
            
            fig.add_trace(go.Scatter(
                name='RPM',
                x=perf_df['broker'][:10],
                y=perf_df['rpm'][:10],
                yaxis='y2',
                marker_color='red'
            ))
            
            fig.update_layout(
                title='Broker Performance Comparison',
                yaxis=dict(title='Performance Score'),
                yaxis2=dict(title='Rate per Mile ($)', overlaying='y', side='right'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.info("Not enough data for performance analysis. Need at least 5 loads per broker.")
            
    except Exception as e:
        st.error(f"Error loading performance data: {str(e)}")

def show_lead_generation(conn):
    """Show broker lead generation opportunities"""
    st.header("🎯 Broker Lead Generation")
    
    st.info("Identify potential new broker relationships based on lane analysis and market data")
    
    # Analyze most profitable lanes
    lane_query = """
        SELECT 
            origin_state || ' to ' || destination_state as lane,
            COUNT(*) as load_count,
            AVG(rate) as avg_rate,
            AVG(CASE WHEN miles > 0 THEN rate/miles ELSE 0 END) as avg_rpm,
            SUM(rate) as total_revenue
        FROM shipments
        WHERE status = 'Delivered'
            AND origin_state IS NOT NULL
            AND destination_state IS NOT NULL
        GROUP BY origin_state, destination_state
        HAVING load_count > 3
        ORDER BY avg_rpm DESC
        LIMIT 20
    """
    
    try:
        lanes_df = pd.read_sql_query(lane_query, conn)
        
        if not lanes_df.empty:
            st.subheader("🛣️ Most Profitable Lanes")
            
            # Display profitable lanes
            for idx, lane in lanes_df.head(10).iterrows():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**{lane['lane']}**")
                with col2:
                    st.write(f"RPM: ${lane['avg_rpm']:.3f}")
                with col3:
                    st.write(f"Avg: ${lane['avg_rate']:,.0f}")
                with col4:
                    st.write(f"Loads: {lane['load_count']}")
            
            # Recommendations
            st.subheader("💡 Broker Development Recommendations")
            
            recommendations = []
            
            # Find underserved lanes
            underserved = lanes_df[lanes_df['load_count'] < 10]
            if not underserved.empty:
                top_underserved = underserved.iloc[0]
                recommendations.append(
                    f"**Opportunity**: Lane {top_underserved['lane']} has high RPM "
                    f"(${top_underserved['avg_rpm']:.3f}) but only {top_underserved['load_count']} loads. "
                    f"Target brokers specializing in this lane."
                )
            
            # Find high-volume lanes
            high_volume = lanes_df[lanes_df['load_count'] > 20]
            if not high_volume.empty:
                recommendations.append(
                    f"**Volume Play**: Focus on brokers serving high-volume lanes for consistent freight."
                )
            
            # Display recommendations
            for rec in recommendations:
                st.success(rec)
            
            # Broker target list
            st.subheader("🎯 Target Broker Characteristics")
            
            target_characteristics = {
                "High RPM Brokers": "Focus on brokers averaging > $2.50/mile",
                "Quick Pay Brokers": "Target brokers offering 1-2 day quick pay",
                "Volume Brokers": "Seek brokers with 50+ loads per month",
                "Specialized Lanes": "Find brokers in your most profitable lanes",
                "Direct Shippers": "Pursue direct relationships to eliminate broker fees"
            }
            
            for characteristic, description in target_characteristics.items():
                st.write(f"• **{characteristic}**: {description}")
                
        else:
            st.info("Need more historical data to generate lead recommendations.")
            
    except Exception as e:
        st.error(f"Error generating leads: {str(e)}")

def show_lane_analysis(conn):
    """Show detailed lane analysis by broker"""
    st.header("📊 Lane Analysis by Broker")
    
    # Lane analysis query
    lane_broker_query = """
        SELECT 
            load_board_broker as broker,
            origin_city || ', ' || origin_state || ' → ' || 
            destination_city || ', ' || destination_state as lane,
            COUNT(*) as frequency,
            AVG(rate) as avg_rate,
            AVG(miles) as avg_miles,
            AVG(CASE WHEN miles > 0 THEN rate/miles ELSE 0 END) as avg_rpm
        FROM shipments
        WHERE load_board_broker IS NOT NULL
            AND status NOT IN ('Cancelled')
            AND origin_city IS NOT NULL
            AND destination_city IS NOT NULL
        GROUP BY load_board_broker, lane
        HAVING frequency > 1
        ORDER BY load_board_broker, frequency DESC
    """
    
    try:
        lane_df = pd.read_sql_query(lane_broker_query, conn)
        
        if not lane_df.empty:
            # Broker selection
            brokers = lane_df['broker'].unique()
            selected_broker = st.selectbox("Select Broker", ['All'] + list(brokers))
            
            if selected_broker != 'All':
                display_df = lane_df[lane_df['broker'] == selected_broker]
            else:
                display_df = lane_df
            
            # Lane frequency heatmap
            if not display_df.empty:
                # Create pivot table for heatmap
                pivot_data = display_df.pivot_table(
                    values='frequency',
                    index='broker',
                    columns='lane',
                    fill_value=0
                )
                
                # Limit to top lanes for readability
                if pivot_data.shape[1] > 15:
                    top_lanes = display_df.groupby('lane')['frequency'].sum().nlargest(15).index
                    pivot_data = pivot_data[top_lanes]
                
                # Create heatmap
                fig = px.imshow(pivot_data,
                              labels=dict(x="Lane", y="Broker", color="Frequency"),
                              title="Broker-Lane Frequency Heatmap",
                              aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed table
                st.subheader("Lane Details")
                
                display_table = display_df.copy()
                display_table['avg_rate'] = display_table['avg_rate'].apply(lambda x: f"${x:,.2f}")
                display_table['avg_rpm'] = display_table['avg_rpm'].apply(lambda x: f"${x:.3f}")
                display_table['avg_miles'] = display_table['avg_miles'].apply(lambda x: f"{x:,.0f}")
                
                st.dataframe(display_table[['broker', 'lane', 'frequency', 'avg_rate', 'avg_miles', 'avg_rpm']])
                
        else:
            st.info("No lane data available. Add more loads to see lane analysis.")
            
    except Exception as e:
        st.error(f"Error loading lane analysis: {str(e)}")

def show_broker_details(conn, broker_name):
    """Show detailed information for a specific broker"""
    with st.expander(f"Details for {broker_name}", expanded=True):
        # Get broker details
        broker_details = pd.read_sql_query("""
            SELECT * FROM broker_analysis WHERE broker_name = ?
        """, conn, params=[broker_name])
        
        if not broker_details.empty:
            broker = broker_details.iloc[0]
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Credit Score**: {broker['credit_score'] if broker['credit_score'] else 'Not rated'}")
                st.write(f"**First Load**: {broker['first_load_date']}")
                st.write(f"**Last Load**: {broker['last_load_date']}")
            
            with col2:
                st.write(f"**Preferred Lanes**: {broker['preferred_lanes'] if broker['preferred_lanes'] else 'Not specified'}")
                st.write(f"**Notes**: {broker['notes'] if broker['notes'] else 'No notes'}")
        
        # Recent loads
        recent_loads = pd.read_sql_query("""
            SELECT load_number, pickup_date, origin_city, destination_city, rate, status
            FROM shipments
            WHERE load_board_broker = ?
            ORDER BY pickup_date DESC
            LIMIT 10
        """, conn, params=[broker_name])
        
        if not recent_loads.empty:
            st.write("**Recent Loads:**")
            st.dataframe(recent_loads)