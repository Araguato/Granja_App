from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

from .views import (
    UserViewSet, GranjaViewSet, GalponViewSet, LoteViewSet, 
    SeguimientoDiarioViewSet, MortalidadDiariaViewSet, 
    MortalidadSemanalViewSet, ProveedorViewSet, RazaViewSet, 
    AlimentoViewSet, VacunaViewSet, InsumoViewSet, 
    GuiaDesempenoRazaViewSet, CategoryViewSet, ArticleViewSet,
    FAQCategoryViewSet, FAQViewSet, BotConversationViewSet,
    EstadisticasViewSet, ComparacionRazasView
)

# Configuración del router para la API
router = routers.DefaultRouter()

# Register your viewsets here
router.register(r'usuarios', UserViewSet)
router.register(r'granjas', GranjaViewSet)
router.register(r'galpones', GalponViewSet)
router.register(r'lotes', LoteViewSet)
router.register(r'seguimientos', SeguimientoDiarioViewSet)
router.register(r'mortalidad-diaria', MortalidadDiariaViewSet)
router.register(r'mortalidad-semanal', MortalidadSemanalViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'razas', RazaViewSet)
router.register(r'alimentos', AlimentoViewSet)
router.register(r'vacunas', VacunaViewSet)
router.register(r'insumos', InsumoViewSet)
router.register(r'guias-desempeno', GuiaDesempenoRazaViewSet)
router.register(r'wiki/categorias', CategoryViewSet)
router.register(r'wiki/articulos', ArticleViewSet)
router.register(r'faq/categorias', FAQCategoryViewSet)
router.register(r'faq/preguntas', FAQViewSet)
router.register(r'bot/conversaciones', BotConversationViewSet, basename='bot-conversation')
router.register(r'estadisticas', EstadisticasViewSet, basename='estadisticas')

urlpatterns = [
    # Rutas generadas automáticamente por el router
    path('', include(router.urls)),
    
    # Rutas para autenticación JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Rutas para comparación de razas
    path('comparacion-razas/', ComparacionRazasView.as_view(), name='comparacion-razas-lista'),
    path('comparacion-razas/<str:raza_id>/<str:lote_id>/', ComparacionRazasView.as_view(), name='comparacion-razas-detalle'),
]