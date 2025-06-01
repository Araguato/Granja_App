#!/usr/bin/env python
"""
Script to check URL configurations in each app.
"""
import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_root = str(Path(__file__).resolve().parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
import django
django.setup()

from django.apps import apps
from django.urls import get_resolver

def check_app_urls():
    """Check URL configurations for all installed apps."""
    print("\n=== Checking App URL Configurations ===\n")
    
    # Get all installed apps
    installed_apps = [app_config.name for app_config in apps.get_app_configs() 
                     if not app_config.name.startswith('django.')]
    
    # Get the root URL resolver
    resolver = get_resolver()
    
    # Get all URL patterns
    all_patterns = []
    
    def get_patterns(patterns, prefix=''):
        """Recursively get all URL patterns."""
        result = []
        for pattern in patterns:
            if hasattr(pattern, 'pattern'):
                if hasattr(pattern, 'url_patterns'):  # URLResolver
                    new_prefix = f"{prefix}{str(pattern.pattern).lstrip('^').rstrip('$')}/"
                    result.extend(get_patterns(pattern.url_patterns, new_prefix))
                else:  # URLPattern
                    result.append(f"{prefix}{pattern.pattern}")
        return result
    
    all_patterns = get_patterns(resolver.url_patterns)
    
    # Check each app
    for app in installed_apps:
        app_name = app.split('.')[-1]
        app_patterns = [p for p in all_patterns if f'/{app_name}/' in p or p.startswith(f'{app_name}/')]
        
        if app_patterns:
            print(f"✅ {app}:")
            for i, pattern in enumerate(app_patterns[:3], 1):
                print(f"   {i}. {pattern}")
            if len(app_patterns) > 3:
                print(f"   ... and {len(app_patterns) - 3} more patterns")
        else:
            print(f"⚠️  {app}: No URL patterns found")
    
    print("\n=== URL Configuration Check Complete ===")

if __name__ == "__main__":
    check_app_urls()
