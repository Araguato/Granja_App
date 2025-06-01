from django.urls import path
from . import views

app_name = 'wiki'

urlpatterns = [
    path('', views.wiki_home, name='wiki_home'),
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),
    path('categoria/<slug:category_slug>/articulo/<slug:article_slug>/', views.article_detail, name='article_detail'),
]
