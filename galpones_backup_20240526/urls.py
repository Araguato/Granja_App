from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configuración del router para las vistas basadas en ViewSet
router = DefaultRouter()
router.register(r'galpones', views.GalponViewSet, basename='galpon')

# URL patterns
urlpatterns = [
    # Incluye las rutas generadas por el router
    path('api/', include(router.urls)),
    
    # Otras URLs de la aplicación galpones (si son necesarias)
    # path('', views.otra_vista, name='otra_vista'),
]
