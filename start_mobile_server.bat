@echo off
echo ====================================
echo Smith & Williams TMS Hub - Mobile Server
echo ====================================
echo.
echo Starting server for mobile access...
echo.
echo Your computer's IP address is: 172.20.10.6
echo.
echo On your mobile device, open browser and go to:
echo http://172.20.10.6:8501
echo.
echo Make sure your mobile device is on the same WiFi network!
echo.
echo Press Ctrl+C to stop the server
echo ====================================
echo.
streamlit run main_app.py --server.address 0.0.0.0 --server.port 8501