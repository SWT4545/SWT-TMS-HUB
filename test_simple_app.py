"""
Simple Test App - No Video Loading
"""
import streamlit as st
from modules.auth_simple import show_simple_login, check_authentication

st.set_page_config(
    page_title="TMS - Simple Test",
    page_icon="🚚",
    layout="wide"
)

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not st.session_state.authenticated:
        show_simple_login()
    else:
        st.success("✅ Successfully logged in!")
        st.title("TMS Dashboard")
        st.write("This is the main dashboard")
        
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()