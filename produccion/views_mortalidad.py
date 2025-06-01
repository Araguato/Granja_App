"""
Vistas personalizadas para el manejo de mortalidad diaria.
Estas vistas proporcionan una alternativa al panel de administración de Django
para que los supervisores puedan registrar la mortalidad diaria.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum

# Importar modelos cuando estén disponibles
# from .models import Lote, MortalidadDiaria

@login_required
def lista_mortalidad(request):
    """Vista para listar los registros de mortalidad diaria."""
    try:
        # En un sistema real, obtendríamos los datos de la base de datos
        # registros = MortalidadDiaria.objects.all().order_by('-fecha')
        
        # Por ahora, usamos datos de ejemplo
        registros_ejemplo = [
            {'id': 1, 'lote': 'L001', 'fecha': timezone.now().date(), 'cantidad_muertes': 5, 'causa': 'Enfermedad respiratoria'},
            {'id': 2, 'lote': 'L002', 'fecha': timezone.now().date() - timezone.timedelta(days=1), 'cantidad_muertes': 3, 'causa': 'Causas naturales'},
            {'id': 3, 'lote': 'L001', 'fecha': timezone.now().date() - timezone.timedelta(days=2), 'cantidad_muertes': 2, 'causa': 'Estrés térmico'},
        ]
        
        context = {
            'title': 'Registro de Mortalidad Diaria',
            'registros': registros_ejemplo
        }
        return render(request, 'produccion/mortalidad/lista_mortalidad.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar los registros de mortalidad: {str(e)}")
        return redirect('dashboard')

@login_required
def nueva_mortalidad(request):
    """Vista para registrar una nueva mortalidad diaria."""
    try:
        # En un sistema real, obtendríamos los lotes de la base de datos
        # lotes = Lote.objects.filter(estado='ACTIVO')
        
        # Por ahora, usamos datos de ejemplo
        lotes_ejemplo = [
            {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 1', 'cantidad_aves': 1000},
            {'id': 2, 'codigo': 'L002', 'galpon': 'Galpón 2', 'cantidad_aves': 1500},
            {'id': 3, 'codigo': 'L003', 'galpon': 'Galpón 3', 'cantidad_aves': 2000},
        ]
        
        if request.method == 'POST':
            # Capturar datos del formulario
            lote_id = request.POST.get('lote')
            fecha = request.POST.get('fecha')
            cantidad_muertes = request.POST.get('cantidad_muertes')
            causa = request.POST.get('causa', '')
            
            # Validar datos
            if not lote_id or not fecha or not cantidad_muertes:
                messages.error(request, "Por favor complete todos los campos obligatorios")
                return render(request, 'produccion/mortalidad/nueva_mortalidad.html', {
                    'title': 'Nuevo Registro de Mortalidad',
                    'lotes': lotes_ejemplo,
                    'fecha_actual': timezone.now().date()
                })
            
            # En un sistema real, guardaríamos en la base de datos
            # lote = get_object_or_404(Lote, id=lote_id)
            # mortalidad = MortalidadDiaria(
            #     lote=lote,
            #     fecha=fecha,
            #     cantidad_muertes=cantidad_muertes,
            #     causa=causa
            # )
            # mortalidad.save()
            
            # Imprimir para depuración
            print(f"Nuevo registro de mortalidad:")
            print(f"Lote: {lote_id}")
            print(f"Fecha: {fecha}")
            print(f"Cantidad de muertes: {cantidad_muertes}")
            print(f"Causa: {causa}")
            
            messages.success(request, "Registro de mortalidad guardado correctamente")
            return redirect('lista_mortalidad')
        
        context = {
            'title': 'Nuevo Registro de Mortalidad',
            'lotes': lotes_ejemplo,
            'fecha_actual': timezone.now().date()
        }
        return render(request, 'produccion/mortalidad/nueva_mortalidad.html', context)
    except Exception as e:
        messages.error(request, f"Error al procesar el formulario: {str(e)}")
        return redirect('lista_mortalidad')

@login_required
def detalle_mortalidad(request, mortalidad_id):
    """Vista para ver el detalle de un registro de mortalidad."""
    try:
        # En un sistema real, obtendríamos el registro de la base de datos
        # mortalidad = get_object_or_404(MortalidadDiaria, id=mortalidad_id)
        
        # Por ahora, usamos datos de ejemplo
        if mortalidad_id == 1:
            mortalidad = {'id': 1, 'lote': 'L001', 'fecha': timezone.now().date(), 'cantidad_muertes': 5, 'causa': 'Enfermedad respiratoria'}
        elif mortalidad_id == 2:
            mortalidad = {'id': 2, 'lote': 'L002', 'fecha': timezone.now().date() - timezone.timedelta(days=1), 'cantidad_muertes': 3, 'causa': 'Causas naturales'}
        else:
            mortalidad = {'id': 3, 'lote': 'L001', 'fecha': timezone.now().date() - timezone.timedelta(days=2), 'cantidad_muertes': 2, 'causa': 'Estrés térmico'}
        
        context = {
            'title': f'Detalle de Mortalidad #{mortalidad_id}',
            'mortalidad': mortalidad
        }
        return render(request, 'produccion/mortalidad/detalle_mortalidad.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el detalle: {str(e)}")
        return redirect('lista_mortalidad')

@login_required
def editar_mortalidad(request, mortalidad_id):
    """Vista para editar un registro de mortalidad."""
    try:
        # En un sistema real, obtendríamos el registro y los lotes de la base de datos
        # mortalidad = get_object_or_404(MortalidadDiaria, id=mortalidad_id)
        # lotes = Lote.objects.filter(estado='ACTIVO')
        
        # Por ahora, usamos datos de ejemplo
        lotes_ejemplo = [
            {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 1', 'cantidad_aves': 1000},
            {'id': 2, 'codigo': 'L002', 'galpon': 'Galpón 2', 'cantidad_aves': 1500},
            {'id': 3, 'codigo': 'L003', 'galpon': 'Galpón 3', 'cantidad_aves': 2000},
        ]
        
        if mortalidad_id == 1:
            mortalidad = {'id': 1, 'lote_id': 1, 'fecha': timezone.now().date(), 'cantidad_muertes': 5, 'causa': 'Enfermedad respiratoria'}
        elif mortalidad_id == 2:
            mortalidad = {'id': 2, 'lote_id': 2, 'fecha': timezone.now().date() - timezone.timedelta(days=1), 'cantidad_muertes': 3, 'causa': 'Causas naturales'}
        else:
            mortalidad = {'id': 3, 'lote_id': 1, 'fecha': timezone.now().date() - timezone.timedelta(days=2), 'cantidad_muertes': 2, 'causa': 'Estrés térmico'}
        
        if request.method == 'POST':
            # Capturar datos del formulario
            lote_id = request.POST.get('lote')
            fecha = request.POST.get('fecha')
            cantidad_muertes = request.POST.get('cantidad_muertes')
            causa = request.POST.get('causa', '')
            
            # Validar datos
            if not lote_id or not fecha or not cantidad_muertes:
                messages.error(request, "Por favor complete todos los campos obligatorios")
                return render(request, 'produccion/mortalidad/editar_mortalidad.html', {
                    'title': f'Editar Registro de Mortalidad #{mortalidad_id}',
                    'mortalidad': mortalidad,
                    'lotes': lotes_ejemplo
                })
            
            # En un sistema real, actualizaríamos en la base de datos
            # mortalidad.lote_id = lote_id
            # mortalidad.fecha = fecha
            # mortalidad.cantidad_muertes = cantidad_muertes
            # mortalidad.causa = causa
            # mortalidad.save()
            
            # Imprimir para depuración
            print(f"Actualización de registro de mortalidad #{mortalidad_id}:")
            print(f"Lote: {lote_id}")
            print(f"Fecha: {fecha}")
            print(f"Cantidad de muertes: {cantidad_muertes}")
            print(f"Causa: {causa}")
            
            messages.success(request, "Registro de mortalidad actualizado correctamente")
            return redirect('lista_mortalidad')
        
        context = {
            'title': f'Editar Registro de Mortalidad #{mortalidad_id}',
            'mortalidad': mortalidad,
            'lotes': lotes_ejemplo
        }
        return render(request, 'produccion/mortalidad/editar_mortalidad.html', context)
    except Exception as e:
        messages.error(request, f"Error al procesar el formulario: {str(e)}")
        return redirect('lista_mortalidad')

@login_required
def eliminar_mortalidad(request, mortalidad_id):
    """Vista para eliminar un registro de mortalidad."""
    try:
        # En un sistema real, obtendríamos y eliminaríamos el registro
        # mortalidad = get_object_or_404(MortalidadDiaria, id=mortalidad_id)
        # mortalidad.delete()
        
        # Imprimir para depuración
        print(f"Eliminación de registro de mortalidad #{mortalidad_id}")
        
        messages.success(request, "Registro de mortalidad eliminado correctamente")
        return redirect('lista_mortalidad')
    except Exception as e:
        messages.error(request, f"Error al eliminar el registro: {str(e)}")
        return redirect('lista_mortalidad')
