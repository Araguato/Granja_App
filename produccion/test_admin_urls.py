from django.urls import path, include
from django.http import JsonResponse
from django.contrib import admin

def test_admin_urls(request):
    """View to test admin URL resolution"""
    from django.urls.resolvers import get_resolver
    
    # Get all registered URLs
    resolver = get_resolver()
    admin_urls = []
    
    # Find admin URLs
    for url_pattern in resolver.url_patterns:
        if hasattr(url_pattern, 'url_patterns'):
            for pattern in url_pattern.url_patterns:
                if 'admin' in str(pattern.pattern):
                    admin_urls.append({
                        'pattern': str(pattern.pattern),
                        'callback': str(pattern.callback),
                        'name': pattern.name
                    })
    
    # Check Galpon admin URL
    galpon_admin_url = None
    try:
        galpon_admin_url = f"/admin/produccion/galpon/"
        resolver.resolve(galpon_admin_url)
    except Exception as e:
        galpon_admin_url = f"Error resolving URL: {str(e)}"
    
    return JsonResponse({
        'admin_urls': admin_urls,
        'galpon_admin_url': galpon_admin_url,
        'admin_site': str(admin.site),
        'admin_site_class': str(admin.site.__class__)
    })
