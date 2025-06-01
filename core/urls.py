from django.urls import path
from . import views
from .test_views import test_view

app_name = 'core'  # This is the app's namespace

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/', test_view, name='test_view'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]
