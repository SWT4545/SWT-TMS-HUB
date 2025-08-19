"""
SWT App Compliance Validator
Ensures all apps follow Smith & Williams Trucking standards
"""

import os
import sys

def validate_app(app_file):
    """Validates if app follows SWT standards"""
    
    if not os.path.exists(app_file):
        print(f"❌ File not found: {app_file}")
        return False
    
    with open(app_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Company Name": "Smith & Williams Trucking LLC" in content,
        "Vernon Protection": "VERNON" in content,
        "Primary Color": "#1e3a8a" in content,
        "Video Logo Code": "company_logo_animation.mp4.MOV" in content,
        "Gradient Background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" in content,
        "White Logo": "swt_logo_white.png" in content,
        "Copyright Notice": "© 2025 Smith & Williams Trucking LLC" in content,
        "Session State Auth": "st.session_state.get('authenticated'" in content,
        "Error Handling": "try:" in content and "except:" in content,
        "Database Init": "CREATE TABLE" in content or "init_database" in content,
    }
    
    print("\n" + "="*50)
    print("SWT APP COMPLIANCE CHECK")
    print("="*50)
    print(f"File: {app_file}\n")
    
    passed = 0
    failed = 0
    
    for check, result in checks.items():
        if result:
            print(f"✅ {check}")
            passed += 1
        else:
            print(f"❌ {check}")
            failed += 1
    
    print("\n" + "-"*50)
    score = (passed / len(checks)) * 100
    print(f"Score: {score:.1f}% ({passed}/{len(checks)} checks passed)")
    
    if score >= 80:
        print("✅ APP IS COMPLIANT WITH SWT STANDARDS")
    else:
        print("⚠️ APP NEEDS UPDATES TO MEET STANDARDS")
        print("\nMissing elements should be added from template")
    
    print("="*50)
    
    return score >= 80

if __name__ == "__main__":
    if len(sys.argv) > 1:
        validate_app(sys.argv[1])
    else:
        print("Usage: python validate_swt_app.py <app_file.py>")
        print("Example: python validate_swt_app.py my_new_app.py")