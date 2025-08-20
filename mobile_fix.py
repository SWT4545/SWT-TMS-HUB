"""
Mobile Access Fix - Comprehensive Solution
Ensures the app works on mobile devices
"""
import streamlit as st
import socket
import subprocess
import sys

def get_network_ip():
    """Get the actual network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_mobile_server():
    """Start server with proper mobile configuration"""
    ip = get_network_ip()
    print(f"""
    ===============================================
    MOBILE ACCESS ENABLED
    ===============================================
    
    Your app is running at:
    
    Local: http://localhost:8501
    Network: http://{ip}:8501
    
    TO ACCESS FROM MOBILE:
    1. Make sure your phone is on the SAME WiFi network
    2. Open browser on your phone
    3. Go to: http://{ip}:8501
    
    If it doesn't work:
    - Check Windows Firewall (allow Python)
    - Try turning off Windows Firewall temporarily
    - Make sure both devices are on same network
    
    ===============================================
    """)
    
    # Start Streamlit with all network interfaces
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "main_app.py",
        "--server.address", "0.0.0.0",
        "--server.port", "8501",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false",
        "--server.enableWebsocketCompression", "false",
        "--browser.gatherUsageStats", "false",
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    start_mobile_server()