from django.conf import settings
from django.urls import reverse, NoReverseMatch
from django.apps import apps

def navigation_items(request):
    """Generate navigation items based on user role and permissions."""
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return {}
    
    is_superuser = request.user.is_superuser
    is_staff = request.user.is_staff
    current_path = request.path
    
    def get_url(url_name):
        try:
            return reverse(url_name)
        except NoReverseMatch:
            return f'/{url_name}'
    
    # Check if apps are installed
    wiki_installed = apps.is_installed('wiki')
    faq_installed = apps.is_installed('faq')
    bot_installed = apps.is_installed('bot')
    
    nav_items = [
        {
            'title': 'Dashboard',
            'url': reverse('core:dashboard'),
            'icon': 'fa-tachometer-alt',
            'permission': True,
            'active': current_path.startswith(reverse('core:dashboard') if is_superuser else reverse('core:dashboard_operario'))
        },
        {
            'title': 'Reportes',
            'url': get_url('reportes:panel_reportes'),
            'icon': 'fa-chart-bar',
            'permission': True,
            'active': current_path.startswith(reverse('reportes:panel_reportes'))
        },
        {
            'title': 'Inventario',
            'icon': 'fa-boxes',
            'url': get_url('inventario:lista_alimentos'),
            'permission': True,
            'active': current_path.startswith('/inventario/')
        },
        {
            'title': 'Producción',
            'icon': 'fa-warehouse',
            'url': get_url('avicola:listar_lotes'),
            'permission': True,
            'active': current_path.startswith('/produccion/') or current_path.startswith('/lotes/')
        },
        {
            'title': 'Estadísticas',
            'icon': 'fa-chart-line',
            'url': get_url('avicola:estadisticas'),
            'permission': True,
            'active': current_path.startswith(reverse('avicola:estadisticas'))
        },
        {
            'title': 'Gráficos',
            'icon': 'fa-chart-pie',
            'url': get_url('avicola:graficos'),
            'permission': True,
            'active': current_path.startswith(reverse('avicola:graficos'))
        },
        {
            'title': 'Wiki',
            'icon': 'fa-book',
            'url': get_url('wiki:wiki_home'),
            'permission': wiki_installed,
            'new_tab': False,
            'active': current_path.startswith('/wiki/')
        },
        {
            'title': 'FAQ',
            'icon': 'fa-question-circle',
            'url': get_url('faq:faq_list'),
            'permission': faq_installed,
            'new_tab': False,
            'active': current_path.startswith('/faq/')
        },
        {
            'title': 'Chat Bot',
            'icon': 'fa-robot',
            'url': get_url('bot:chat'),
            'permission': bot_installed,
            'new_tab': False,
            'active': current_path.startswith('/bot/')
        },
        {
            'title': 'Administración',
            'icon': 'fa-cogs',
            'url': get_url('admin:index'),
            'permission': is_superuser,
            'new_tab': True,
            'active': current_path.startswith('/admin/')
        }
    ]
    
    # Process navigation items
    processed_items = []
    for item in nav_items:
        # Skip items without permission
        if 'permission' in item and not item['permission']:
            continue
            
        # Create a copy to avoid modifying the original
        nav_item = item.copy()
        
        # Process URL
        if 'url' in nav_item:
            nav_item['url'] = get_url(nav_item['url'])
            nav_item['active'] = current_path.startswith(nav_item['url'])
        
        # Process children
        if 'children' in nav_item:
            nav_item['children'] = []
            for child in item.get('children', []):
                if 'permission' in child and not child['permission']:
                    continue
                    
                child_copy = child.copy()
                child_url = get_url(child['url'])
                child_copy['url'] = child_url
                child_copy['active'] = current_path.startswith(child_url)
                
                # If any child is active, mark parent as active
                if child_copy['active']:
                    nav_item['active'] = True
                    
                nav_item['children'].append(child_copy)
        
        processed_items.append(nav_item)
    
    return {
        'nav_items': processed_items
    }
