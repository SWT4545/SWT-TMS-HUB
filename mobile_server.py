"""
Mobile Server Launcher for Smith & Williams TMS Hub
Automatically detects IP and provides QR code for easy mobile access
"""
import socket
import streamlit as st
import subprocess
import sys
import os

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Connect to an external server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    ip = get_local_ip()
    port = 8501
    
    print("=" * 50)
    print("SMITH & WILLIAMS TMS HUB - MOBILE SERVER")
    print("=" * 50)
    print(f"\nServer starting on: http://{ip}:{port}")
    print("\nIMPORTANT: To access from mobile devices:")
    print(f"1. Ensure your phone is on the same WiFi network")
    print(f"2. Open browser and go to: http://{ip}:{port}")
    print(f"3. If it doesn't load, check Windows Firewall settings")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    # Launch streamlit with network access
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "main_app.py",
        "--server.address", "0.0.0.0",
        "--server.port", str(port),
        "--server.headless", "true"
    ])

if __name__ == "__main__":
    main()