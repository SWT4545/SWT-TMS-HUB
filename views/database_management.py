"""
Database Management Module for Smith & Williams Trucking TMS
Allows manual editing of database records with full CRUD operations
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from config.database import get_connection
import sqlite3
import json

def show_database_management():
    """Main database management interface"""
    st.title("🗄️ Database Management")
    
    # Security check - only super_user and admin can access
    user_role = st.session_state.get('user_role', '')
    if user_role not in ['super_user', 'admin']:
        st.error("⛔ Access Denied: Database management requires admin privileges")
        return
    
    st.warning("⚠️ **Warning**: Direct database editing can affect system integrity. Always backup before making changes.")
    
    conn = get_connection()
    
    # Quick actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Backup Database", use_container_width=True):
            backup_database(conn)
    
    with col2:
        if st.button("🔄 Refresh Schema", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("📊 Database Stats", use_container_width=True):
            show_database_stats(conn)
    
    with col4:
        if st.button("🧹 Cleanup", use_container_width=True):
            cleanup_database(conn)
    
    # Main tabs
    tabs = st.tabs([
        "📋 Tables",
        "✏️ Edit Records",
        "➕ Insert Records",
        "🗑️ Delete Records",
        "🔍 Query Builder",
        "📜 SQL Console",
        "🔧 Maintenance"
    ])
    
    with tabs[0]:
        show_tables_overview(conn)
    
    with tabs[1]:
        edit_records(conn)
    
    with tabs[2]:
        insert_records(conn)
    
    with tabs[3]:
        delete_records(conn)
    
    with tabs[4]:
        query_builder(conn)
    
    with tabs[5]:
        sql_console(conn)
    
    with tabs[6]:
        database_maintenance(conn)

def show_tables_overview(conn):
    """Display overview of all database tables"""
    st.header("📋 Database Tables")
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        selected_table = st.selectbox(
            "Select Table",
            [table[0] for table in tables]
        )
        
        if selected_table:
            # Get table info
            cursor.execute(f"PRAGMA table_info({selected_table})")
            columns = cursor.fetchall()
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {selected_table}")
            row_count = cursor.fetchone()[0]
            
            # Display table info
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Rows", f"{row_count:,}")
            
            with col2:
                st.metric("Total Columns", len(columns))
            
            # Show column details
            st.subheader("Column Structure")
            
            column_data = []
            for col in columns:
                column_data.append({
                    'Column': col[1],
                    'Type': col[2],
                    'Not Null': '✓' if col[3] else '',
                    'Default': col[4] if col[4] else '',
                    'Primary Key': '🔑' if col[5] else ''
                })
            
            st.dataframe(pd.DataFrame(column_data), use_container_width=True, hide_index=True)
            
            # Show sample data
            st.subheader("Sample Data (First 10 rows)")
            
            try:
                query = f"SELECT * FROM {selected_table} LIMIT 10"
                df = pd.read_sql_query(query, conn)
                
                if not df.empty:
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Table is empty")
                    
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")

def edit_records(conn):
    """Edit existing database records"""
    st.header("✏️ Edit Records")
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_table = st.selectbox(
                "Select Table to Edit",
                [table[0] for table in tables],
                key="edit_table"
            )
        
        with col2:
            record_id = st.text_input("Record ID (Primary Key)")
        
        if selected_table and record_id:
            # Get table columns
            cursor.execute(f"PRAGMA table_info({selected_table})")
            columns = cursor.fetchall()
            
            # Find primary key column
            pk_column = None
            for col in columns:
                if col[5]:  # Primary key flag
                    pk_column = col[1]
                    break
            
            if not pk_column:
                pk_column = 'id'  # Default assumption
            
            # Fetch the record
            try:
                query = f"SELECT * FROM {selected_table} WHERE {pk_column} = ?"
                cursor.execute(query, (record_id,))
                record = cursor.fetchone()
                
                if record:
                    st.success(f"Found record with {pk_column} = {record_id}")
                    
                    # Create edit form
                    st.subheader("Edit Values")
                    
                    with st.form("edit_form"):
                        updated_values = {}
                        
                        for i, col in enumerate(columns):
                            col_name = col[1]
                            col_type = col[2]
                            current_value = record[i] if i < len(record) else None
                            
                            # Skip primary key
                            if col[5]:
                                st.text_input(col_name, value=str(current_value), disabled=True)
                                continue
                            
                            # Create appropriate input based on type
                            if 'INT' in col_type.upper():
                                updated_values[col_name] = st.number_input(
                                    col_name,
                                    value=int(current_value) if current_value is not None else 0
                                )
                            elif 'REAL' in col_type.upper() or 'DECIMAL' in col_type.upper():
                                updated_values[col_name] = st.number_input(
                                    col_name,
                                    value=float(current_value) if current_value is not None else 0.0,
                                    format="%.2f"
                                )
                            elif 'DATE' in col_type.upper():
                                if current_value:
                                    try:
                                        date_value = datetime.strptime(str(current_value), '%Y-%m-%d').date()
                                    except:
                                        date_value = date.today()
                                else:
                                    date_value = date.today()
                                updated_values[col_name] = st.date_input(col_name, value=date_value)
                            elif 'BOOL' in col_type.upper():
                                updated_values[col_name] = st.checkbox(
                                    col_name,
                                    value=bool(current_value) if current_value is not None else False
                                )
                            else:  # TEXT or other
                                updated_values[col_name] = st.text_area(
                                    col_name,
                                    value=str(current_value) if current_value is not None else ""
                                )
                        
                        if st.form_submit_button("Update Record", type="primary"):
                            # Build UPDATE query
                            set_clause = ", ".join([f"{k} = ?" for k in updated_values.keys()])
                            update_query = f"UPDATE {selected_table} SET {set_clause} WHERE {pk_column} = ?"
                            
                            try:
                                cursor.execute(
                                    update_query,
                                    list(updated_values.values()) + [record_id]
                                )
                                conn.commit()
                                st.success(f"Record updated successfully!")
                                st.balloons()
                            except Exception as e:
                                st.error(f"Update failed: {str(e)}")
                else:
                    st.warning(f"No record found with {pk_column} = {record_id}")
                    
            except Exception as e:
                st.error(f"Error fetching record: {str(e)}")

def insert_records(conn):
    """Insert new records into database"""
    st.header("➕ Insert New Records")
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        selected_table = st.selectbox(
            "Select Table",
            [table[0] for table in tables],
            key="insert_table"
        )
        
        if selected_table:
            # Get table columns
            cursor.execute(f"PRAGMA table_info({selected_table})")
            columns = cursor.fetchall()
            
            st.subheader(f"Insert into {selected_table}")
            
            with st.form("insert_form"):
                values = {}
                
                for col in columns:
                    col_name = col[1]
                    col_type = col[2]
                    is_pk = col[5]
                    is_required = col[3]
                    
                    # Skip auto-increment primary keys
                    if is_pk and 'INTEGER' in col_type.upper():
                        continue
                    
                    # Create appropriate input
                    if 'INT' in col_type.upper():
                        values[col_name] = st.number_input(
                            f"{col_name}{'*' if is_required else ''}",
                            value=0
                        )
                    elif 'REAL' in col_type.upper() or 'DECIMAL' in col_type.upper():
                        values[col_name] = st.number_input(
                            f"{col_name}{'*' if is_required else ''}",
                            value=0.0,
                            format="%.2f"
                        )
                    elif 'DATE' in col_type.upper():
                        values[col_name] = st.date_input(
                            f"{col_name}{'*' if is_required else ''}",
                            value=date.today()
                        )
                    elif 'TIMESTAMP' in col_type.upper():
                        use_current = st.checkbox(f"Use current time for {col_name}")
                        if use_current:
                            values[col_name] = datetime.now()
                        else:
                            values[col_name] = st.text_input(
                                f"{col_name}{'*' if is_required else ''}"
                            )
                    elif 'BOOL' in col_type.upper():
                        values[col_name] = st.checkbox(
                            f"{col_name}{'*' if is_required else ''}"
                        )
                    else:  # TEXT or other
                        if col_name in ['password', 'password_hash']:
                            values[col_name] = st.text_input(
                                f"{col_name}{'*' if is_required else ''}",
                                type="password"
                            )
                        else:
                            values[col_name] = st.text_area(
                                f"{col_name}{'*' if is_required else ''}",
                                height=70
                            )
                
                if st.form_submit_button("Insert Record", type="primary"):
                    # Build INSERT query
                    columns_str = ", ".join(values.keys())
                    placeholders = ", ".join(["?" for _ in values])
                    insert_query = f"INSERT INTO {selected_table} ({columns_str}) VALUES ({placeholders})"
                    
                    try:
                        cursor.execute(insert_query, list(values.values()))
                        conn.commit()
                        st.success(f"Record inserted successfully! New ID: {cursor.lastrowid}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Insert failed: {str(e)}")

def delete_records(conn):
    """Delete records from database"""
    st.header("🗑️ Delete Records")
    
    st.error("⚠️ **Danger Zone**: Deletions are permanent and cannot be undone!")
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        col1, col2 = st.columns(2)
        
        with col1:
            selected_table = st.selectbox(
                "Select Table",
                [table[0] for table in tables],
                key="delete_table"
            )
        
        with col2:
            delete_mode = st.radio(
                "Delete Mode",
                ["Single Record", "Multiple Records", "Conditional Delete"]
            )
        
        if selected_table:
            if delete_mode == "Single Record":
                record_id = st.text_input("Record ID (Primary Key)")
                
                if record_id:
                    # Find primary key column
                    cursor.execute(f"PRAGMA table_info({selected_table})")
                    columns = cursor.fetchall()
                    
                    pk_column = None
                    for col in columns:
                        if col[5]:
                            pk_column = col[1]
                            break
                    
                    if not pk_column:
                        pk_column = 'id'
                    
                    # Show record to be deleted
                    try:
                        query = f"SELECT * FROM {selected_table} WHERE {pk_column} = ?"
                        df = pd.read_sql_query(query, conn, params=[record_id])
                        
                        if not df.empty:
                            st.warning("Record to be deleted:")
                            st.dataframe(df, use_container_width=True)
                            
                            confirm = st.checkbox("I understand this action cannot be undone")
                            
                            if confirm:
                                if st.button("Delete Record", type="primary"):
                                    cursor.execute(
                                        f"DELETE FROM {selected_table} WHERE {pk_column} = ?",
                                        (record_id,)
                                    )
                                    conn.commit()
                                    st.success("Record deleted successfully!")
                        else:
                            st.info("No record found with that ID")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            elif delete_mode == "Multiple Records":
                st.write("Enter comma-separated IDs to delete multiple records")
                record_ids = st.text_input("Record IDs (e.g., 1,2,3)")
                
                if record_ids:
                    ids_list = [id.strip() for id in record_ids.split(',')]
                    
                    # Find primary key column
                    cursor.execute(f"PRAGMA table_info({selected_table})")
                    columns = cursor.fetchall()
                    
                    pk_column = None
                    for col in columns:
                        if col[5]:
                            pk_column = col[1]
                            break
                    
                    if not pk_column:
                        pk_column = 'id'
                    
                    # Show records to be deleted
                    placeholders = ','.join(['?' for _ in ids_list])
                    query = f"SELECT * FROM {selected_table} WHERE {pk_column} IN ({placeholders})"
                    
                    try:
                        df = pd.read_sql_query(query, conn, params=ids_list)
                        
                        if not df.empty:
                            st.warning(f"Records to be deleted ({len(df)} found):")
                            st.dataframe(df, use_container_width=True)
                            
                            confirm = st.checkbox("I understand this action cannot be undone")
                            
                            if confirm:
                                if st.button("Delete All Records", type="primary"):
                                    cursor.execute(
                                        f"DELETE FROM {selected_table} WHERE {pk_column} IN ({placeholders})",
                                        ids_list
                                    )
                                    conn.commit()
                                    st.success(f"{cursor.rowcount} records deleted!")
                        else:
                            st.info("No records found with those IDs")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            else:  # Conditional Delete
                st.write("Delete records based on conditions")
                
                # Get columns for condition building
                cursor.execute(f"PRAGMA table_info({selected_table})")
                columns = cursor.fetchall()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    column = st.selectbox(
                        "Column",
                        [col[1] for col in columns]
                    )
                
                with col2:
                    operator = st.selectbox(
                        "Operator",
                        ["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN", "IS NULL", "IS NOT NULL"]
                    )
                
                with col3:
                    if operator not in ["IS NULL", "IS NOT NULL"]:
                        value = st.text_input("Value")
                    else:
                        value = None
                
                if column and operator:
                    # Build WHERE clause
                    if operator in ["IS NULL", "IS NOT NULL"]:
                        where_clause = f"{column} {operator}"
                        params = []
                    elif operator == "IN":
                        values = [v.strip() for v in value.split(',')]
                        placeholders = ','.join(['?' for _ in values])
                        where_clause = f"{column} IN ({placeholders})"
                        params = values
                    else:
                        where_clause = f"{column} {operator} ?"
                        params = [value]
                    
                    # Preview records to be deleted
                    if st.button("Preview Records"):
                        query = f"SELECT * FROM {selected_table} WHERE {where_clause}"
                        try:
                            df = pd.read_sql_query(query, conn, params=params)
                            
                            if not df.empty:
                                st.warning(f"Records matching condition ({len(df)} found):")
                                st.dataframe(df, use_container_width=True)
                                
                                confirm = st.checkbox("I understand this action cannot be undone", key="confirm_conditional")
                                
                                if confirm:
                                    if st.button("Delete Matching Records", type="primary"):
                                        cursor.execute(
                                            f"DELETE FROM {selected_table} WHERE {where_clause}",
                                            params
                                        )
                                        conn.commit()
                                        st.success(f"{cursor.rowcount} records deleted!")
                            else:
                                st.info("No records match the condition")
                                
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

def query_builder(conn):
    """Visual query builder"""
    st.header("🔍 Query Builder")
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' 
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    if tables:
        # Query type
        query_type = st.radio(
            "Query Type",
            ["SELECT", "UPDATE", "JOIN"],
            horizontal=True
        )
        
        if query_type == "SELECT":
            selected_table = st.selectbox(
                "From Table",
                [table[0] for table in tables]
            )
            
            if selected_table:
                # Get columns
                cursor.execute(f"PRAGMA table_info({selected_table})")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                # Select columns
                selected_columns = st.multiselect(
                    "Select Columns",
                    column_names,
                    default=column_names[:3] if len(column_names) > 3 else column_names
                )
                
                # WHERE conditions
                st.subheader("WHERE Conditions (Optional)")
                
                conditions = []
                num_conditions = st.number_input("Number of conditions", 0, 5, 0)
                
                for i in range(num_conditions):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        if i > 0:
                            logic = st.selectbox(f"Logic {i}", ["AND", "OR"], key=f"logic_{i}")
                        else:
                            logic = "WHERE"
                    
                    with col2:
                        col = st.selectbox(f"Column {i+1}", column_names, key=f"col_{i}")
                    
                    with col3:
                        op = st.selectbox(f"Operator {i+1}", ["=", "!=", ">", "<", ">=", "<=", "LIKE"], key=f"op_{i}")
                    
                    with col4:
                        val = st.text_input(f"Value {i+1}", key=f"val_{i}")
                    
                    if col and op and val:
                        if i == 0:
                            conditions.append(f"{col} {op} '{val}'")
                        else:
                            conditions.append(f"{logic} {col} {op} '{val}'")
                
                # ORDER BY
                col1, col2 = st.columns(2)
                
                with col1:
                    order_by = st.selectbox("Order By", [""] + column_names)
                
                with col2:
                    order_dir = st.radio("Direction", ["ASC", "DESC"], horizontal=True)
                
                # LIMIT
                limit = st.number_input("Limit Results", 0, 1000, 100)
                
                # Build query
                if selected_columns:
                    query = f"SELECT {', '.join(selected_columns)} FROM {selected_table}"
                    
                    if conditions:
                        query += f" WHERE {' '.join(conditions)}"
                    
                    if order_by:
                        query += f" ORDER BY {order_by} {order_dir}"
                    
                    if limit > 0:
                        query += f" LIMIT {limit}"
                    
                    # Display query
                    st.code(query, language='sql')
                    
                    # Execute query
                    if st.button("Execute Query", type="primary"):
                        try:
                            df = pd.read_sql_query(query, conn)
                            st.success(f"Query returned {len(df)} rows")
                            st.dataframe(df, use_container_width=True)
                            
                            # Export option
                            csv = df.to_csv(index=False)
                            st.download_button(
                                "Download as CSV",
                                csv,
                                "query_results.csv",
                                "text/csv"
                            )
                        except Exception as e:
                            st.error(f"Query failed: {str(e)}")

def sql_console(conn):
    """Direct SQL console for advanced users"""
    st.header("📜 SQL Console")
    
    st.warning("⚠️ Direct SQL execution - Use with caution!")
    
    # SQL input
    sql_query = st.text_area(
        "Enter SQL Query",
        height=200,
        placeholder="SELECT * FROM shipments WHERE status = 'Active';"
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        execute_btn = st.button("▶️ Execute", type="primary", use_container_width=True)
    
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    with col3:
        # Query templates
        template = st.selectbox(
            "Templates",
            ["", "SELECT", "INSERT", "UPDATE", "DELETE", "CREATE TABLE", "ALTER TABLE"]
        )
    
    if template:
        templates = {
            "SELECT": "SELECT column1, column2\nFROM table_name\nWHERE condition\nORDER BY column1 ASC;",
            "INSERT": "INSERT INTO table_name (column1, column2)\nVALUES (value1, value2);",
            "UPDATE": "UPDATE table_name\nSET column1 = value1\nWHERE condition;",
            "DELETE": "DELETE FROM table_name\nWHERE condition;",
            "CREATE TABLE": "CREATE TABLE table_name (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    column1 TEXT NOT NULL,\n    column2 INTEGER,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);",
            "ALTER TABLE": "ALTER TABLE table_name\nADD COLUMN column_name datatype;"
        }
        
        if template in templates:
            st.code(templates[template], language='sql')
    
    if execute_btn and sql_query:
        try:
            cursor = conn.cursor()
            
            # Check if it's a SELECT query
            if sql_query.strip().upper().startswith('SELECT'):
                df = pd.read_sql_query(sql_query, conn)
                st.success(f"Query executed successfully! Returned {len(df)} rows")
                st.dataframe(df, use_container_width=True)
                
                # Export option
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download Results as CSV",
                    csv,
                    "sql_results.csv",
                    "text/csv"
                )
            else:
                # Execute non-SELECT query
                cursor.execute(sql_query)
                conn.commit()
                st.success(f"Query executed successfully! {cursor.rowcount} rows affected")
                
        except Exception as e:
            st.error(f"SQL Error: {str(e)}")
    
    # Query history
    with st.expander("📜 Recent Queries"):
        if 'query_history' not in st.session_state:
            st.session_state.query_history = []
        
        if sql_query and execute_btn:
            st.session_state.query_history.insert(0, {
                'time': datetime.now().strftime('%H:%M:%S'),
                'query': sql_query[:100] + '...' if len(sql_query) > 100 else sql_query
            })
            st.session_state.query_history = st.session_state.query_history[:10]
        
        for entry in st.session_state.query_history:
            st.text(f"[{entry['time']}] {entry['query']}")

def database_maintenance(conn):
    """Database maintenance operations"""
    st.header("🔧 Database Maintenance")
    
    cursor = conn.cursor()
    
    # Database info
    st.subheader("Database Information")
    
    # Get database size
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    db_size = cursor.fetchone()[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Database Size", f"{db_size / 1024 / 1024:.2f} MB")
    
    with col2:
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        st.metric("Total Tables", table_count)
    
    with col3:
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index'")
        index_count = cursor.fetchone()[0]
        st.metric("Total Indexes", index_count)
    
    st.markdown("---")
    
    # Maintenance operations
    st.subheader("Maintenance Operations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔧 VACUUM Database", use_container_width=True):
            try:
                conn.execute("VACUUM")
                st.success("Database vacuumed successfully!")
            except Exception as e:
                st.error(f"Vacuum failed: {str(e)}")
        
        if st.button("📊 ANALYZE Database", use_container_width=True):
            try:
                conn.execute("ANALYZE")
                st.success("Database analyzed successfully!")
            except Exception as e:
                st.error(f"Analyze failed: {str(e)}")
        
        if st.button("🔍 Check Integrity", use_container_width=True):
            try:
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()[0]
                if result == "ok":
                    st.success("✅ Database integrity check passed!")
                else:
                    st.error(f"Integrity check failed: {result}")
            except Exception as e:
                st.error(f"Check failed: {str(e)}")
    
    with col2:
        if st.button("📈 Reindex Database", use_container_width=True):
            try:
                conn.execute("REINDEX")
                st.success("Database reindexed successfully!")
            except Exception as e:
                st.error(f"Reindex failed: {str(e)}")
        
        if st.button("🗑️ Clear Orphaned Records", use_container_width=True):
            clear_orphaned_records(conn)
        
        if st.button("📝 Export Schema", use_container_width=True):
            export_schema(conn)
    
    # Table statistics
    st.subheader("Table Statistics")
    
    cursor.execute("""
        SELECT 
            name as table_name,
            (SELECT COUNT(*) FROM sqlite_master WHERE type='index' AND tbl_name=m.name) as indexes
        FROM sqlite_master m
        WHERE type='table'
        ORDER BY name
    """)
    
    tables = cursor.fetchall()
    
    table_stats = []
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            row_count = cursor.fetchone()[0]
            table_stats.append({
                'Table': table[0],
                'Rows': row_count,
                'Indexes': table[1]
            })
        except:
            continue
    
    if table_stats:
        df = pd.DataFrame(table_stats)
        st.dataframe(df, use_container_width=True, hide_index=True)

def backup_database(conn):
    """Create database backup"""
    try:
        from config.database import backup_database as backup_db
        backup_path = backup_db()
        st.success(f"✅ Database backed up successfully to: {backup_path}")
    except Exception as e:
        st.error(f"Backup failed: {str(e)}")

def show_database_stats(conn):
    """Show database statistics"""
    cursor = conn.cursor()
    
    stats = {}
    
    # Get table counts
    tables = ['shipments', 'customers', 'drivers', 'trucks', 'invoices', 'users']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        except:
            stats[table] = 0
    
    # Display stats
    st.info(f"""
    **Database Statistics:**
    - Shipments: {stats.get('shipments', 0)}
    - Customers: {stats.get('customers', 0)}
    - Drivers: {stats.get('drivers', 0)}
    - Trucks: {stats.get('trucks', 0)}
    - Invoices: {stats.get('invoices', 0)}
    - Users: {stats.get('users', 0)}
    """)

def cleanup_database(conn):
    """Clean up database"""
    cursor = conn.cursor()
    
    try:
        # Remove old logs
        cursor.execute("""
            DELETE FROM system_learning 
            WHERE learning_date < date('now', '-90 days')
        """)
        
        # Remove old GPS data
        cursor.execute("""
            DELETE FROM motive_gps_data 
            WHERE created_at < date('now', '-30 days')
        """)
        
        conn.commit()
        st.success("✅ Database cleaned up successfully!")
        
    except Exception as e:
        st.error(f"Cleanup failed: {str(e)}")

def clear_orphaned_records(conn):
    """Clear orphaned records from database"""
    cursor = conn.cursor()
    
    try:
        # Find orphaned dispatches
        cursor.execute("""
            DELETE FROM dispatches 
            WHERE shipment_id NOT IN (SELECT id FROM shipments)
        """)
        
        orphaned_dispatches = cursor.rowcount
        
        # Find orphaned invoices
        cursor.execute("""
            DELETE FROM invoices 
            WHERE customer_id NOT IN (SELECT id FROM customers)
        """)
        
        orphaned_invoices = cursor.rowcount
        
        conn.commit()
        
        st.success(f"""
        ✅ Orphaned records cleared:
        - Dispatches: {orphaned_dispatches}
        - Invoices: {orphaned_invoices}
        """)
        
    except Exception as e:
        st.error(f"Clear failed: {str(e)}")

def export_schema(conn):
    """Export database schema"""
    cursor = conn.cursor()
    
    # Get all CREATE statements
    cursor.execute("""
        SELECT sql FROM sqlite_master 
        WHERE type IN ('table', 'index', 'trigger')
        ORDER BY type, name
    """)
    
    schema = cursor.fetchall()
    
    schema_text = "-- Database Schema Export\n"
    schema_text += f"-- Generated: {datetime.now()}\n\n"
    
    for item in schema:
        if item[0]:
            schema_text += item[0] + ";\n\n"
    
    st.download_button(
        "📥 Download Schema",
        schema_text,
        "database_schema.sql",
        "text/plain"
    )
    
    st.success("Schema ready for download!")

# Export the function
__all__ = ['show_database_management']