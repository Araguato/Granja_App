from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from django.apps import apps
import sys

class Command(BaseCommand):
    help = 'Verifies URL configurations for all installed apps'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Verifying URL Configurations ===\n'))
        
        # Get all installed apps that might have URLs
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        
        # Get the root URL resolver
        resolver = get_resolver()
        
        # Get all URL patterns
        all_patterns = self.get_url_patterns(resolver.url_patterns)
        
        # Group patterns by app
        app_patterns = {app: [] for app in installed_apps}
        
        for pattern in all_patterns:
            for app in installed_apps:
                if f"{app.split('.')[-1]}:" in pattern.get('name', '') or app.split('.')[-1] in pattern.get('pattern', ''):
                    app_patterns[app].append(pattern)
        
        # Print results
        all_ok = True
        for app in installed_apps:
            patterns = app_patterns[app]
            if not patterns:
                self.stdout.write(self.style.WARNING(f"⚠️  {app}: No URL patterns found"))
                all_ok = False
            else:
                self.stdout.write(self.style.SUCCESS(f"✅ {app}: Found {len(patterns)} URL pattern(s)"))
                for i, pattern in enumerate(patterns[:3], 1):  # Show first 3 patterns
                    self.stdout.write(f"   {i}. {pattern['pattern']} (name='{pattern.get('name', '')}')")
                if len(patterns) > 3:
                    self.stdout.write(f"   ... and {len(patterns) - 3} more")
        
        self.stdout.write('\n' + self.style.SUCCESS('=== Verification Complete ==='))
        if all_ok:
            self.stdout.write(self.style.SUCCESS('✅ All apps have valid URL configurations!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Some issues were found. Please check the output above.'))
    
    def get_url_patterns(self, url_patterns, prefix=''):
        """Recursively get all URL patterns with their names."""
        patterns = []
        for pattern in url_patterns:
            if hasattr(pattern, 'pattern'):
                if isinstance(pattern, URLPattern):
                    patterns.append({
                        'pattern': f"{prefix}{str(pattern.pattern).lstrip('^').rstrip('$')}",
                        'name': pattern.name or '',
                        'type': 'URLPattern'
                    })
                elif isinstance(pattern, URLResolver):
                    new_prefix = f"{prefix}{str(pattern.pattern).lstrip('^').rstrip('$')}/"
                    patterns.extend(self.get_url_patterns(pattern.url_patterns, new_prefix))
        return patterns
