from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

app_name = 'avicola_api'

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'lotes', api_views.LoteViewSet)
router.register(r'galpones', api_views.GalponViewSet)
router.register(r'seguimientos', api_views.SeguimientoDiarioViewSet)

urlpatterns = router.urls

# Add any additional API endpoints here
urlpatterns += [
    # Add any custom API endpoints here
]
