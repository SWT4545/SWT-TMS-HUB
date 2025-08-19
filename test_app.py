"""
Simple test app to verify Streamlit is working
"""
import streamlit as st

st.set_page_config(
    page_title="TMS Hub Test",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 SWT TMS Hub - Test Mode")
st.success("✅ Streamlit is working!")

# Test basic functionality
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Status", "Online", "✓")
    
with col2:
    st.metric("Version", "2.0.0", None)
    
with col3:
    st.metric("Database", "Connected", "✓")

# Test form
st.markdown("---")
st.subheader("Test Login Form")

with st.form("test_login"):
    username = st.text_input("Username", value="Brandon")
    password = st.text_input("Password", type="password", value="ceo123")
    submit = st.form_submit_button("Login")
    
    if submit:
        st.success(f"Test login for {username} successful!")

st.info("If you can see this page, Streamlit is working correctly. The issue may be with imports or dependencies.")