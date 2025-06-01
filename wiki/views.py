from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Article


@login_required
def wiki_home(request):
    """Vista para la página principal de la wiki"""
    categories = Category.objects.all().order_by('order', 'name')
    recent_articles = Article.objects.filter(is_published=True).order_by('-updated_at')[:5]
    
    return render(request, 'wiki/wiki_home.html', {
        'title': 'Wiki - Documentación',
        'categories': categories,
        'recent_articles': recent_articles
    })


@login_required
def category_detail(request, slug):
    """Vista para mostrar los artículos de una categoría específica"""
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.filter(is_published=True).order_by('title')
    
    return render(request, 'wiki/category_detail.html', {
        'title': f'Wiki - {category.name}',
        'category': category,
        'articles': articles
    })


@login_required
def article_detail(request, category_slug, article_slug):
    """Vista para mostrar un artículo específico"""
    category = get_object_or_404(Category, slug=category_slug)
    article = get_object_or_404(Article, slug=article_slug, category=category, is_published=True)
    
    # Obtener artículos relacionados
    related_articles = Article.objects.filter(
        category=category, 
        is_published=True
    ).exclude(id=article.id).order_by('title')[:5]
    
    return render(request, 'wiki/article_detail.html', {
        'title': article.title,
        'category': category,
        'article': article,
        'related_articles': related_articles
    })
