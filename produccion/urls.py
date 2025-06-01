from django.urls import path
from . import views
from . import views_mortalidad

app_name = 'produccion'  # This should match the app's label in INSTALLED_APPS

urlpatterns = [
    # Rutas para lotes
    path('lotes/', views.lista_lotes, name='lista_lotes'),
    path('lotes/<int:lote_id>/', views.detalle_lote, name='detalle_lote'),
    path('lotes/nuevo/<int:galpon_id>/', views.nuevo_lote, name='nuevo_lote'),
    path('lotes/<int:lote_id>/editar/', views.editar_lote, name='editar_lote'),
    
    # Rutas para galpones
    path('galpones/', views.lista_galpones, name='lista_galpones'),
    path('galpones/nuevo/', views.nuevo_galpon, name='nuevo_galpon'),
    path('galpones/<int:galpon_id>/', views.detalle_galpon, name='detalle_galpon'),
    path('galpones/<int:galpon_id>/editar/', views.editar_galpon, name='editar_galpon'),
    path('galpones/mantenimiento/<int:galpon_id>/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    
    # Rutas para tareas
    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/<int:tarea_id>/', views.detalle_tarea, name='detalle_tarea'),
    path('tareas/<int:tarea_id>/completar/', views.completar_tarea, name='completar_tarea'),
    
    # Rutas para mortalidad diaria
    path('mortalidad/', views_mortalidad.lista_mortalidad, name='lista_mortalidad'),
    path('mortalidad/nueva/', views_mortalidad.nueva_mortalidad, name='nueva_mortalidad'),
    path('mortalidad/<int:mortalidad_id>/', views_mortalidad.detalle_mortalidad, name='detalle_mortalidad'),
    path('mortalidad/<int:mortalidad_id>/editar/', views_mortalidad.editar_mortalidad, name='editar_mortalidad'),
    path('mortalidad/<int:mortalidad_id>/eliminar/', views_mortalidad.eliminar_mortalidad, name='eliminar_mortalidad'),
    
    # Rutas para seguimientos
    path('seguimientos/', views.lista_seguimientos, name='lista_seguimientos'),
    path('seguimientos/nuevo/<int:lote_id>/', views.nuevo_seguimiento, name='nuevo_seguimiento'),
    
    # Test URLs for admin
    path('test-admin-registration/', views.test_admin_registration, name='test_admin_registration'),
    path('test-admin-urls/', views.test_admin_urls, name='test_admin_urls'),
]
