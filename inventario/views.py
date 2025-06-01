from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Sum, F
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, NoReverseMatch, reverse_lazy
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

def debug_urls(request):
    """Vista de depuración para verificar la resolución de URLs"""
    url_tests = [
        ('inventario:registrar_consumo', {}),
        ('registrar_consumo', {}),
    ]
    
    results = []
    for name, kwargs in url_tests:
        try:
            url = reverse(name, kwargs=kwargs)
            results.append(f"✓ {name} -> {url}")
        except NoReverseMatch as e:
            results.append(f"✗ {name} -> Error: {str(e)}")
    
    return HttpResponse("<pre>" + "\n".join(results) + "</pre>")

# Importar modelos
from .models import Alimento, ConsumoAlimento, Vacuna, AplicacionVacuna, Insumo, Proveedor
from produccion.models import Lote, SeguimientoDiario
from django.forms import ModelForm
from django.db import transaction
from django.core.exceptions import ValidationError

@login_required
def seguimiento_lote(request, lote_id):
    """Vista para mostrar historial de seguimiento de un lote específico"""
    try:
        from produccion.models import Lote, SeguimientoDiario
        
        # Obtener el lote de la base de datos
        lote = get_object_or_404(Lote, id=lote_id)
        
        # Obtener los seguimientos de la base de datos (ordenados por fecha ascendente)
        seguimientos = SeguimientoDiario.objects.filter(
            lote=lote
        ).select_related('lote', 'registrado_por').order_by('fecha_seguimiento')
        
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

# Vistas para Alimentos
@login_required
def lista_alimentos(request):
    """Vista para listar todos los alimentos disponibles"""
    try:
        alimentos = Alimento.objects.all().order_by('nombre')
        
        context = {
            'title': 'Alimentos',
            'alimentos': alimentos
        }
        return render(request, 'inventario/lista_alimentos.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar los alimentos: {str(e)}")
        return redirect('inventario:inicio')

@login_required
def detalle_alimento(request, alimento_id):
    """Vista para mostrar detalles de un alimento específico"""
    try:
        alimento = get_object_or_404(Alimento, id=alimento_id)
        
        # Obtener el consumo total de este alimento
        consumo_total = ConsumoAlimento.objects.filter(
            alimento=alimento
        ).aggregate(total=Sum('cantidad_kg'))['total'] or 0
        
        context = {
            'title': f'Alimento: {alimento.nombre}',
            'alimento': alimento,
            'consumo_total': consumo_total
        }
        return render(request, 'inventario/detalle_alimento.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el detalle del alimento: {str(e)}")
        return redirect('inventario:lista_alimentos')

@login_required
def registrar_consumo(request):
    """Vista para registrar consumo de alimento"""
    if request.method == 'POST':
        try:
            alimento_id = request.POST.get('alimento')
            cantidad = float(request.POST.get('cantidad', 0))
            lote_id = request.POST.get('lote')
            fecha = request.POST.get('fecha') or timezone.now().date()
            
            with transaction.atomic():
                # Registrar el consumo
                consumo = ConsumoAlimento.objects.create(
                    alimento_id=alimento_id,
                    lote_id=lote_id,
                    cantidad_kg=cantidad,
                    fecha_consumo=fecha,
                    registrado_por=request.user
                )
                
                # Actualizar el stock del alimento
                alimento = Alimento.objects.get(id=alimento_id)
                alimento.stock_kg -= cantidad
                alimento.save()
                
                messages.success(request, f'Consumo de {cantidad} kg de {alimento.nombre} registrado correctamente.')
                return redirect('inventario:lista_alimentos')
                
        except Exception as e:
            messages.error(request, f'Error al registrar el consumo: {str(e)}')
            return redirect('inventario:registrar_consumo')
    else:
        # Mostrar formulario para registrar consumo
        alimentos = Alimento.objects.filter(stock_kg__gt=0)
        # Filtra lotes que estén en estado INICIAL, CRECIMIENTO o PRODUCCION
        lotes = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
        
        context = {
            'title': 'Registrar Consumo de Alimento',
            'alimentos': alimentos,
            'lotes': lotes,
            'hoy': timezone.now().date()
        }
        return render(request, 'inventario/registrar_consumo.html', context)

# Vistas para Vacunas
# ============================================
# Vistas para Medicamentos
# ============================================

class MedicamentoForm(ModelForm):
    class Meta:
        model = Insumo
        fields = [
            'nombre', 'descripcion', 'proveedor', 'stock', 'unidad_medida',
            'stock_minimo', 'precio_unitario', 'fecha_vencimiento', 'lote', 'activo'
        ]
        labels = {
            'nombre': 'Nombre del Medicamento',
            'descripcion': 'Descripción',
            'proveedor': 'Laboratorio/Proveedor',
            'stock': 'Cantidad en Stock',
            'unidad_medida': 'Unidad de Medida',
            'stock_minimo': 'Stock Mínimo',
            'precio_unitario': 'Precio Unitario',
            'fecha_vencimiento': 'Fecha de Vencimiento',
            'lote': 'Lote',
            'activo': 'Activo'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.objects.all()
        self.fields['tipo_insumo'].initial = 'MEDICAMENTO'
        self.fields['tipo_insumo'].widget.attrs['readonly'] = True
        self.fields['tipo_insumo'].widget.attrs['hidden'] = True

@login_required
def lista_medicamentos(request):
    """Vista para listar todos los medicamentos disponibles"""
    try:
        # Filtrar solo los insumos que son medicamentos
        medicamentos = Insumo.objects.filter(tipo_insumo='MEDICAMENTO').order_by('nombre')
        
        # Contar medicamentos con stock bajo
        stock_bajo = medicamentos.filter(stock__lt=F('stock_minimo')).count()
        
        context = {
            'title': 'Medicamentos',
            'medicamentos': medicamentos,
            'stock_bajo': stock_bajo
        }
        return render(request, 'inventario/medicamentos/lista_medicamentos.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar los medicamentos: {str(e)}")
        return redirect('inventario:lista_medicamentos')

@login_required
def detalle_medicamento(request, medicamento_id):
    """Vista para mostrar los detalles de un medicamento específico"""
    try:
        medicamento = get_object_or_404(Insumo, id=medicamento_id, tipo_insumo='MEDICAMENTO')
        
        # Obtener el historial de aplicaciones de este medicamento
        aplicaciones = AplicacionMedicamento.objects.filter(
            medicamento=medicamento
        ).select_related('lote', 'aplicado_por').order_by('-fecha_aplicacion')
        
        context = {
            'title': f'Medicamento: {medicamento.nombre}',
            'medicamento': medicamento,
            'aplicaciones': aplicaciones
        }
        return render(request, 'inventario/medicamentos/detalle_medicamento.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el detalle del medicamento: {str(e)}")
        return redirect('inventario:lista_medicamentos')

@login_required
def nuevo_medicamento(request):
    """Vista para agregar un nuevo medicamento"""
    if request.method == 'POST':
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    medicamento = form.save(commit=False)
                    medicamento.tipo_insumo = 'MEDICAMENTO'  # Asegurarse que sea un medicamento
                    medicamento.save()
                    
                    messages.success(request, f'Medicamento {medicamento.nombre} registrado correctamente.')
                    return redirect('inventario:detalle_medicamento', medicamento_id=medicamento.id)
            except Exception as e:
                messages.error(request, f'Error al guardar el medicamento: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = MedicamentoForm()
    
    context = {
        'title': 'Nuevo Medicamento',
        'form': form,
        'is_new': True
    }
    return render(request, 'inventario/medicamentos/form_medicamento.html', context)

@login_required
def editar_medicamento(request, medicamento_id):
    """Vista para editar un medicamento existente"""
    medicamento = get_object_or_404(Insumo, id=medicamento_id, tipo_insumo='MEDICAMENTO')
    
    if request.method == 'POST':
        form = MedicamentoForm(request.POST, instance=medicamento)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, f'Medicamento {medicamento.nombre} actualizado correctamente.')
                    return redirect('inventario:detalle_medicamento', medicamento_id=medicamento.id)
            except Exception as e:
                messages.error(request, f'Error al actualizar el medicamento: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario.')
    else:
        form = MedicamentoForm(instance=medicamento)
    
    context = {
        'title': f'Editar Medicamento: {medicamento.nombre}',
        'form': form,
        'medicamento': medicamento,
        'is_edit': True
    }
    return render(request, 'inventario/medicamentos/form_medicamento.html', context)

@login_required
def eliminar_medicamento(request, medicamento_id):
    """Vista para eliminar un medicamento"""
    medicamento = get_object_or_404(Insumo, id=medicamento_id, tipo_insumo='MEDICAMENTO')
    
    if request.method == 'POST':
        try:
            nombre = medicamento.nombre
            medicamento.delete()
            messages.success(request, f'Medicamento {nombre} eliminado correctamente.')
            return redirect('inventario:lista_medicamentos')
        except Exception as e:
            messages.error(request, f'Error al eliminar el medicamento: {str(e)}')
            return redirect('inventario:detalle_medicamento', medicamento_id=medicamento.id)
    
    context = {
        'title': 'Eliminar Medicamento',
        'medicamento': medicamento
    }
    return render(request, 'inventario/medicamentos/confirmar_eliminar_medicamento.html', context)

@login_required
def registrar_aplicacion_medicamento(request):
    """Vista para registrar la aplicación de un medicamento a un lote"""
    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Obtener datos del formulario
                medicamento_id = request.POST.get('medicamento')
                lote_id = request.POST.get('lote')
                dosis = float(request.POST.get('dosis', 0))
                fecha_aplicacion = request.POST.get('fecha_aplicacion') or timezone.now().date()
                via_aplicacion = request.POST.get('via_aplicacion', '')
                observaciones = request.POST.get('observaciones', '')
                
                # Validar que el medicamento existe y es un medicamento
                medicamento = get_object_or_404(Insumo, id=medicamento_id, tipo_insumo='MEDICAMENTO')
                
                # Validar que hay suficiente stock
                if medicamento.stock < dosis:
                    raise ValidationError(f'No hay suficiente stock de {medicamento.nombre}. Stock disponible: {medicamento.stock} {medicamento.unidad_medida}')
                
                # Registrar la aplicación
                aplicacion = AplicacionMedicamento.objects.create(
                    medicamento=medicamento,
                    lote_id=lote_id,
                    dosis=dosis,
                    fecha_aplicacion=fecha_aplicacion,
                    via_aplicacion=via_aplicacion,
                    observaciones=observaciones,
                    aplicada_por=request.user
                )
                
                # Actualizar el stock del medicamento
                medicamento.stock -= dosis
                medicamento.save()
                
                messages.success(request, f'Aplicación de {medicamento.nombre} registrada correctamente.')
                return redirect('inventario:detalle_medicamento', medicamento_id=medicamento.id)
                
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, f'Error al registrar la aplicación: {str(e)}')
            
        # Si hay un error, redirigir de nuevo al formulario con los datos ingresados
        return redirect('inventario:registrar_aplicacion_medicamento')
    else:
        # Mostrar formulario para registrar aplicación
        medicamentos = Insumo.objects.filter(tipo_insumo='MEDICAMENTO', stock__gt=0)
        lotes = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
        
        context = {
            'title': 'Registrar Aplicación de Medicamento',
            'medicamentos': medicamentos,
            'lotes': lotes,
            'hoy': timezone.now().date(),
            'vias_aplicacion': [
                ('Oral', 'Vía Oral'),
                ('Inyectable', 'Inyección'),
                ('Agua de Bebida', 'Agua de Bebida'),
                ('Otra', 'Otra')
            ]
        }
        return render(request, 'inventario/medicamentos/registrar_aplicacion.html', context)

# ============================================
# Vistas para Vacunas
# ============================================
@login_required
def lista_vacunas(request):
    """Vista para listar todas las vacunas disponibles"""
    try:
        vacunas = Vacuna.objects.all().order_by('nombre_comercial')
        
        context = {
            'title': 'Vacunas',
            'vacunas': vacunas
        }
        return render(request, 'inventario/lista_vacunas.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar las vacunas: {str(e)}")
        return redirect('inventario:lista_alimentos')

@login_required
def detalle_vacuna(request, vacuna_id):
    """Vista para mostrar detalles de una vacuna específica"""
    try:
        vacuna = get_object_or_404(Vacuna, id=vacuna_id)
        aplicaciones = AplicacionVacuna.objects.filter(vacuna=vacuna).select_related('lote', 'aplicada_por')
        
        context = {
            'title': f'Vacuna: {vacuna.nombre}',
            'vacuna': vacuna,
            'aplicaciones': aplicaciones
        }
        return render(request, 'inventario/detalle_vacuna.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el detalle de la vacuna: {str(e)}")
        return redirect('inventario:lista_vacunas')

@login_required
def registrar_aplicacion(request):
    """Vista para registrar aplicación de vacuna"""
    if request.method == 'POST':
        try:
            vacuna_id = request.POST.get('vacuna')
            lote_id = request.POST.get('lote')
            fecha = request.POST.get('fecha') or timezone.now().date()
            dosis = float(request.POST.get('dosis', 0))
            observaciones = request.POST.get('observaciones', '')
            
            with transaction.atomic():
                # Registrar la aplicación
                aplicacion = AplicacionVacuna.objects.create(
                    vacuna_id=vacuna_id,
                    lote_id=lote_id,
                    fecha_aplicacion=fecha,
                    dosis_ml=dosis,
                    observaciones=observaciones,
                    aplicada_por=request.user
                )
                
                # Actualizar el stock de la vacuna
                vacuna = Vacuna.objects.get(id=vacuna_id)
                vacuna.stock_ml -= dosis
                vacuna.save()
                
                messages.success(request, f'Aplicación de {vacuna.nombre} registrada correctamente.')
                return redirect('inventario:lista_vacunas')
                
        except Exception as e:
            messages.error(request, f'Error al registrar la aplicación: {str(e)}')
            return redirect('inventario:registrar_aplicacion')
    else:
        # Mostrar formulario para registrar aplicación
        vacunas = Vacuna.objects.filter(stock_ml__gt=0)
        lotes = Lote.objects.filter(activo=True)
        
        context = {
            'title': 'Registrar Aplicación de Vacuna',
            'vacunas': vacunas,
            'lotes': lotes,
            'hoy': timezone.now().date()
        }
        return render(request, 'inventario/registrar_aplicacion.html', context)

# Vistas para Seguimiento de Lotes
@login_required
def registro_seguimiento(request):
    """Vista para listar lotes disponibles para registro de seguimiento"""
    try:
        lotes = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']).select_related('galpon', 'raza')
        
        context = {
            'title': 'Seguimiento de Lotes',
            'lotes': lotes
        }
        return render(request, 'inventario/registro_seguimiento.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar los lotes: {str(e)}")
        return redirect('inventario:inicio')

@login_required
def nuevo_seguimiento(request, lote_id):
    """Vista para registrar un nuevo seguimiento para un lote específico"""
    lote = get_object_or_404(Lote, id=lote_id)
    
    if request.method == 'POST':
        try:
            fecha = request.POST.get('fecha') or timezone.now().date()
            peso_promedio = float(request.POST.get('peso_promedio', 0)) / 1000  # Convertir a kg
            consumo_alimento = float(request.POST.get('consumo_alimento', 0))
            mortalidad = int(request.POST.get('mortalidad', 0))
            observaciones = request.POST.get('observaciones', '')
            
            with transaction.atomic():
                # Actualizar datos del lote
                lote.peso_promedio_ave = peso_promedio
                lote.ultimo_consumo_alimento = consumo_alimento
                lote.ultima_actualizacion = timezone.now()
                
                # Guardar el lote con los datos actualizados
                lote.save()
                
                # Registrar seguimiento
                seguimiento = SeguimientoDiario.objects.create(
                    lote=lote,
                    fecha_seguimiento=fecha,
                    peso_promedio_ave=peso_promedio,
                    consumo_alimento_kg=consumo_alimento,
                    mortalidad=mortalidad,
                    observaciones=observaciones,
                    registrado_por=request.user
                )
                
                # Registrar la mortalidad si existe
                if mortalidad > 0:
                    from produccion.models import MortalidadDiaria
                    from datetime import datetime
                    
                    # Convertir la fecha de string a objeto date si es necesario
                    if isinstance(fecha, str):
                        try:
                            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            # Si hay un error en el formato, usar la fecha actual
                            fecha_obj = timezone.now().date()
                    else:
                        fecha_obj = fecha
                    
                    mortalidad_diaria = MortalidadDiaria(
                        lote=lote,
                        fecha=fecha_obj,  # Usar el objeto date
                        cantidad_muertes=mortalidad,
                        causa='Registrado en seguimiento diario',
                        observaciones=observaciones or 'Mortalidad registrada automáticamente desde el seguimiento diario'
                    )
                    mortalidad_diaria.save()
                
                messages.success(request, 'Seguimiento registrado correctamente.')
                return redirect('inventario:seguimiento_lote', lote_id=lote.id)
                
        except Exception as e:
            messages.error(request, f'Error al registrar el seguimiento: {str(e)}')
            return redirect('inventario:nuevo_seguimiento', lote_id=lote.id)
    else:
        # Mostrar formulario para nuevo seguimiento
        hoy = timezone.now().date()
        
        context = {
            'title': f'Nuevo Seguimiento - {lote.codigo_lote}',
            'lote': lote,
            'hoy': hoy,
            'siguiente_seguimiento': hoy
        }
        return render(request, 'inventario/nuevo_seguimiento.html', context)
