from django.urls import path
from . import views
import sys

print("Loading inventario URLs...", file=sys.stderr)
app_name = 'inventario'

# URL patterns
urlpatterns = [
    # Debug URL - Remove in production
    path('debug/urls/', views.debug_urls, name='debug_urls'),
    
    # Rutas para alimentos
    path('alimentos/', views.lista_alimentos, name='lista_alimentos'),
    path('alimentos/<int:alimento_id>/', views.detalle_alimento, name='detalle_alimento'),
    path('alimentos/consumo/', views.registrar_consumo, name='registrar_consumo'),
    
    # Rutas para vacunas
    path('vacunas/', views.lista_vacunas, name='lista_vacunas'),
    path('vacunas/<int:vacuna_id>/', views.detalle_vacuna, name='detalle_vacuna'),
    path('vacunas/aplicacion/', views.registrar_aplicacion, name='registrar_aplicacion'),
    
    # Rutas para seguimiento
    path('seguimiento/', views.registro_seguimiento, name='registro_seguimiento'),
    path('seguimiento/nuevo/<int:lote_id>/', views.nuevo_seguimiento, name='nuevo_seguimiento'),
    path('seguimiento/historial/<int:lote_id>/', views.seguimiento_lote, name='seguimiento_lote'),
    
    # Rutas para medicamentos
    path('medicamentos/', views.lista_medicamentos, name='lista_medicamentos'),
    path('medicamentos/nuevo/', views.nuevo_medicamento, name='nuevo_medicamento'),
    path('medicamentos/<int:medicamento_id>/', views.detalle_medicamento, name='detalle_medicamento'),
    path('medicamentos/<int:medicamento_id>/editar/', views.editar_medicamento, name='editar_medicamento'),
    path('medicamentos/<int:medicamento_id>/eliminar/', views.eliminar_medicamento, name='eliminar_medicamento'),
    path('medicamentos/aplicacion/', views.registrar_aplicacion_medicamento, name='registrar_aplicacion_medicamento'),
]
