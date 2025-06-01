from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FAQCategory, FAQ


@login_required
def faq_list(request):
    """Vista para mostrar todas las categorías y preguntas frecuentes"""
    categories = FAQCategory.objects.all()
    
    # Si no hay categorías, mostrar mensaje de que no hay FAQs disponibles
    if not categories.exists():
        return render(request, 'faq/faq_list.html', {
            'title': 'Preguntas Frecuentes',
            'categories': [],
            'no_faqs': True
        })
    
    # Obtener todas las preguntas publicadas para cada categoría
    for category in categories:
        category.faqs_list = category.faqs.filter(is_published=True)
    
    return render(request, 'faq/faq_list.html', {
        'title': 'Preguntas Frecuentes',
        'categories': categories,
        'no_faqs': False
    })


@login_required
def faq_category(request, slug):
    """Vista para mostrar las preguntas de una categoría específica"""
    category = get_object_or_404(FAQCategory, slug=slug)
    faqs = category.faqs.filter(is_published=True)
    
    return render(request, 'faq/faq_category.html', {
        'title': f'Preguntas Frecuentes - {category.name}',
        'category': category,
        'faqs': faqs
    })
