from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.panel_reportes, name='panel_reportes'),
    path('nuevo/', views.nuevo_reporte, name='nuevo_reporte'),
    path('<int:reporte_id>/', views.detalle_reporte, name='detalle_reporte'),
    path('<int:reporte_id>/descargar/', views.descargar_reporte, name='descargar_reporte'),
    path('<int:reporte_id>/eliminar/', views.eliminar_reporte, name='eliminar_reporte'),
]
