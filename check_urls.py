#!/usr/bin/env python
"""
Script to verify URL configurations in Django apps.
"""
import importlib
from pathlib import Path

# List of all apps in the project
APPS = [
    'core',
    'api',
    'avicola',
    'bot',
    'faq',
    'galpones',
    'inventario',
    'produccion',
    'reportes',
    'respaldos',
    'wiki',
]

def check_urls_module(app_name):
    """Check if the app has a urls.py file and if it defines app_name."""
    try:
        # Try to import the urls module
        module_path = f"{app_name}.urls"
        module = importlib.import_module(module_path)
        
        # Check if app_name is defined
        if hasattr(module, 'app_name'):
            return True, module.app_name
        return False, None
    except ImportError as e:
        return None, str(e)

def main():
    """Main function to check all apps."""
    print("\n=== Verifying URL Configurations ===\n")
    
    all_ok = True
    for app in APPS:
        app_path = Path(app.replace('.', '/'))
        urls_path = app_path / 'urls.py'
        
        if not urls_path.exists():
            print(f"❌ {app}: No urls.py found")
            all_ok = False
            continue
            
        has_app_name, app_name_or_error = check_urls_module(app)
        
        if has_app_name is None:
            print(f"❌ {app}: Error importing urls.py - {app_name_or_error}")
            all_ok = False
        elif has_app_name:
            print(f"✅ {app}: OK (app_name='{app_name_or_error}')")
        else:
            print(f"⚠️  {app}: urls.py exists but no app_name defined")
            all_ok = False
    
    print("\n=== Verification Complete ===")
    if all_ok:
        print("✅ All URL configurations are valid!")
    else:
        print("❌ Some issues were found. Please check the output above.")

if __name__ == "__main__":
    main()
