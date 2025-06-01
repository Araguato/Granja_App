"""granja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import handler400, handler403, handler404, handler500

# Import our custom admin site
from avicola.custom_admin import custom_admin_site

# Custom error handlers
handler400 = 'core.views.handler400'
handler403 = 'core.views.handler403'
handler404 = 'core.views.handler404'
handler500 = 'core.views.handler500'

urlpatterns = [
    # Admin site - using our custom admin site
    path('admin/', custom_admin_site.urls),
    
    # API endpoints
    path('api/', include('api.urls', namespace='api')),
    
    # DRF browsable API auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    # Summernote editor
    path('summernote/', include('django_summernote.urls')),
]

# All apps in the project
app_urls = [
    # Core app (keep this last to avoid catching other URLs)
    ('', 'core.urls'),
    
    # Main apps
    ('avicola/', 'avicola.urls'),
    ('bot/', 'bot.urls'),
    ('faq/', 'faq.urls'),
    ('inventario/', 'inventario.urls'),
    ('produccion/', 'produccion.urls'),
    ('reportes/', 'reportes.urls'),
    ('respaldos/', 'respaldos.urls'),
    ('wiki/', 'wiki.urls'),
]

# Add all app URLs
for prefix, app_url in app_urls:
    try:
        urlpatterns.append(path(prefix, include(app_url)))
    except ModuleNotFoundError:
        print(f"Warning: Could not find URL module {app_url}")

# Static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add debug toolbar if DEBUG is True
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
