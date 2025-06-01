from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse, NoReverseMatch
from django.conf import settings

# Importar modelos cuando estén disponibles
# from .models import Alimento, ConsumoAlimento, Vacuna, AplicacionVacuna

@login_required
def seguimiento_lote(request, lote_id):
    """Vista para mostrar historial de seguimiento de un lote específico"""
    try:
        from produccion.models import Lote, SeguimientoDiario
        
        # Obtener el lote de la base de datos
        lote = get_object_or_404(Lote, id=lote_id)
        
        # Obtener los seguimientos de la base de datos
        seguimientos = SeguimientoDiario.objects.filter(
            lote=lote
        ).select_related('lote', 'registrado_por').order_by('-fecha_seguimiento')
        
        # Formatear los datos para la plantilla
        seguimientos_vista = []
        for seguimiento in seguimientos:
            # Calcular la conversión alimenticia (kg alimento / kg peso ganado)
            # Esto es un ejemplo, ajusta según tu lógica de negocio
            conversion = seguimiento.consumo_alimento_kg / (seguimiento.peso_promedio_ave * 1000) if seguimiento.peso_promedio_ave > 0 else 0
            
            seguimientos_vista.append({
                'id': seguimiento.id,
                'fecha': seguimiento.fecha_seguimiento,
                'peso_promedio': float(seguimiento.peso_promedio_ave * 1000),  # Convertir a gramos
                'consumo_alimento': float(seguimiento.consumo_alimento_kg),
                'mortalidad': seguimiento.mortalidad,
                'conversion_alimenticia': round(conversion, 2),
                'energia': 0,  # Este campo no está en el modelo actual
                'observaciones': seguimiento.observaciones or ''
            })
        
        # Crear un diccionario con los datos del lote para la plantilla
        lote_data = {
            'id': lote.id,
            'codigo': lote.codigo_lote,
            'galpon': str(lote.galpon),
            'raza': str(lote.raza) if lote.raza else 'No especificada',
            'edad_semanas': lote.edad_semanas,
            'cantidad_aves': lote.cantidad_inicial_aves,  # Considera calcular las aves actuales
            'estado': lote.get_estado_display()
        }
        
        context = {
            'title': f'Seguimiento: {lote.codigo_lote}',
            'lote': lote_data,
            'seguimientos': seguimientos_vista
        }
        return render(request, 'inventario/seguimiento_lote.html', context)
        
    except Exception as e:
        messages.error(request, f"Error al cargar el seguimiento: {str(e)}")
        return redirect('produccion:lista_lotes')
