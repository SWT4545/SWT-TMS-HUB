# Smith & Williams Trucking - TMS Hub

## Project Overview
A comprehensive Transportation Management System (TMS) built with Streamlit for Smith & Williams Trucking LLC. This system provides complete shipment tracking, dispatch management, billing, and reporting capabilities.

## Version Information
- **Current Version**: 2.0.0 (Refactored)
- **Previous Version**: 1.0.0 (Legacy)
- **Last Refactored**: August 18, 2025
- **Refactored by**: Claude AI Assistant

## Project Structure (Organized)
```
SWT-TMS-HUB/
├── main_app.py              # New main application entry point
├── app.py                   # Legacy app (references missing modules)
├── tms_app.py              # Legacy comprehensive app
├── config/
│   ├── database.py         # Database configuration and initialization
│   └── COMPLETE_SYSTEM_TEMPLATE_PACKAGE.py  # Styling and components
├── modules/
│   ├── auth.py             # Authentication and authorization
│   └── ui_components.py    # UI components and styling
├── views/
│   ├── executive.py        # Executive dashboard
│   ├── data_entry.py       # Data entry and management
│   ├── driver.py           # Driver portal
│   └── user_management.py  # User management (admin only)
├── data/
│   └── swt_tms.db         # Persistent SQLite database
└── assets/
    ├── logos/             # Company logos
    └── videos/            # Video assets
```

## Database Information
- **Type**: SQLite
- **Location**: `data/swt_tms.db`
- **Persistence**: ✅ Fixed - Database now persists between sessions
- **Backup**: Automatic backup functionality included

## Fixed Issues
1. **Data Persistence Bug**: Database now uses persistent file storage instead of in-memory
2. **Missing Modules**: Created proper module structure with all required components
3. **Code Organization**: Refactored monolithic files into organized modules and views
4. **Duplicate Code**: Eliminated code duplication through modular architecture

## Key Features
- **Role-based Access Control**: Super User, CEO, Admin, Dispatcher, Driver, Customer, Accounting
- **Persistent Database**: SQLite database with WAL mode for better performance
- **Modular Architecture**: Clean separation of concerns
- **Responsive UI**: Modern styling with CSS variables and animations
- **Security**: Vernon protection branding and secure authentication

## Default Login Credentials
- **Username**: `Brandon`
- **Password**: `ceo123`
- **Role**: `super_user` (full system access)

## Running the Application

### Using the New Refactored App
```bash
streamlit run main_app.py
```

### Using Legacy App (has missing modules)
```bash
streamlit run app.py  # Will show import errors
```

### Using Comprehensive Legacy App
```bash
streamlit run tms_app.py  # Works but no modular structure
```

## Dependencies
Install required packages:
```bash
pip install -r requirements.txt
```

## Database Management
- Database is automatically initialized on first run
- Backup functionality available in System Settings
- Performance indexes created for optimal query speed

## Module Descriptions

### Config Modules
- `database.py`: Database connection, initialization, and backup utilities
- `COMPLETE_SYSTEM_TEMPLATE_PACKAGE.py`: Company info, styling, and reusable components

### Core Modules
- `auth.py`: User authentication, session management, role-based access
- `ui_components.py`: UI helpers, styling, and common components

### View Modules
- `executive.py`: Executive dashboard with KPIs and analytics
- `data_entry.py`: Forms for creating shipments, customers, drivers, trucks
- `driver.py`: Driver portal for viewing loads and updating status
- `user_management.py`: Admin interface for managing users and permissions

## Recent Improvements
1. **Database Persistence**: Fixed data loss issue - database now persists in `data/` directory
2. **Modular Structure**: Separated concerns into logical modules
3. **Error Handling**: Added comprehensive error handling and logging
4. **UI/UX**: Modern design with consistent styling and animations
5. **Security**: Enhanced authentication and role-based permissions

## Database Schema
The system includes the following main tables:
- `users` - System users with role-based access
- `customers` - Customer information and billing details
- `shipments` - Load/shipment tracking
- `dispatches` - Driver assignments and status
- `drivers` - Driver information and credentials
- `trucks` - Fleet management
- `carriers` - Carrier/partner information
- `invoices` - Billing and payment tracking
- `system_settings` - Application configuration

## Development Notes
- All modules use proper error handling and logging
- Database connections are properly managed and closed
- Session state is properly initialized and managed
- UI components are reusable and consistent
- Role-based access control is enforced throughout

## Testing Commands
```bash
# Test database initialization
python3 -c "from config.database import init_database; init_database()"

# Test module imports
python3 -c "from modules.auth import authenticate_user; print('Auth module OK')"

# Run the application
streamlit run main_app.py
```

## Future Enhancements
- Complete remaining view modules (shipments, dispatch, billing, reports)
- Add API endpoints for mobile app integration
- Implement real-time GPS tracking
- Add email/SMS notification system
- Create customer portal
- Add advanced reporting and analytics