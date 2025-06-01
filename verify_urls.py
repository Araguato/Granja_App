#!/usr/bin/env python
"""
Django script to verify URL configurations.
Run with: python manage.py shell < verify_urls.py
"""
import sys
from pathlib import Path

# Add the project directory to Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Set up Django environment
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
import django
django.setup()

from django.conf import settings
from django.urls import get_resolver, URLPattern, URLResolver

# List of all installed apps with URL configurations
INSTALLED_APPS_WITH_URLS = [
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

def get_url_patterns(url_patterns, prefix=''):
    """Recursively get all URL patterns with their names."""
    patterns = []
    for pattern in url_patterns:
        if isinstance(pattern, URLPattern):
            patterns.append({
                'pattern': f"{prefix}{str(pattern.pattern).lstrip('^').rstrip('$')}",
                'name': pattern.name,
                'app_name': pattern.namespace or '',
                'type': 'URLPattern'
            })
        elif isinstance(pattern, URLResolver):
            new_prefix = f"{prefix}{str(pattern.pattern).lstrip('^').rstrip('$')}/"
            patterns.extend(get_url_patterns(pattern.url_patterns, new_prefix))
    return patterns

def check_app_urls():
    """Check URL configurations for all installed apps."""
    print("\n=== Verifying URL Configurations ===\n")
    
    # Get the root URL resolver
    resolver = get_resolver()
    
    # Get all URL patterns
    all_patterns = get_url_patterns(resolver.url_patterns)
    
    # Group patterns by app
    app_patterns = {app: [] for app in INSTALLED_APPS_WITH_URLS}
    
    for pattern in all_patterns:
        for app in INSTALLED_APPS_WITH_URLS:
            if f"{app}:" in pattern.get('name', '') or app in pattern.get('pattern', ''):
                app_patterns[app].append(pattern)
    
    # Print results
    all_ok = True
    for app in INSTALLED_APPS_WITH_URLS:
        patterns = app_patterns[app]
        if not patterns:
            print(f"⚠️  {app}: No URL patterns found")
            all_ok = False
        else:
            print(f"✅ {app}: Found {len(patterns)} URL pattern(s)")
            for i, pattern in enumerate(patterns[:3], 1):  # Show first 3 patterns
                print(f"   {i}. {pattern['pattern']} (name='{pattern.get('name', '')}')")
            if len(patterns) > 3:
                print(f"   ... and {len(patterns) - 3} more")
    
    print("\n=== Verification Complete ===")
    if all_ok:
        print("✅ All apps have valid URL configurations!")
    else:
        print("❌ Some issues were found. Please check the output above.")

if __name__ == "__main__":
    check_app_urls()
