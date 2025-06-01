"""
Views para la sección de Gráficos del sistema
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Count, F, Q
from django.utils import timezone
from datetime import timedelta
import json

from produccion.models import Lote, SeguimientoDiario, MortalidadDiaria
from inventario.models import ConsumoAlimento, AplicacionVacuna

@login_required
def graficos(request):
    """
    Vista para mostrar los gráficos de estadísticas
    """
    # Obtener datos para los gráficos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Datos de producción de huevos (últimos 30 días)
    fecha_limite = hoy - timedelta(days=30)
    produccion_huevos = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite,
        huevos_totales__gt=0
    ).values('fecha_seguimiento').annotate(
        total_huevos=Sum('huevos_totales'),
        huevos_rotos=Sum('huevos_rotos'),
        huevos_sucios=Sum('huevos_sucios')
    ).order_by('fecha_seguimiento')
    
    # Datos de mortalidad (últimos 30 días)
    mortalidad = MortalidadDiaria.objects.filter(
        fecha__gte=fecha_limite
    ).values('fecha').annotate(
        total_muertes=Sum('cantidad_muertes')
    ).order_by('fecha')
    
    # Datos de consumo de alimento (últimos 30 días)
    consumo_alimento = ConsumoAlimento.objects.filter(
        fecha_consumo__gte=fecha_limite
    ).values('fecha_consumo').annotate(
        total_kg=Sum('cantidad_kg')
    ).order_by('fecha_consumo')
    
    # Preparar datos para los gráficos
    datos_graficos = {
        'produccion_huevos': [],
        'mortalidad': [],
        'consumo_alimento': []
    }
    
    for p in produccion_huevos:
        datos_graficos['produccion_huevos'].append({
            'fecha': p['fecha_seguimiento'].strftime('%Y-%m-%d'),
            'total': float(p['total_huevos'] or 0),
            'rotos': float(p['huevos_rotos'] or 0),
            'sucios': float(p['huevos_sucios'] or 0)
        })
    
    for m in mortalidad:
        datos_graficos['mortalidad'].append({
            'fecha': m['fecha'].strftime('%Y-%m-%d'),
            'muertes': float(m['total_muertes'] or 0)
        })
    
    for c in consumo_alimento:
        datos_graficos['consumo_alimento'].append({
            'fecha': c['fecha_consumo'].strftime('%Y-%m-%d'),
            'kg': float(c['total_kg'] or 0)
        })
    
    # Convertir a JSON para usar en JavaScript
    datos_graficos_json = json.dumps(datos_graficos)
    
    context = {
        'datos_graficos': datos_graficos_json,
        'title': 'Gráficos y Estadísticas',
        'section': 'graficos',
    }
    
    return render(request, 'avicola/graficos.html', context)
