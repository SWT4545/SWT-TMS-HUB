# Streamlit Cloud Deployment Guide

## Deploy to Streamlit Cloud for Mobile Access Anywhere

### Why Streamlit Cloud?
- Access from ANY device (phone, tablet, computer)
- No network configuration needed
- No firewall issues
- Works on cellular data
- Free hosting

---

## Step-by-Step Deployment

### 1. Your Repository is Ready
✅ Code is already on GitHub: https://github.com/SWT4545/SWT-TMS-HUB

### 2. Go to Streamlit Cloud
1. Visit: https://streamlit.io/cloud
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub

### 3. Deploy Your App
1. Click "New app"
2. Select repository: `SWT4545/SWT-TMS-HUB`
3. Branch: `main`
4. Main file path: `main_app.py`
5. Click "Deploy"

### 4. Wait for Deployment
- Takes 2-5 minutes
- You'll get a URL like: `https://swt-tms-hub.streamlit.app`

### 5. Access from Mobile
- Open the URL on ANY device
- Works on iPhone, iPad, Android
- No WiFi network setup needed

---

## Environment Variables (Optional)
If you need to set environment variables:

1. In Streamlit Cloud dashboard
2. Click ⚙️ Settings
3. Add secrets in TOML format:
```toml
DATABASE_URL = "your_database_url"
API_KEY = "your_api_key"
```

---

## Current Local Access
While waiting for cloud deployment, access locally:

### From Computer:
- http://localhost:8501

### From Mobile (Same WiFi):
- http://172.20.10.6:8501

### Requirements:
- Mobile device on same WiFi network
- Windows Firewall allows port 8501

---

## Troubleshooting Cloud Deployment

### If deployment fails:
1. Check requirements.txt is present
2. Ensure all imports are installed
3. Check Python version compatibility

### If mobile access doesn't work locally:
1. Verify devices on same network
2. Check Windows Firewall:
   - Allow Python through firewall
   - Allow port 8501
3. Try different port (8080, 3000)

---

## Benefits of Cloud Deployment

✅ **Access Anywhere**: No network configuration
✅ **Always Available**: 24/7 uptime
✅ **Automatic Updates**: Pushes to GitHub auto-deploy
✅ **Mobile Optimized**: Works on all devices
✅ **Secure**: HTTPS by default
✅ **Free Tier**: Perfect for your needs

---

## Quick Deploy Button
[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=https://github.com/SWT4545/SWT-TMS-HUB)

Click the button above to deploy directly!