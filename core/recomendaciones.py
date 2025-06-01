"""
Módulo de recomendaciones para optimización de alimentación basada en eficiencia nutricional.
"""
from django.db.models import Avg, Min, Max, F, Q
from django.utils import timezone
from datetime import timedelta
from produccion.models import SeguimientoEngorde, Lote
from inventario.models import Alimento

def analizar_eficiencia_nutricional(lote_id=None, galpon_id=None, dias=30):
    """
    Analiza la eficiencia nutricional de un lote o galpón específico y genera recomendaciones.
    
    Args:
        lote_id: ID del lote a analizar (opcional)
        galpon_id: ID del galpón a analizar (opcional)
        dias: Número de días hacia atrás para analizar (por defecto 30)
        
    Returns:
        dict: Diccionario con análisis y recomendaciones
    """
    fecha_limite = timezone.now().date() - timedelta(days=dias)
    
    # Construir la consulta base
    query = SeguimientoEngorde.objects.select_related(
        'seguimiento_diario__lote',
        'seguimiento_diario__lote__alimento',
        'seguimiento_diario__lote__galpon'
    ).filter(
        seguimiento_diario__fecha_seguimiento__gte=fecha_limite,
        eficiencia_energetica__isnull=False,
        eficiencia_proteica__isnull=False
    )
    
    # Filtrar por lote o galpón si se especifica
    if lote_id:
        query = query.filter(seguimiento_diario__lote_id=lote_id)
    elif galpon_id:
        query = query.filter(seguimiento_diario__lote__galpon_id=galpon_id)
    
    # Si no hay datos suficientes, retornar mensaje
    if query.count() < 3:
        return {
            'status': 'error',
            'message': 'No hay suficientes datos para generar recomendaciones (mínimo 3 registros).'
        }
    
    # Calcular promedios y valores óptimos
    stats = query.aggregate(
        avg_eficiencia_energetica=Avg('eficiencia_energetica'),
        min_eficiencia_energetica=Min('eficiencia_energetica'),
        max_eficiencia_energetica=Max('eficiencia_energetica'),
        avg_eficiencia_proteica=Avg('eficiencia_proteica'),
        min_eficiencia_proteica=Min('eficiencia_proteica'),
        max_eficiencia_proteica=Max('eficiencia_proteica'),
        avg_relacion_energia_proteina=Avg('relacion_energia_proteina')
    )
    
    # Obtener el mejor registro (menor eficiencia energética = mejor)
    mejor_registro = query.order_by('eficiencia_energetica').first()
    
    # Inicializar el resultado
    resultado = {
        'status': 'success',
        'estadisticas': stats,
        'recomendaciones': [],
        'mejor_registro': {
            'fecha': mejor_registro.seguimiento_diario.fecha_seguimiento,
            'lote': mejor_registro.seguimiento_diario.lote.codigo_lote,
            'alimento': mejor_registro.seguimiento_diario.lote.alimento.nombre if mejor_registro.seguimiento_diario.lote.alimento else 'No especificado',
            'eficiencia_energetica': mejor_registro.eficiencia_energetica,
            'eficiencia_proteica': mejor_registro.eficiencia_proteica,
            'relacion_energia_proteina': mejor_registro.relacion_energia_proteina
        }
    }
    
    # Generar recomendaciones basadas en los datos
    if stats['avg_eficiencia_energetica'] > 3.5:
        resultado['recomendaciones'].append({
            'tipo': 'alerta',
            'mensaje': 'La eficiencia energética promedio es deficiente (>3.5 kcal/g).',
            'accion': 'Considere aumentar la densidad energética del alimento o revisar factores ambientales que puedan estar causando estrés en las aves.'
        })
    elif stats['avg_eficiencia_energetica'] > 3.0:
        resultado['recomendaciones'].append({
            'tipo': 'advertencia',
            'mensaje': 'La eficiencia energética promedio es aceptable pero puede mejorarse.',
            'accion': 'Evalúe la posibilidad de ajustar la formulación del alimento para mejorar la digestibilidad de la energía.'
        })
    else:
        resultado['recomendaciones'].append({
            'tipo': 'positivo',
            'mensaje': 'La eficiencia energética promedio es buena (<3.0 kcal/g).',
            'accion': 'Mantenga las prácticas actuales de alimentación y manejo.'
        })
    
    if stats['avg_eficiencia_proteica'] > 0.45:
        resultado['recomendaciones'].append({
            'tipo': 'alerta',
            'mensaje': 'La eficiencia proteica promedio es deficiente (>0.45 g/g).',
            'accion': 'Considere ajustar el perfil de aminoácidos del alimento o mejorar la calidad de las fuentes proteicas.'
        })
    elif stats['avg_eficiencia_proteica'] > 0.40:
        resultado['recomendaciones'].append({
            'tipo': 'advertencia',
            'mensaje': 'La eficiencia proteica promedio es aceptable pero puede mejorarse.',
            'accion': 'Evalúe la posibilidad de suplementar con aminoácidos sintéticos para mejorar el balance proteico.'
        })
    else:
        resultado['recomendaciones'].append({
            'tipo': 'positivo',
            'mensaje': 'La eficiencia proteica promedio es buena (<0.40 g/g).',
            'accion': 'Mantenga las prácticas actuales de alimentación proteica.'
        })
    
    # Recomendaciones sobre la relación energía/proteína
    if stats['avg_relacion_energia_proteina'] < 130 or stats['avg_relacion_energia_proteina'] > 170:
        resultado['recomendaciones'].append({
            'tipo': 'alerta',
            'mensaje': f"La relación energía/proteína promedio está desequilibrada ({stats['avg_relacion_energia_proteina']:.1f}).",
            'accion': 'Ajuste la formulación del alimento para alcanzar una relación entre 140-160.'
        })
    elif stats['avg_relacion_energia_proteina'] < 140 or stats['avg_relacion_energia_proteina'] > 160:
        resultado['recomendaciones'].append({
            'tipo': 'advertencia',
            'mensaje': f"La relación energía/proteína promedio es aceptable pero no óptima ({stats['avg_relacion_energia_proteina']:.1f}).",
            'accion': 'Considere pequeños ajustes en la formulación para optimizar la relación energía/proteína.'
        })
    else:
        resultado['recomendaciones'].append({
            'tipo': 'positivo',
            'mensaje': f"La relación energía/proteína promedio es óptima ({stats['avg_relacion_energia_proteina']:.1f}).",
            'accion': 'Mantenga el balance actual entre energía y proteína en la dieta.'
        })
    
    # Añadir recomendación de alimento basada en el mejor registro
    if mejor_registro.seguimiento_diario.lote.alimento:
        mejor_alimento = mejor_registro.seguimiento_diario.lote.alimento
        alimentos_similares = Alimento.objects.filter(
            etapa=mejor_alimento.etapa
        ).exclude(
            id=mejor_alimento.id
        )[:3]
        
        resultado['recomendaciones'].append({
            'tipo': 'informacion',
            'mensaje': f"El mejor rendimiento se obtuvo con el alimento '{mejor_alimento.nombre}'.",
            'accion': f"Considere utilizar este alimento o similares para otros lotes en la misma etapa de crecimiento."
        })
        
        if alimentos_similares:
            resultado['alimentos_recomendados'] = [
                {
                    'id': alimento.id,
                    'nombre': alimento.nombre,
                    'etapa': alimento.get_etapa_display(),
                    'energia': alimento.energia_metabolizable,
                    'proteina': alimento.contenido_proteina
                }
                for alimento in alimentos_similares
            ]
    
    return resultado

def obtener_recomendaciones_lote(lote_id, dias=30):
    """
    Obtiene recomendaciones específicas para un lote.
    
    Args:
        lote_id: ID del lote
        dias: Número de días hacia atrás para analizar
        
    Returns:
        dict: Recomendaciones para el lote
    """
    try:
        lote = Lote.objects.get(id=lote_id)
        resultado = analizar_eficiencia_nutricional(lote_id=lote_id, dias=dias)
        
        if resultado['status'] == 'success':
            # Añadir información específica del lote
            resultado['lote'] = {
                'id': lote.id,
                'codigo': lote.codigo_lote,
                'edad_semanas': lote.edad_semanas,
                'galpon': lote.galpon.numero_galpon,
                'raza': lote.raza.nombre,
                'alimento_actual': lote.alimento.nombre if lote.alimento else 'No especificado'
            }
            
            # Recomendaciones específicas basadas en la edad
            if lote.edad_semanas < 3:
                resultado['recomendaciones'].append({
                    'tipo': 'informacion',
                    'mensaje': 'Lote en etapa inicial de crecimiento.',
                    'accion': 'Asegúrese de proporcionar un alimento con alto contenido proteico (>21%) para un desarrollo óptimo.'
                })
            elif lote.edad_semanas < 6:
                resultado['recomendaciones'].append({
                    'tipo': 'informacion',
                    'mensaje': 'Lote en etapa de crecimiento.',
                    'accion': 'Balance adecuado de energía y proteína es crucial en esta etapa para el desarrollo muscular.'
                })
            else:
                resultado['recomendaciones'].append({
                    'tipo': 'informacion',
                    'mensaje': 'Lote en etapa de finalización.',
                    'accion': 'Considere un alimento con mayor contenido energético para mejorar la ganancia de peso final.'
                })
        
        return resultado
    
    except Lote.DoesNotExist:
        return {
            'status': 'error',
            'message': f'No se encontró el lote con ID {lote_id}.'
        }

def obtener_recomendaciones_galpon(galpon_id, dias=30):
    """
    Obtiene recomendaciones específicas para un galpón.
    
    Args:
        galpon_id: ID del galpón
        dias: Número de días hacia atrás para analizar
        
    Returns:
        dict: Recomendaciones para el galpón
    """
    from produccion.models import Galpon
    
    try:
        galpon = Galpon.objects.get(id=galpon_id)
        resultado = analizar_eficiencia_nutricional(galpon_id=galpon_id, dias=dias)
        
        if resultado['status'] == 'success':
            # Añadir información específica del galpón
            resultado['galpon'] = {
                'id': galpon.id,
                'numero': galpon.numero_galpon,
                'tipo': galpon.get_tipo_galpon_display(),
                'capacidad': galpon.capacidad_aves,
                'lotes_activos': galpon.lotes.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']).count()
            }
            
            # Recomendaciones específicas basadas en el tipo de galpón
            if galpon.tipo_galpon == 'CRIA':
                resultado['recomendaciones'].append({
                    'tipo': 'informacion',
                    'mensaje': 'Galpón de cría requiere especial atención en la eficiencia proteica.',
                    'accion': 'Monitoree de cerca el consumo de alimento y ajuste la densidad de aves si es necesario.'
                })
            elif galpon.tipo_galpon == 'PRODUCCION':
                resultado['recomendaciones'].append({
                    'tipo': 'informacion',
                    'mensaje': 'Galpón de producción debe mantener un balance óptimo de nutrientes.',
                    'accion': 'Evalúe regularmente la conversión alimenticia y ajuste la formulación según sea necesario.'
                })
        
        return resultado
    
    except Galpon.DoesNotExist:
        return {
            'status': 'error',
            'message': f'No se encontró el galpón con ID {galpon_id}.'
        }
