"""
Mobile Optimization Module for Smith & Williams Trucking TMS
Optimized for iOS and all mobile devices
"""
import streamlit as st

def apply_mobile_styles():
    """Apply mobile-optimized styles for all devices, especially iOS"""
    st.markdown("""
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes, viewport-fit=cover">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="SWT TMS">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="theme-color" content="#8B0000">
    <meta name="format-detection" content="telephone=no">
    
    <style>
        /* ============================================
           MOBILE OPTIMIZATION STYLES
           Designed for iOS and all mobile devices
        ============================================ */
        
        /* Responsive font sizes */
        @media screen and (max-width: 768px) {
            html {
                font-size: 14px !important;
                -webkit-text-size-adjust: 100% !important;
            }
        }
        
        /* iOS safe area handling */
        .stApp {
            padding-left: env(safe-area-inset-left) !important;
            padding-right: env(safe-area-inset-right) !important;
            padding-bottom: env(safe-area-inset-bottom) !important;
        }
        
        /* Mobile header optimization */
        @media screen and (max-width: 768px) {
            .stApp::before {
                font-size: 16px !important;
                height: 50px !important;
                padding: 0 10px !important;
            }
            
            .stApp {
                padding-top: 50px !important;
            }
        }
        
        /* Touch-friendly buttons */
        @media screen and (max-width: 768px) {
            .stButton button {
                min-height: 44px !important;
                min-width: 44px !important;
                padding: 12px 20px !important;
                font-size: 16px !important;
                -webkit-tap-highlight-color: rgba(139, 0, 0, 0.2) !important;
                touch-action: manipulation !important;
            }
            
            /* Prevent double-tap zoom on buttons */
            .stButton button {
                touch-action: manipulation !important;
            }
        }
        
        /* Mobile sidebar optimization */
        @media screen and (max-width: 768px) {
            section[data-testid="stSidebar"] {
                width: 280px !important;
                z-index: 999998 !important;
            }
            
            section[data-testid="stSidebar"] .block-container {
                padding: 1rem !important;
            }
            
            /* Sidebar toggle button - larger for mobile */
            button[kind="header"] {
                min-width: 44px !important;
                min-height: 44px !important;
            }
        }
        
        /* Touch-friendly input fields */
        @media screen and (max-width: 768px) {
            .stTextInput input, 
            .stTextArea textarea, 
            .stSelectbox select, 
            .stNumberInput input,
            .stDateInput input,
            .stTimeInput input {
                min-height: 44px !important;
                font-size: 16px !important;
                padding: 10px !important;
                -webkit-appearance: none !important;
                -moz-appearance: none !important;
                appearance: none !important;
                border-radius: 8px !important;
            }
            
            /* Prevent zoom on input focus (iOS) */
            input[type="text"],
            input[type="number"],
            input[type="email"],
            input[type="tel"],
            input[type="date"],
            input[type="time"],
            textarea,
            select {
                font-size: 16px !important;
            }
        }
        
        /* Mobile container optimization */
        @media screen and (max-width: 768px) {
            .main .block-container {
                padding: 1rem !important;
                max-width: 100% !important;
            }
            
            /* Stack columns on mobile */
            div[data-testid="column"] {
                width: 100% !important;
                flex: 0 0 100% !important;
                margin-bottom: 1rem !important;
            }
        }
        
        /* Mobile metrics optimization */
        @media screen and (max-width: 768px) {
            div[data-testid="metric-container"] {
                padding: 15px !important;
                margin-bottom: 10px !important;
            }
            
            div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
                font-size: 1.8rem !important;
            }
            
            div[data-testid="metric-container"] label {
                font-size: 0.9rem !important;
            }
        }
        
        /* Mobile table optimization */
        @media screen and (max-width: 768px) {
            .dataframe {
                font-size: 12px !important;
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
            
            .dataframe th,
            .dataframe td {
                padding: 8px !important;
                white-space: nowrap !important;
            }
            
            /* Horizontal scroll indicator */
            div[data-testid="stDataFrame"] {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
        }
        
        /* Mobile tabs optimization */
        @media screen and (max-width: 768px) {
            .stTabs [data-baseweb="tab"] {
                padding: 10px 15px !important;
                font-size: 14px !important;
                min-height: 44px !important;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                overflow-x: auto !important;
                -webkit-overflow-scrolling: touch !important;
            }
        }
        
        /* Mobile modal/dialog optimization */
        @media screen and (max-width: 768px) {
            div[data-testid="stModal"] {
                padding: 1rem !important;
            }
            
            div[data-testid="stModal"] .modal-body {
                padding: 1rem !important;
            }
        }
        
        /* Touch-friendly expandables */
        @media screen and (max-width: 768px) {
            .streamlit-expanderHeader {
                min-height: 44px !important;
                padding: 12px !important;
                font-size: 16px !important;
                -webkit-tap-highlight-color: rgba(139, 0, 0, 0.2) !important;
            }
        }
        
        /* Mobile-friendly spacing */
        @media screen and (max-width: 768px) {
            h1 { font-size: 1.5rem !important; }
            h2 { font-size: 1.3rem !important; }
            h3 { font-size: 1.1rem !important; }
            h4 { font-size: 1rem !important; }
            h5, h6 { font-size: 0.9rem !important; }
            
            p, span, label {
                line-height: 1.5 !important;
            }
        }
        
        /* Vernon badge in navbar - mobile optimized */
        @media screen and (max-width: 768px) {
            .stApp::after {
                top: 10px !important;
                right: 10px !important;
                padding: 5px 8px !important;
                font-size: 9px !important;
            }
        }
        
        /* Fix text truncation on mobile */
        @media screen and (max-width: 768px) {
            * {
                text-overflow: clip !important;
            }
            
            .stMarkdown, p, span, label {
                white-space: normal !important;
                word-wrap: break-word !important;
            }
        }
        
        /* Smooth scrolling for mobile */
        * {
            -webkit-overflow-scrolling: touch !important;
            scroll-behavior: smooth !important;
        }
        
        /* Prevent text selection issues on mobile */
        @media screen and (max-width: 768px) {
            * {
                -webkit-user-select: text !important;
                -webkit-touch-callout: default !important;
            }
            
            button, .stButton {
                -webkit-user-select: none !important;
                -webkit-touch-callout: none !important;
            }
        }
        
        /* iOS-specific fixes */
        @supports (-webkit-touch-callout: none) {
            /* Fix for iOS input zoom */
            input, textarea, select {
                font-size: 16px !important;
            }
            
            /* Fix for iOS button appearance */
            button, input[type="button"], input[type="submit"] {
                -webkit-appearance: none !important;
                border-radius: 8px !important;
            }
        }
        
        /* Landscape mode optimization */
        @media screen and (max-width: 768px) and (orientation: landscape) {
            .stApp::before {
                height: 40px !important;
                font-size: 14px !important;
            }
            
            .stApp {
                padding-top: 40px !important;
            }
            
            .main .block-container {
                padding: 0.5rem 1rem !important;
            }
        }
        
        /* High contrast mode for better visibility */
        @media screen and (max-width: 768px) {
            .stMarkdown, p, span, label {
                font-weight: 600 !important;
            }
            
            .stButton button {
                font-weight: 700 !important;
                letter-spacing: 0.5px !important;
            }
        }
        
        /* Loading spinner optimization for mobile */
        @media screen and (max-width: 768px) {
            .stSpinner > div {
                width: 40px !important;
                height: 40px !important;
            }
        }
        
        /* File uploader mobile optimization */
        @media screen and (max-width: 768px) {
            section[data-testid="stFileUploadDropzone"] {
                min-height: 100px !important;
                padding: 20px !important;
            }
        }
        
        /* Mobile-friendly alerts */
        @media screen and (max-width: 768px) {
            .stAlert {
                padding: 12px !important;
                font-size: 14px !important;
            }
        }
        
        /* Responsive grid system */
        @media screen and (max-width: 480px) {
            /* Extra small devices */
            .row-widget.stHorizontal {
                flex-direction: column !important;
            }
            
            .row-widget.stHorizontal > div {
                width: 100% !important;
                margin-bottom: 0.5rem !important;
            }
        }
        
        /* Performance optimizations */
        @media screen and (max-width: 768px) {
            /* Reduce animations on mobile for better performance */
            * {
                animation-duration: 0.2s !important;
                transition-duration: 0.2s !important;
            }
            
            /* Disable hover effects on touch devices */
            @media (hover: none) {
                *:hover {
                    transform: none !important;
                    box-shadow: none !important;
                }
            }
        }
        
        /* Accessibility improvements for mobile */
        @media screen and (max-width: 768px) {
            /* Larger touch targets */
            a, button, input, select, textarea {
                min-height: 44px !important;
                min-width: 44px !important;
            }
            
            /* Better focus indicators */
            *:focus {
                outline: 3px solid #8B0000 !important;
                outline-offset: 2px !important;
            }
        }
    </style>
    """, unsafe_allow_html=True)

def create_mobile_header():
    """Create a mobile-optimized header"""
    st.markdown("""
    <div style='display: none;' id='mobile-header'>
        <style>
            @media screen and (max-width: 768px) {
                #mobile-header {
                    display: block !important;
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    height: 50px;
                    background: linear-gradient(135deg, #8B0000 0%, #660000 100%);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 0 15px;
                    z-index: 999999;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
                }
                
                #mobile-header .logo {
                    font-size: 18px;
                    font-weight: 900;
                    letter-spacing: 1px;
                }
                
                #mobile-header .menu-btn {
                    width: 44px;
                    height: 44px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                }
            }
        </style>
        <div class='logo'>SWT TMS</div>
        <div class='menu-btn'>☰</div>
    </div>
    """, unsafe_allow_html=True)

def optimize_for_mobile():
    """Main function to apply all mobile optimizations"""
    apply_mobile_styles()
    create_mobile_header()
    
    # Add PWA manifest link for installable web app
    st.markdown("""
    <link rel="manifest" href="data:application/json;base64,ewogICAgIm5hbWUiOiAiU1dUIFRNUyBIdWIiLAogICAgInNob3J0X25hbWUiOiAiU1dUIFRNUyIsCiAgICAiZGVzY3JpcHRpb24iOiAiU21pdGggJiBXaWxsaWFtcyBUcnVja2luZyBUTVMiLAogICAgInN0YXJ0X3VybCI6ICIvIiwKICAgICJkaXNwbGF5IjogInN0YW5kYWxvbmUiLAogICAgImJhY2tncm91bmRfY29sb3IiOiAiIzAwMDAwMCIsCiAgICAidGhlbWVfY29sb3IiOiAiIzhCMDAwMCIsCiAgICAib3JpZW50YXRpb24iOiAicG9ydHJhaXQiCn0=">
    """, unsafe_allow_html=True)
    
    # Add iOS icons
    st.markdown("""
    <link rel="apple-touch-icon" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==">
    <link rel="apple-touch-startup-image" href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==">
    """, unsafe_allow_html=True)

def is_mobile():
    """Detect if the user is on a mobile device"""
    # This is a placeholder - Streamlit doesn't directly expose user agent
    # But the CSS media queries will handle the actual responsive behavior
    return True  # Always apply mobile optimizations for consistency