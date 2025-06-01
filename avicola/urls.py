from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.shortcuts import redirect
from . import views  # Importamos las vistas de avicola
from . import views_permisos  # Importamos las vistas de permisos
from . import views_grupos  # Importamos las vistas de grupos
from . import views_admin  # Importamos las vistas de administración
from . import views_dashboard  # Importamos las vistas de dashboard
from . import views_graficos  # Importamos las vistas de gráficos
from .test_admin_style import AdminStyleTestView  # Para probar estilos de admin

# Definimos el namespace para la aplicación
app_name = 'avicola'

urlpatterns = [
    # Authentication URLs have been moved to the main urls.py
    # They are now available at the root level (e.g., /login/, /logout/, etc.)
    path('dashboard/', views_dashboard.dashboard_supervisor, name='avicola_dashboard'),
    path('reportes/', views.reportes, name='avicola_reportes'),
    path('estadisticas/', views_dashboard.estadisticas, name='estadisticas'),
    path('graficos/', views_graficos.graficos, name='graficos'),
    
    # Dashboard redirections (kept for backward compatibility)
    path('dashboard/operario/', views_dashboard.dashboard_operario, name='dashboard_operario_legacy'),
    path('dashboard/supervisor/', views_dashboard.dashboard_supervisor, name='dashboard_supervisor_legacy'),
    
    # Language selection
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
    path('set-language-ajax/', views.set_language_ajax, name='set_language_ajax'),
    
    # Admin style test
    path('admin/style-test/', AdminStyleTestView.as_view(), name='admin_style_test'),
    
    # Lot and coop management
    path('lotes/', views.listar_lotes, name='listar_lotes'),
    path('lote/<int:lote_id>/', views.detalle_lote, name='detalle_lote'),
    path('galpones/', views.listar_galpones, name='listar_galpones'),
    path('seguimientos/recientes/', views.seguimientos_recientes, name='seguimientos_recientes'),
    
    # Permissions and groups
    path('permisos/actualizar-supervisores/', 
         views_permisos.actualizar_permisos_supervisores, 
         name='actualizar_permisos_supervisores'),
    path('grupos/verificar-permisos/<str:grupo_nombre>/', views_grupos.verificar_permisos_grupo, name='verificar_permisos_grupo'),
    path('grupos/verificar-permisos/', views_grupos.verificar_permisos_grupo, name='verificar_permisos_grupo_default'),
    
    # Gestión de usuarios en grupos
    path('grupos/usuarios/<str:grupo_nombre>/', views_grupos.usuarios_grupo, name='usuarios_grupo'),
    path('grupos/usuarios/', views_grupos.usuarios_grupo, name='usuarios_grupo_default'),
    path('grupos/agregar-usuario/<str:grupo_nombre>/', views_grupos.agregar_usuario_grupo, name='agregar_usuario_grupo'),
    path('grupos/quitar-usuario/<str:grupo_nombre>/<int:usuario_id>/', views_grupos.quitar_usuario_grupo, name='quitar_usuario_grupo'),
    
    # Configuración de acceso al panel de administración
    path('admin/configurar-acceso/', views_admin.configurar_acceso_admin, name='configurar_acceso_admin'),
    
    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),
    
    # Configuración
    path('configuracion/', views.configuracion, name='configuracion'),
    
    # Estadísticas y Recomendaciones
    path('estadisticas/', views.estadisticas_view, name='estadisticas'),
    path('recomendaciones/', views.recomendaciones_view, name='recomendaciones'),
    
    # Redirección para mantener compatibilidad con URLs antiguas
    path('dashboard/', lambda request: redirect('avicola:dashboard')),
    path('dashboard/operario/', lambda request: redirect('avicola:dashboard_operario')),
    path('dashboard/supervisor/', lambda request: redirect('avicola:dashboard_supervisor')),
    path('lotes/', lambda request: redirect('avicola:listar_lotes')),
    path('galpones/', lambda request: redirect('avicola:listar_galpones')),
    path('seguimientos/recientes/', lambda request: redirect('avicola:seguimientos_recientes')),
    path('reportes/', lambda request: redirect('avicola:avicola_reportes')),
]