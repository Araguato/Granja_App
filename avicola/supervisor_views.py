from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q, Sum, F, Avg
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from produccion.models import Galpon, Lote, SeguimientoDiario, Tarea
from django.contrib import messages

@login_required
@permission_required('avicola.es_supervisor', raise_exception=True)
def listar_galpones(request):
    """Lista todos los galpones con información relevante"""
    galpones = Galpon.objects.annotate(
        lotes_activos=Count('lotes', filter=Q(lotes__estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']), distinct=True)
    ).select_related('granja').order_by('numero')
    
    # Paginación
    paginator = Paginator(galpones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Listado de Galpones',
        'page_obj': page_obj,
        'total_galpones': galpones.count(),
    }
    return render(request, 'supervisor/galpones_list.html', context)

@login_required
@permission_required('avicola.es_supervisor', raise_exception=True)
def detalle_galpon(request, galpon_id):
    """Muestra el detalle de un galpón específico"""
    galpon = get_object_or_404(Galpon.objects.select_related('granja'), id=galpon_id)
    lotes_activos = galpon.lotes.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
    
    # Obtener estadísticas del galpón
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener seguimientos recientes (últimos 5 días)
    fecha_limite = hoy - timedelta(days=5)
    ultimos_seguimientos = SeguimientoDiario.objects.filter(
        lote__galpon=galpon,
        fecha_seguimiento__gte=fecha_limite
    ).select_related('lote').order_by('-fecha_seguimiento')[:10]
    
    context = {
        'title': f'Galpón {galpon.numero} - {galpon.nombre}',
        'galpon': galpon,
        'lotes_activos': lotes_activos,
        'ultimos_seguimientos': ultimos_seguimientos,
    }
    return render(request, 'supervisor/galpon_detalle.html', context)

@login_required
@permission_required('avicola.es_supervisor', raise_exception=True)
def listar_lotes(request):
    """Lista todos los lotes activos"""
    lotes = Lote.objects.filter(
        estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
    ).select_related('galpon', 'galpon__granja', 'raza').order_by('galpon__numero', 'fecha_ingreso')
    
    # Obtener estadísticas
    total_lotes = lotes.count()
    total_aves = sum(lote.cantidad_inicial_aves for lote in lotes if lote.cantidad_inicial_aves)
    
    # Paginación
    paginator = Paginator(lotes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Lotes Activos',
        'page_obj': page_obj,
        'total_lotes': total_lotes,
        'total_aves': total_aves,
    }
    return render(request, 'supervisor/lotes_list.html', context)

@login_required
@permission_required('avicola.es_supervisor', raise_exception=True)
def detalle_lote(request, lote_id):
    """Muestra el detalle de un lote específico"""
    lote = get_object_or_404(
        Lote.objects.select_related('galpon', 'galpon__granja', 'raza', 'alimento'),
        id=lote_id
    )
    
    # Obtener seguimientos del lote
    seguimientos = SeguimientoDiario.objects.filter(
        lote=lote
    ).order_by('-fecha_seguimiento')
    
    # Calcular estadísticas
    total_huevos = seguimientos.aggregate(Sum('huevos_totales'))['huevos_totales__sum'] or 0
    total_mortalidad = seguimientos.aggregate(Sum('mortalidad'))['mortalidad__sum'] or 0
    
    context = {
        'title': f'Lote {lote.codigo}',
        'lote': lote,
        'seguimientos': seguimientos[:10],  # Últimos 10 seguimientos
        'total_seguimientos': seguimientos.count(),
        'total_huevos': total_huevos,
        'total_mortalidad': total_mortalidad,
    }
    return render(request, 'supervisor/lote_detalle.html', context)
