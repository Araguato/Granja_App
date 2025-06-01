from django.urls import path
from . import views

app_name = 'respaldos'

urlpatterns = [
    path('', views.backup_dashboard, name='backup_dashboard'),
    path('lista/', views.backup_list, name='backup_list'),
    path('crear/', views.create_backup, name='create_backup'),
    path('configuracion/', views.backup_config, name='backup_config'),
    path('<int:backup_id>/', views.backup_detail, name='backup_detail'),
    path('<int:backup_id>/restaurar/', views.restore_backup, name='restore_backup'),
    path('<int:backup_id>/descargar/', views.download_backup, name='download_backup'),
    path('<int:backup_id>/eliminar/', views.delete_backup, name='delete_backup'),
    path('<int:backup_id>/estado/', views.backup_status, name='backup_status'),
]
