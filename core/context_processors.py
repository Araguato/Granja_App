from django.conf import settings
from .navigation import navigation_items

def user_context(request):
    """Adds user role, navigation information, and dashboard URLs to the template context."""
    context = {
        'is_supervisor': hasattr(request.user, 'is_superuser') and request.user.is_superuser,
        'is_operario': hasattr(request.user, 'is_staff') and request.user.is_staff,
        'DASHBOARD_URLS': {
            'supervisor': 'core:dashboard_supervisor',
            'operario': 'core:dashboard_operario',
            'admin': 'admin:index'
        }
    }
    
    # Add navigation items if user is authenticated
    if hasattr(request, 'user') and request.user.is_authenticated:
        context.update(navigation_items(request))
    
    return context
