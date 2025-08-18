# Super-User TMS - System Guide

## Overview
The Super-User Transportation Management System (TMS) is a unified platform that provides role-based access to different operational views while maintaining a single codebase.

## User Roles & Access

### 1. Super-User (Brandon Only)
- **Username:** Brandon
- **Password:** ceo123
- **Access:** Can toggle between ALL three views
- **Special Features:**
  - View toggle in sidebar
  - User management capabilities
  - Full system oversight

### 2. Individual Role Users

#### Executive Role
- **Access:** Executive dashboard only
- **Features:** KPIs, analytics, financial overview, fleet management

#### Data Entry Role  
- **Access:** Historical Data Feeder only
- **Features:** Conversational AI for load entry, payment reconciliation

#### Driver Role
- **Access:** Driver View only
- **Features:** Load tracking, GPS, document upload, HOS status

## Sample User Accounts (For Testing)

| Username | Password | Role | Full Name |
|----------|----------|------|-----------|
| Brandon | ceo123 | super_user | Brandon Smith (CEO) |
| driver1 | driver123 | driver | John Driver |
| dataentry1 | data123 | data_entry | Sarah DataEntry |
| exec1 | exec123 | executive | Mike Executive |

## Key Features

### Three Operating Views

1. **Executive View**
   - Real-time KPIs and metrics
   - Revenue analytics
   - Payment reconciliation status
   - Fleet management
   - Goal setting and tracking

2. **Historical Data Feeder**
   - Conversational AI assistant
   - Guided load entry workflow
   - Intelligent payment reconciliation
   - Automatic rate calculations
   - Carrier-specific payment logic

3. **Driver View**
   - Current load information
   - GPS tracking (Motive API integration)
   - Document upload (Vector API)
   - Hours of Service tracking
   - Check-in functionality

### Intelligent Payment Logic

- **CanAmex Loads:**
  - 12% fee deduction
  - Weekly payment cycle (Sunday-Saturday)
  - Pays following week

- **Factored Loads:**
  - 3% factoring fee
  - Next-day payment
  - Daily reconciliation

### API Integrations (Ready for Keys)

1. **Motive API** - GPS tracking and ELD data
2. **Vector API** - Document management
3. **Google Maps API** - Distance calculations
4. **Truckstop.com API** - Load board integration (future)
5. **QuickBooks API** - Accounting integration (future)

## User Management (Super-User Only)

As the super-user, Brandon can:
1. Add new users with specific roles
2. Modify existing user roles
3. Delete users (except himself)
4. View all system users

Access user management by clicking "Manage Users" button in the sidebar when logged in as Brandon.

## Running the Application

```bash
streamlit run super_user_tms.py
```

Then navigate to http://localhost:8501

## Configuration

1. Copy `.env.template` to `.env`
2. Add your API keys:
   - Motive API key
   - Vector API credentials
   - Google Maps API key
   - Other service keys as needed

## Database

The system uses SQLite database (`super_user_tms.db`) with tables for:
- Users (role-based access)
- Loads (comprehensive tracking)
- Payments (reconciliation)
- Equipment (fleet management)
- Geofences (automated check-ins)
- Chat history (AI conversations)

## Security Notes

- All passwords are hashed using SHA256
- Session management for user authentication
- Role-based access control
- API keys stored in environment variables

## Support

For issues or questions, contact Brandon Smith at (951) 437-5474