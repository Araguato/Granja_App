from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Q, Sum, F, Avg
from django.utils import timezone
from datetime import timedelta
from produccion.models import Galpon, Lote, SeguimientoDiario, ConsumoEnergia
from ventas.models import Venta, InventarioHuevos

@login_required
@permission_required('produccion.view_estadisticas', raise_exception=True)
def dashboard_supervisor(request):
    """Dashboard específico para supervisores"""
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener galpones con información de lotes activos
    galpones = Galpon.objects.annotate(
        lotes_activos=Count('lote', filter=Q(lote__estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']), distinct=True)
    ).select_related('granja')
    
    # Obtener todos los lotes (activos e inactivos)
    lotes = Lote.objects.all().select_related('galpon', 'raza')
    lotes_activos = lotes.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
    
    # Obtener seguimientos recientes (últimos 5 días)
    fecha_limite = hoy - timedelta(days=5)
    ultimos_seguimientos = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite
    ).select_related('lote', 'lote__galpon').order_by('-fecha_seguimiento')[:10]
    
    # Calcular estadísticas de producción
    produccion_hoy = SeguimientoDiario.objects.filter(
        fecha_seguimiento=hoy
    ).aggregate(
        total_huevos=Sum('huevos_totales'),
        total_mortalidad=Sum('mortalidad')
    )
    
    # Obtener estadísticas de energía
    consumo_hoy = ConsumoEnergia.objects.filter(
        fecha_registro=hoy
    ).aggregate(
        total_consumo=Sum('consumo_kwh')
    )
    
    consumo_mes = ConsumoEnergia.objects.filter(
        fecha_registro__month=hoy.month,
        fecha_registro__year=hoy.year
    ).aggregate(
        total_consumo=Sum('consumo_kwh')
    )
    
    estadisticas_energia = {
        'consumo_diario': consumo_hoy['total_consumo'] or 0,
        'consumo_mensual': consumo_mes['total_consumo'] or 0,
        'costo_estimado': (consumo_mes['total_consumo'] or 0) * 0.15  # Ajustar según tarifa
    }
    
    # Obtener estadísticas de ventas
    ventas_mes = Venta.objects.filter(
        fecha_venta__month=hoy.month,
        fecha_venta__year=hoy.year
    ).aggregate(
        total_ventas=Sum('total')
    )
    
    # Obtener inventario actual de huevos
    inventario_huevos = InventarioHuevos.objects.aggregate(
        total_huevos=Sum('cantidad')
    )
    
    context = {
        'title': 'Dashboard Supervisor',
        'user': request.user,
        'galpones': galpones,
        'lotes': lotes,
        'lotes_activos': lotes_activos,
        'galpones_activos': galpones.count(),
        'total_huevos_hoy': produccion_hoy['total_huevos'] or 0,
        'mortalidad_hoy': produccion_hoy['total_mortalidad'] or 0,
        'estadisticas_energia': estadisticas_energia,
        'ultimos_seguimientos': ultimos_seguimientos,
        'total_ventas_mes': ventas_mes['total_ventas'] or 0,
        'total_huevos_inventario': inventario_huevos['total_huevos'] or 0,
        'es_admin': request.user.is_superuser or request.user.groups.filter(name='Administradores').exists(),
        'hoy': hoy,
    }
    
    return render(request, 'dashboard_supervisor.html', context)
