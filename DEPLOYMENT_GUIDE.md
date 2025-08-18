# 🚀 DEPLOYMENT GUIDE FOR SWT-TMS-HUB

## Step-by-Step GitHub & Streamlit Cloud Deployment

### 📋 Prerequisites
- Git installed on your computer
- GitHub account
- Streamlit Cloud account (free at share.streamlit.io)

---

## PART 1: GitHub Setup

### Step 1: Initialize Git Repository
Open terminal/command prompt in `C:\SWTTMSHUB` and run:

```bash
# Initialize git repository
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Smith & Williams TMS Hub"
```

### Step 2: Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon → **New repository**
3. Repository settings:
   - Name: `SWT-TMS-HUB`
   - Description: "Smith & Williams Trucking Transportation Management System"
   - Visibility: **Private** (recommended for business data)
   - Do NOT initialize with README (we already have one)
4. Click **Create repository**

### Step 3: Connect and Push to GitHub
After creating the repository, GitHub will show you commands. Use these:

```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/SWT-TMS-HUB.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## PART 2: Streamlit Cloud Deployment

### Step 1: Access Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account

### Step 2: Create New App
1. Click **New app**
2. Fill in the deployment form:
   - **Repository**: `YOUR_USERNAME/SWT-TMS-HUB`
   - **Branch**: `main`
   - **Main file path**: `app.py` (or `super_user_tms.py` for monolithic version)
3. Click **Advanced settings**

### Step 3: Configure Secrets
In the **Secrets** section, paste this configuration:

```toml
# API Keys
MOTIVE_API_KEY = "your_motive_api_key_here"
VECTOR_API_KEY = "your_vector_api_key_here"
VECTOR_API_SECRET = "your_vector_api_secret_here"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key_here"

# Truckstop.com API (when available)
TRUCKSTOP_CLIENT_ID = "your_truckstop_client_id_here"
TRUCKSTOP_CLIENT_SECRET = "your_truckstop_client_secret_here"

# QuickBooks API (when available)
QUICKBOOKS_CLIENT_ID = "your_quickbooks_client_id_here"
QUICKBOOKS_CLIENT_SECRET = "your_quickbooks_client_secret_here"
QUICKBOOKS_REDIRECT_URI = "your_app_url/callback"

# Database Configuration
DATABASE_PATH = "super_user_tms.db"

# Session Configuration
SESSION_SECRET_KEY = "generate_a_random_secret_key_here"

# Company Settings
COMPANY_NAME = "Smith & Williams Trucking"
COMPANY_EMAIL = "brandon@swtrucking.com"
COMPANY_PHONE = "(951) 437-5474"
```

### Step 4: Deploy
1. Click **Deploy!**
2. Wait for the app to build (first deployment takes 5-10 minutes)
3. Once deployed, you'll get a URL like: `https://swt-tms-hub.streamlit.app`

---

## PART 3: Environment Variables (Local Development)

For local development, create `.env` file:

```bash
# Copy template
cp .env.template .env

# Edit with your actual keys
# Never commit .env to GitHub!
```

---

## PART 4: Database Initialization

The app will automatically create the database on first run. Default admin credentials:
- Username: `Brandon`
- Password: `ceo123`

**⚠️ IMPORTANT**: Change the password after first login!

---

## 📱 Access Your Deployed App

### Public URL
Your app will be available at:
```
https://[your-app-name].streamlit.app
```

### Custom Domain (Optional)
You can configure a custom domain in Streamlit Cloud settings:
1. Go to app settings
2. Click "Custom domain"
3. Follow CNAME configuration instructions

---

## 🔄 Updating the App

To update your deployed app:

```bash
# Make changes locally
# Then commit and push
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will automatically redeploy when you push to GitHub.

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **Database Errors**
   - Database is created fresh on Streamlit Cloud
   - Use Streamlit secrets for persistent data

3. **API Key Errors**
   - Verify all secrets are properly configured
   - Check for typos in secret names

4. **Deployment Fails**
   - Check Streamlit Cloud logs
   - Verify `requirements.txt` is complete
   - Ensure no local file paths are hardcoded

---

## 📞 Support Contacts

- **Technical Issues**: Check Streamlit Cloud logs first
- **Business Support**: Brandon Smith - (951) 437-5474
- **Security Concerns**: Vernon - IT Head of Data Security

---

## 🔒 Security Checklist

- [ ] Changed default password
- [ ] Configured all API keys as secrets
- [ ] Repository set to private
- [ ] `.env` file in `.gitignore`
- [ ] No sensitive data in code
- [ ] Vernon Security Protocol active

---

**Last Updated**: January 2025
**System Version**: 1.0.0
**Protected by Vernon - IT Head of Data Security**