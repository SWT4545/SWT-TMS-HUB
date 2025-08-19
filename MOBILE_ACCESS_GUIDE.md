# Mobile Access Guide - SWT TMS Hub

## Quick Start for Mobile Access

### Method 1: Using the Batch File (Easiest)
1. Double-click `start_mobile_server.bat`
2. Note the IP address shown (172.20.10.6)
3. On your mobile device, open browser
4. Go to: `http://172.20.10.6:8501`

### Method 2: Using Python Script
```bash
python mobile_server.py
```

### Method 3: Manual Start
```bash
streamlit run main_app.py --server.address 0.0.0.0
```

## Troubleshooting

### Mobile Device Can't Connect?

#### 1. Check Network
- Ensure mobile device is on **same WiFi network** as computer
- Both devices must be on same network (not cellular data)

#### 2. Windows Firewall
You may need to allow port 8501 through Windows Firewall:

**Option A: Windows Defender Firewall GUI**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature"
3. Click "Allow another app"
4. Browse to Python.exe
5. Check both Private and Public networks

**Option B: Command Line (Run as Administrator)**
```cmd
netsh advfirewall firewall add rule name="Streamlit TMS" dir=in action=allow protocol=TCP localport=8501
```

#### 3. Check IP Address
Your IP may change. To find current IP:
```cmd
ipconfig | findstr IPv4
```

#### 4. Alternative Ports
If port 8501 is blocked, try:
- Port 8080: `streamlit run main_app.py --server.port 8080`
- Port 3000: `streamlit run main_app.py --server.port 3000`

## Mobile Browser Requirements
- **iOS**: Safari 12+ or Chrome
- **Android**: Chrome 80+ or Firefox
- JavaScript must be enabled
- Cookies must be enabled

## Security Notes
- Only accessible on local network
- Not accessible from internet
- Use VPN for remote access if needed

## Current Network Configuration
- **Local IP**: 172.20.10.6
- **Port**: 8501
- **URL**: http://172.20.10.6:8501

## Login Credentials
- **Username**: Brandon
- **Password**: ceo123

## Features on Mobile
✅ Fully responsive design
✅ Touch-optimized interface
✅ iOS/Android compatible
✅ PWA support (installable)
✅ Offline capability (limited)