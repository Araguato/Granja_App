from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import timedelta

from produccion.models import SeguimientoDiario, Lote, MortalidadDiaria
from ventas.models import Venta, DetalleVenta
from inventario.models import Alimento, Vacuna

def obtener_estadisticas_produccion(periodo='semana'):
    """
    Obtiene estadísticas de producción (huevos) para el período especificado.
    Períodos: 'dia', 'semana', 'mes'
    """
    fecha_actual = timezone.now().date()
    
    if periodo == 'dia':
        # Últimos 7 días
        fecha_inicio = fecha_actual - timedelta(days=6)
        truncate_func = TruncDay
        fecha_format = '%d/%m'
    elif periodo == 'semana':
        # Últimas 8 semanas
        fecha_inicio = fecha_actual - timedelta(weeks=7)
        truncate_func = TruncWeek
        fecha_format = 'Sem %W'
    else:  # mes
        # Últimos 6 meses
        fecha_inicio = (fecha_actual - timedelta(days=180)).replace(day=1)
        truncate_func = TruncMonth
        fecha_format = '%b %Y'
    
    # Obtener datos de producción de huevos
    datos_produccion = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_inicio,
        fecha_seguimiento__lte=fecha_actual
    ).annotate(
        periodo=truncate_func('fecha_seguimiento')
    ).values('periodo').annotate(
        total_huevos=Sum('huevos_totales')
    ).order_by('periodo')
    
    # Formatear los datos para el gráfico
    labels = []
    datos = []
    
    for item in datos_produccion:
        if periodo == 'dia':
            labels.append(item['periodo'].strftime(fecha_format))
        elif periodo == 'semana':
            labels.append(item['periodo'].strftime(fecha_format))
        else:  # mes
            labels.append(item['periodo'].strftime(fecha_format))
        
        datos.append(item['total_huevos'])
    
    return {
        'labels': labels,
        'datos': datos
    }

def obtener_estadisticas_mortalidad(periodo='semana'):
    """
    Obtiene estadísticas de mortalidad para el período especificado.
    Períodos: 'dia', 'semana', 'mes'
    """
    fecha_actual = timezone.now().date()
    
    if periodo == 'dia':
        # Últimos 7 días
        fecha_inicio = fecha_actual - timedelta(days=6)
        truncate_func = TruncDay
        fecha_format = '%d/%m'
    elif periodo == 'semana':
        # Últimas 8 semanas
        fecha_inicio = fecha_actual - timedelta(weeks=7)
        truncate_func = TruncWeek
        fecha_format = 'Sem %W'
    else:  # mes
        # Últimos 6 meses
        fecha_inicio = (fecha_actual - timedelta(days=180)).replace(day=1)
        truncate_func = TruncMonth
        fecha_format = '%b %Y'
    
    # Obtener datos de mortalidad
    datos_mortalidad = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_inicio,
        fecha_seguimiento__lte=fecha_actual,
        mortalidad__gt=0
    ).annotate(
        periodo=truncate_func('fecha_seguimiento')
    ).values('periodo').annotate(
        total_mortalidad=Sum('mortalidad')
    ).order_by('periodo')
    
    # Formatear los datos para el gráfico
    labels = []
    datos = []
    
    for item in datos_mortalidad:
        if periodo == 'dia':
            labels.append(item['periodo'].strftime(fecha_format))
        elif periodo == 'semana':
            labels.append(item['periodo'].strftime(fecha_format))
        else:  # mes
            labels.append(item['periodo'].strftime(fecha_format))
        
        datos.append(item['total_mortalidad'])
    
    return {
        'labels': labels,
        'datos': datos
    }

def obtener_estadisticas_ventas(periodo='semana'):
    """
    Obtiene estadísticas de ventas para el período especificado.
    Períodos: 'dia', 'semana', 'mes'
    """
    fecha_actual = timezone.now().date()
    
    if periodo == 'dia':
        # Últimos 7 días
        fecha_inicio = fecha_actual - timedelta(days=6)
        truncate_func = TruncDay
        fecha_format = '%d/%m'
    elif periodo == 'semana':
        # Últimas 8 semanas
        fecha_inicio = fecha_actual - timedelta(weeks=7)
        truncate_func = TruncWeek
        fecha_format = 'Sem %W'
    else:  # mes
        # Últimos 6 meses
        fecha_inicio = (fecha_actual - timedelta(days=180)).replace(day=1)
        truncate_func = TruncMonth
        fecha_format = '%b %Y'
    
    # Obtener datos de ventas
    datos_ventas = Venta.objects.filter(
        fecha_venta__gte=fecha_inicio,
        fecha_venta__lte=fecha_actual
    ).annotate(
        periodo=truncate_func('fecha_venta')
    ).values('periodo').annotate(
        total_ventas=Sum('total_venta')
    ).order_by('periodo')
    
    # Formatear los datos para el gráfico
    labels = []
    datos = []
    
    for item in datos_ventas:
        if periodo == 'dia':
            labels.append(item['periodo'].strftime(fecha_format))
        elif periodo == 'semana':
            labels.append(item['periodo'].strftime(fecha_format))
        else:  # mes
            labels.append(item['periodo'].strftime(fecha_format))
        
        datos.append(float(item['total_ventas']))
    
    return {
        'labels': labels,
        'datos': datos
    }

def obtener_distribucion_tipos_huevo():
    """
    Obtiene la distribución de ventas por tipo de huevo.
    """
    # Obtener datos de ventas por tipo de huevo
    datos_tipos_huevo = DetalleVenta.objects.values(
        'tipo_huevo__clasificacion'
    ).annotate(
        total=Sum('cantidad')
    ).order_by('-total')
    
    # Formatear los datos para el gráfico
    labels = []
    datos = []
    
    for item in datos_tipos_huevo:
        # Obtener el display value del choice field
        from ventas.models import TipoHuevo
        try:
            tipo_huevo = TipoHuevo.objects.get(clasificacion=item['tipo_huevo__clasificacion'])
            label = tipo_huevo.get_clasificacion_display()
        except TipoHuevo.DoesNotExist:
            label = item['tipo_huevo__clasificacion']
            
        labels.append(label)
        datos.append(item['total'])
    
    return {
        'labels': labels,
        'datos': datos
    }

def obtener_resumen_inventario():
    """
    Obtiene un resumen del inventario actual.
    """
    # Obtener datos de alimentos
    alimentos = Alimento.objects.all()
    total_alimentos = alimentos.count()
    
    # Obtener datos de vacunas
    vacunas = Vacuna.objects.all()
    total_vacunas = vacunas.count()
    
    # Obtener datos de lotes
    lotes = Lote.objects.all()
    total_lotes = lotes.count()
    lotes_activos = lotes.filter(estado='activo').count()
    
    return {
        'total_alimentos': total_alimentos,
        'total_vacunas': total_vacunas,
        'total_lotes': total_lotes,
        'lotes_activos': lotes_activos
    }

def obtener_estadisticas_engorde(periodo='semana', lote_id=None, galpon_id=None):
    """
    Obtiene estadísticas de engorde para el período y lote/galpón especificados.
    Períodos: 'dia', 'semana', 'mes'
    """
    from produccion.models import SeguimientoEngorde
    
    fecha_actual = timezone.now().date()
    
    if periodo == 'dia':
        # Últimos 14 días
        fecha_inicio = fecha_actual - timedelta(days=13)
        truncate_func = TruncDay
        fecha_format = '%d/%m'
    elif periodo == 'semana':
        # Últimas 8 semanas
        fecha_inicio = fecha_actual - timedelta(weeks=7)
        truncate_func = TruncWeek
        fecha_format = 'Sem %W'
    else:  # mes
        # Últimos 6 meses
        fecha_inicio = (fecha_actual - timedelta(days=180)).replace(day=1)
        truncate_func = TruncMonth
        fecha_format = '%b %Y'
    
    # Filtrar por lote o galpón si se especifica
    query = SeguimientoEngorde.objects.select_related('seguimiento_diario', 'seguimiento_diario__lote', 'seguimiento_diario__lote__galpon')
    
    if lote_id:
        query = query.filter(seguimiento_diario__lote_id=lote_id)
    elif galpon_id:
        query = query.filter(seguimiento_diario__lote__galpon_id=galpon_id)
    
    # Obtener datos de engorde
    query = query.filter(
        seguimiento_diario__fecha_seguimiento__gte=fecha_inicio,
        seguimiento_diario__fecha_seguimiento__lte=fecha_actual
    )
    
    # Agrupar por periodo
    datos_engorde = query.annotate(
        periodo=truncate_func('seguimiento_diario__fecha_seguimiento')
    ).values('periodo').annotate(
        peso_promedio=Avg('seguimiento_diario__peso_promedio_ave'),
        ganancia_diaria_promedio=Avg('ganancia_diaria_peso'),
        conversion_alimenticia_promedio=Avg('conversion_alimenticia'),
        eficiencia_energetica_promedio=Avg('eficiencia_energetica'),
        eficiencia_proteica_promedio=Avg('eficiencia_proteica'),
        relacion_energia_proteina_promedio=Avg('relacion_energia_proteina')
    ).order_by('periodo')
    
    # Formatear los datos para los gráficos
    labels = []
    datos_peso = []
    datos_ganancia = []
    datos_conversion = []
    datos_eficiencia_energetica = []
    datos_eficiencia_proteica = []
    datos_relacion_energia_proteina = []
    
    for item in datos_engorde:
        if periodo == 'dia':
            labels.append(item['periodo'].strftime(fecha_format))
        elif periodo == 'semana':
            labels.append(item['periodo'].strftime(fecha_format))
        else:  # mes
            labels.append(item['periodo'].strftime(fecha_format))
        
        datos_peso.append(float(item['peso_promedio']) if item['peso_promedio'] else 0)
        datos_ganancia.append(float(item['ganancia_diaria_promedio']) if item['ganancia_diaria_promedio'] else 0)
        datos_conversion.append(float(item['conversion_alimenticia_promedio']) if item['conversion_alimenticia_promedio'] else 0)
        datos_eficiencia_energetica.append(float(item['eficiencia_energetica_promedio']) if item['eficiencia_energetica_promedio'] else 0)
        datos_eficiencia_proteica.append(float(item['eficiencia_proteica_promedio']) if item['eficiencia_proteica_promedio'] else 0)
        datos_relacion_energia_proteina.append(float(item['relacion_energia_proteina_promedio']) if item['relacion_energia_proteina_promedio'] else 0)
    
    return {
        'labels': labels,
        'datos_peso': datos_peso,
        'datos_ganancia': datos_ganancia,
        'datos_conversion': datos_conversion,
        'datos_eficiencia_energetica': datos_eficiencia_energetica,
        'datos_eficiencia_proteica': datos_eficiencia_proteica,
        'datos_relacion_energia_proteina': datos_relacion_energia_proteina
    }

def obtener_estadisticas_por_galpon(periodo='semana'):
    """
    Obtiene estadísticas comparativas por galpón.
    """
    from produccion.models import Galpon
    
    # Obtener todos los galpones activos
    galpones = Galpon.objects.filter(lotes__estado='PRODUCCION').distinct()
    
    resultado = {
        'labels': [],
        'datos_peso': [],
        'datos_ganancia': [],
        'datos_conversion': [],
        'datos_mortalidad': [],
        'datos_eficiencia_energetica': [],
        'datos_eficiencia_proteica': [],
        'datos_relacion_energia_proteina': []
    }
    
    for galpon in galpones:
        # Añadir etiqueta del galpón
        resultado['labels'].append(f"Galpón {galpon.numero_galpon}")
        
        # Obtener estadísticas de engorde para este galpón
        stats_engorde = obtener_estadisticas_engorde(periodo, galpon_id=galpon.id)
        
        # Calcular promedios para este galpón
        if stats_engorde['datos_peso']:
            resultado['datos_peso'].append(sum(stats_engorde['datos_peso']) / len(stats_engorde['datos_peso']))
        else:
            resultado['datos_peso'].append(0)
            
        if stats_engorde['datos_ganancia']:
            resultado['datos_ganancia'].append(sum(stats_engorde['datos_ganancia']) / len(stats_engorde['datos_ganancia']))
        else:
            resultado['datos_ganancia'].append(0)
            
        if stats_engorde['datos_conversion']:
            resultado['datos_conversion'].append(sum(stats_engorde['datos_conversion']) / len(stats_engorde['datos_conversion']))
        else:
            resultado['datos_conversion'].append(0)
        
        # Eficiencia energética y nutricional
        if 'datos_eficiencia_energetica' in stats_engorde and stats_engorde['datos_eficiencia_energetica']:
            resultado['datos_eficiencia_energetica'].append(sum(stats_engorde['datos_eficiencia_energetica']) / len(stats_engorde['datos_eficiencia_energetica']))
        else:
            resultado['datos_eficiencia_energetica'].append(0)
            
        if 'datos_eficiencia_proteica' in stats_engorde and stats_engorde['datos_eficiencia_proteica']:
            resultado['datos_eficiencia_proteica'].append(sum(stats_engorde['datos_eficiencia_proteica']) / len(stats_engorde['datos_eficiencia_proteica']))
        else:
            resultado['datos_eficiencia_proteica'].append(0)
            
        if 'datos_relacion_energia_proteina' in stats_engorde and stats_engorde['datos_relacion_energia_proteina']:
            resultado['datos_relacion_energia_proteina'].append(sum(stats_engorde['datos_relacion_energia_proteina']) / len(stats_engorde['datos_relacion_energia_proteina']))
        else:
            resultado['datos_relacion_energia_proteina'].append(0)
        
        # Obtener mortalidad para este galpón
        mortalidad = SeguimientoDiario.objects.filter(
            lote__galpon=galpon,
            fecha_seguimiento__gte=timezone.now().date() - timedelta(days=30),
            mortalidad__gt=0
        ).aggregate(total=Sum('mortalidad'))['total'] or 0
        
        resultado['datos_mortalidad'].append(mortalidad)
    
    return resultado

def obtener_estadisticas_dashboard():
    """
    Obtiene todas las estadísticas necesarias para el dashboard.
    """
    # Producción de huevos (últimas 4 semanas)
    produccion = obtener_estadisticas_produccion('semana')
    
    # Mortalidad (últimas 4 semanas)
    mortalidad = obtener_estadisticas_mortalidad('semana')
    
    # Ventas (últimos 6 meses)
    ventas = obtener_estadisticas_ventas('mes')
    
    # Distribución de tipos de huevo
    tipos_huevo = obtener_distribucion_tipos_huevo()
    
    # Resumen de inventario
    inventario = obtener_resumen_inventario()
    
    # Estadísticas de engorde
    engorde = obtener_estadisticas_engorde('semana')
    
    # Estadísticas por galpón
    por_galpon = obtener_estadisticas_por_galpon('semana')
    
    return {
        'produccion': produccion,
        'mortalidad': mortalidad,
        'ventas': ventas,
        'tipos_huevo': tipos_huevo,
        'inventario': inventario,
        'engorde': engorde,
        'por_galpon': por_galpon
    }
