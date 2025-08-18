# SWT-TMS-HUB
## Smith & Williams Trucking - Transportation Management System

A comprehensive Super-User Transportation Management System with role-based access control, AI-powered data entry, and real-time fleet management capabilities.

![Smith & Williams Trucking](assets/logos/swt_logo.png)

## 🚀 Features

### Three Operating Modes
- **Executive View** - KPIs, analytics, and business intelligence
- **Historical Data Feeder** - AI-assisted data entry with Florida, your TMS assistant
- **Driver View** - Mobile-friendly interface for field operations

### Key Capabilities
- 🔐 Role-based access control (Super-User, Executive, Data Entry, Driver)
- 💬 Conversational AI for guided data entry
- 📊 Real-time metrics and analytics
- 🗺️ GPS tracking and geofencing
- 📄 Document management
- 💰 Intelligent payment reconciliation
- 🛡️ Vernon Security Protocol - IT Head of Data Security

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: SQLite
- **APIs**: Motive, Vector, Google Maps
- **Deployment**: Streamlit Cloud

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Streamlit Cloud account
- API keys for integrated services

## 🔧 Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/SWT-TMS-HUB.git
cd SWT-TMS-HUB
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file from template:
```bash
cp .env.template .env
# Edit .env with your API keys
```

5. Run the application:
```bash
streamlit run app.py
```

## 🚀 Deployment to Streamlit Cloud

1. **Fork or Clone this Repository** to your GitHub account

2. **Go to Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Create New App**:
   - Click "New app"
   - Select your repository: `SWT-TMS-HUB`
   - Select branch: `main`
   - Main file path: `app.py`

4. **Configure Secrets**:
   In Streamlit Cloud settings, add your secrets:
   ```toml
   # .streamlit/secrets.toml format
   MOTIVE_API_KEY = "your_motive_api_key"
   VECTOR_API_KEY = "your_vector_api_key"
   VECTOR_API_SECRET = "your_vector_api_secret"
   GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"
   DATABASE_PATH = "super_user_tms.db"
   SESSION_SECRET_KEY = "your_session_secret_key"
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait for the app to build and deploy

## 📁 Project Structure

```
SWT-TMS-HUB/
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
├── .env.template          # Environment variables template
├── README.md              # Project documentation
│
├── modules/               # Modular components
│   ├── __init__.py
│   ├── auth.py           # Authentication system
│   ├── database.py       # Database models and connections
│   ├── ui_components.py  # UI components and styling
│   ├── api_services.py   # External API integrations
│   └── ai_assistant.py   # Florida AI assistant
│
├── views/                 # Application views
│   ├── __init__.py
│   ├── executive.py      # Executive dashboard
│   ├── data_entry.py     # Historical data feeder
│   ├── driver.py         # Driver interface
│   └── user_management.py # User management
│
├── assets/               # Static assets
│   ├── logos/           # Company logos
│   └── videos/          # Animation files
│
└── config/              # Configuration files
    └── settings.py      # Application settings
```

## 👤 Default Login

For initial setup:
- Username: `Brandon`
- Password: `ceo123`

**Important**: Change the default password after first login!

## 🔒 Security

- All passwords are hashed using SHA256
- Session management for authentication
- Role-based access control
- Vernon Security Protocol monitors data integrity
- API keys stored as environment variables

## 📊 Database Schema

The system uses SQLite with the following main tables:
- `users` - User accounts and roles
- `loads` - Load tracking and management
- `payments` - Payment reconciliation
- `equipment` - Fleet management
- `geofences` - Location-based automation
- `chat_history` - AI conversation logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

© 2025 Smith & Williams Trucking LLC - All Rights Reserved

## 🛡️ Data Protection

**All data is protected by Vernon - IT Head of Data Security**
- Self-Fixing Protocol Active
- System Integrity Monitored 24/7

## 📞 Support

For support, contact:
- Brandon Smith (CEO)
- Email: brandon@swtrucking.com
- Phone: (951) 437-5474

---
Built with ❤️ for Smith & Williams Trucking