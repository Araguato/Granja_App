"""
Vistas para los dashboards del sistema
"""
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta

from produccion.models import Galpon, Lote, SeguimientoDiario, MortalidadDiaria, Granja
from inventario.models import Alimento, Vacuna, ConsumoAlimento, AplicacionVacuna
from ventas.models import Venta, DetalleVenta, TipoHuevo

logger = logging.getLogger(__name__)

@login_required
def dashboard_supervisor(request):
    """
    Vista del dashboard para supervisores
    """
    # Verificar si el usuario tiene permisos de supervisor o es superusuario
    if not request.user.is_authenticated:
        return redirect('avicola:login')
        
    if not (request.user.is_superuser or (hasattr(request.user, 'groups') and 
            request.user.groups.filter(name__in=['Supervisores', 'Administradores']).exists())):
        messages.warning(request, 'No tiene permisos para acceder al panel de supervisión.')
        return render(request, 'core/home.html', {'title': 'Inicio'})
    
    # Importar las funciones de estadísticas
    from core.estadisticas import obtener_estadisticas_dashboard
    
    # Obtener las estadísticas para el dashboard
    try:
        estadisticas = obtener_estadisticas_dashboard()
        return render(request, 'core/dashboard_updated.html', {
            'title': 'Panel de Supervisión',
            'estadisticas': estadisticas,
            'user': request.user
        })
    except Exception as e:
        logger.error(f'Error en dashboard_supervisor: {str(e)}', exc_info=True)
        messages.error(request, 'Error al cargar el panel de supervisión. Por favor, intente nuevamente.')
        return render(request, 'core/home.html', {'title': 'Inicio'})

@login_required
def dashboard_operario(request):
    """
    Vista del dashboard para operarios
    """
    # Verificar si el usuario está autenticado
    if not request.user.is_authenticated:
        return redirect('avicola:login')
        
    # Verificar si el usuario es operario
    if not (hasattr(request.user, 'groups') and 
            request.user.groups.filter(name='Operarios').exists()):
        messages.warning(request, 'No tiene permisos para acceder al panel de operario.')
        return render(request, 'core/home.html', {'title': 'Inicio'})
    
    # Lógica específica para el dashboard de operarios
    try:
        # Aquí iría la lógica específica para el dashboard de operarios
        return render(request, 'core/dashboard_operario.html', {
            'title': 'Panel de Operario',
            'user': request.user
        })
    except Exception as e:
        logger.error(f'Error en dashboard_operario: {str(e)}', exc_info=True)
        messages.error(request, 'Error al cargar el panel de operario. Por favor, intente nuevamente.')
        return render(request, 'core/home.html', {'title': 'Inicio'})

@login_required
def estadisticas(request):
    """
    Vista para mostrar estadísticas generales de la granja
    """
    if not request.user.is_authenticated:
        return redirect('avicola:login')
    
    # Obtener datos para las estadísticas
    context = {
        'title': 'Estadísticas',
        'total_gallinas': Lote.objects.aggregate(total=Sum('cantidad_aves'))['total'] or 0,
        'total_galpones': Galpon.objects.count(),
        'lotes_activos': Lote.objects.filter(activo=True).count(),
        'produccion_hoy': SeguimientoDiario.objects.filter(
            fecha=timezone.now().date()
        ).aggregate(total=Sum('huevos_producidos'))['total'] or 0,
        'ventas_mes': Venta.objects.filter(
            fecha__month=timezone.now().month,
            fecha__year=timezone.now().year
        ).aggregate(total=Sum('total'))['total'] or 0,
        'mortalidad_mes': MortalidadDiaria.objects.filter(
            fecha__month=timezone.now().month,
            fecha__year=timezone.now().year
        ).aggregate(total=Sum('cantidad'))['total'] or 0,
    }
    
    # Datos para gráficos (últimos 7 días)
    fecha_inicio = timezone.now().date() - timedelta(days=7)
    produccion_7dias = SeguimientoDiario.objects.filter(
        fecha__gte=fecha_inicio
    ).values('fecha').annotate(
        total=Sum('huevos_producidos')
    ).order_by('fecha')
    
    context['produccion_labels'] = [d['fecha'].strftime('%d/%m') for d in produccion_7dias]
    context['produccion_data'] = [d['total'] or 0 for d in produccion_7dias]
    
    # Distribución por tipo de huevo
    distribucion_huevos = TipoHuevo.objects.annotate(
        total_vendido=Sum('detalleventa__cantidad')
    ).filter(total_vendido__gt=0).values('nombre', 'total_vendido')
    
    context['huevos_labels'] = [d['nombre'] for d in distribucion_huevos]
    context['huevos_data'] = [d['total_vendido'] or 0 for d in distribucion_huevos]
    
    return render(request, 'avicola/estadisticas.html', context)
