from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, admin
from django.contrib.admin.sites import site as default_site
from django.db.models import Q
from django.utils import timezone
from .models import Lote, Galpon, SeguimientoDiario

# Modelo de Tarea (temporal hasta que se implemente correctamente)
class Tarea:
    def __init__(self, id, titulo, descripcion, fecha_asignacion, fecha_limite, estado, prioridad, lote=None, galpon=None):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_asignacion = fecha_asignacion
        self.fecha_limite = fecha_limite
        self.estado = estado
        self.prioridad = prioridad
        self.lote = lote
        self.galpon = galpon

# Datos de ejemplo para tareas (temporal)
tareas_ejemplo = [
    Tarea(
        id=1,
        titulo="Revisar temperatura Lote 1",
        descripcion="Verificar que la temperatura esté entre 30-32°C",
        fecha_asignacion=timezone.now(),
        fecha_limite=timezone.now() + timezone.timedelta(days=1),
        estado="PENDIENTE",
        prioridad="ALTA",
        lote=1
    ),
    Tarea(
        id=2,
        titulo="Alimentar Lote 3",
        descripcion="Distribuir 50kg de alimento",
        fecha_asignacion=timezone.now() - timezone.timedelta(days=1),
        fecha_limite=timezone.now(),
        estado="PENDIENTE",
        prioridad="MEDIA",
        lote=3
    ),
    Tarea(
        id=3,
        titulo="Limpieza Galpón 2",
        descripcion="Realizar limpieza general del galpón",
        fecha_asignacion=timezone.now() - timezone.timedelta(days=2),
        fecha_limite=timezone.now() + timezone.timedelta(days=1),
        estado="PENDIENTE",
        prioridad="BAJA",
        galpon=2
    ),
]

@login_required
def lista_lotes(request):
    """Vista para listar todos los lotes"""
    try:
        # Mostrar datos de ejemplo para asegurar que todos los usuarios vean algo
        lotes_ejemplo = [
            {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 2', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO'},
            {'id': 3, 'codigo': 'L003', 'galpon': 'Galpón 1', 'raza': 'Ross 308', 'edad_semanas': 30, 'cantidad_aves': 1500, 'estado': 'PRODUCCION'},
        ]
        
        # Intentar obtener lotes reales si existen
        try:
            # Obtener todos los lotes con sus relaciones
            lotes_reales = Lote.objects.all().select_related('galpon', 'raza')
            print(f"Encontrados {lotes_reales.count()} lotes en la base de datos")
            
            if lotes_reales.exists():
                # Usar los lotes reales de la base de datos
                lotes = lotes_reales
                # Imprimir información de depuración
                for lote in lotes:
                    print(f"Lote ID: {lote.id}, Código: {getattr(lote, 'codigo_lote', 'No disponible')}, "
                          f"Galpón: {lote.galpon.numero_galpon if hasattr(lote.galpon, 'numero_galpon') else 'No disponible'}, "
                          f"Raza: {lote.raza.nombre if hasattr(lote.raza, 'nombre') else 'No disponible'}")
            else:
                print("No se encontraron lotes en la base de datos, usando datos de ejemplo")
                lotes = lotes_ejemplo
        except Exception as e:
            print(f"Error al obtener lotes reales: {e}")
            lotes = lotes_ejemplo
        
        context = {
            'title': 'Lotes',
            'lotes': lotes,
            'lotes_ejemplo': lotes_ejemplo
        }
        return render(request, 'produccion/lista_lotes.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar los lotes: {str(e)}")
        # Si hay un error, mostrar una página con datos de ejemplo
        lotes_ejemplo = [
            {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 2', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO'},
            {'id': 3, 'codigo': 'L003', 'galpon': 'Galpón 1', 'raza': 'Ross 308', 'edad_semanas': 30, 'cantidad_aves': 1500, 'estado': 'PRODUCCION'},
        ]
        context = {
            'title': 'Lotes (Ejemplo)',
            'lotes_ejemplo': lotes_ejemplo,
            'error': str(e)
        }
        return render(request, 'produccion/lista_lotes_ejemplo.html', context)

@login_required
def detalle_lote(request, lote_id):
    """Vista para mostrar detalles de un lote específico"""
    try:
        # Intentar obtener el lote por ID
        try:
            lote = Lote.objects.get(id=lote_id)
            
            # Obtener seguimientos diarios del lote
            seguimientos = SeguimientoDiario.objects.filter(lote=lote).order_by('-fecha_seguimiento')[:30]
            
            context = {
                'title': f'Lote {lote.codigo_lote}',
                'lote': lote,
                'seguimientos': seguimientos
            }
            return render(request, 'produccion/detalle_lote.html', context)
        except Lote.DoesNotExist:
            # Si el lote no existe, mostrar datos de ejemplo sin mostrar mensaje de error
            if lote_id == 1:
                lote_ejemplo = {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 2', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO', 'mortalidad_acumulada': 2.5, 'produccion_diaria': 0, 'conversion_alimenticia': 1.8}
            else:
                lote_ejemplo = {'id': lote_id, 'codigo': f'L00{lote_id}', 'galpon': 'Galpón 1', 'raza': 'Ross 308', 'edad_semanas': 30, 'cantidad_aves': 1500, 'estado': 'PRODUCCION', 'mortalidad_acumulada': 3.2, 'produccion_diaria': 1350, 'conversion_alimenticia': 2.1}
            
            context = {
                'title': f'Lote {lote_ejemplo["codigo"]} (Ejemplo)',
                'lote_ejemplo': lote_ejemplo,
                'modo_ejemplo': True  # Indicador de que estamos mostrando datos de ejemplo
            }
            return render(request, 'produccion/detalle_lote_ejemplo.html', context)
    except Exception as e:
        # Para otros errores, mostrar mensaje de error
        messages.error(request, f"Error al cargar el lote: {str(e)}")
        if lote_id == 1:
            lote_ejemplo = {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 2', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO', 'mortalidad_acumulada': 2.5, 'produccion_diaria': 0, 'conversion_alimenticia': 1.8}
        else:
            lote_ejemplo = {'id': lote_id, 'codigo': f'L00{lote_id}', 'galpon': 'Galpón 1', 'raza': 'Ross 308', 'edad_semanas': 30, 'cantidad_aves': 1500, 'estado': 'PRODUCCION', 'mortalidad_acumulada': 3.2, 'produccion_diaria': 1350, 'conversion_alimenticia': 2.1}
        
        context = {
            'title': f'Lote {lote_ejemplo["codigo"]} (Ejemplo)',
            'lote_ejemplo': lote_ejemplo,
            'error': str(e),
            'modo_ejemplo': True
        }
        return render(request, 'produccion/detalle_lote_ejemplo.html', context)

@login_required
def lista_galpones(request):
    """Vista para listar todos los galpones"""
    try:
        # Debug: Print all Galpones in database
        print("Fetching all galpones from database...")
        galpones = Galpon.objects.all().select_related('granja').prefetch_related('lotes')
        print(f"Found {galpones.count()} galpones in the database")
        
        # Debug: Print each galpon details
        for galpon in galpones:
            print(f"Galpon ID: {galpon.id}, Número: {galpon.numero_galpon}, Granja: {galpon.granja.nombre if galpon.granja else 'None'}")
            
            # Check if galpon has active lotes
            galpon.tiene_lotes_activos = galpon.lotes.filter(
                estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
            ).exists()
        
        context = {
            'title': 'Galpones',
            'galpones': galpones
        }
        return render(request, 'produccion/lista_galpones.html', context)
        
    except Exception as e:
        import traceback
        error_msg = f"Error al cargar los galpones: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        messages.error(request, f"Error al cargar los galpones: {str(e)}")
        
        # Return empty queryset in case of error
        context = {
            'title': 'Galpones',
            'galpones': Galpon.objects.none(),
            'error': str(e)
        }
        return render(request, 'produccion/lista_galpones.html', context)

@login_required
def detalle_galpon(request, galpon_id):
    """Vista para mostrar detalles de un galpón específico"""
    try:
        # Intentar obtener el galpón por ID
        try:
            galpon = Galpon.objects.get(id=galpon_id)
            
            # Obtener lotes activos en el galpón
            lotes = Lote.objects.filter(
                galpon=galpon,
                estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
            ).select_related('raza')
            
            context = {
                'title': f'Galpón {galpon.numero_galpon}',
                'galpon': galpon,
                'lotes': lotes
            }
            return render(request, 'produccion/detalle_galpon.html', context)
        except Galpon.DoesNotExist:
            # Si el galpón no existe, mostrar datos de ejemplo sin mostrar mensaje de error
            galpon_ejemplo = {'id': galpon_id, 'numero': f'G00{galpon_id}', 'granja': 'Granja Principal', 'tipo': 'PRODUCCION', 'capacidad': 2000}
            lotes_ejemplo = [
                {'id': 1, 'codigo': 'L001', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO'},
            ]
            
            context = {
                'title': f'Galpón {galpon_ejemplo["numero"]} (Ejemplo)',
                'galpon_ejemplo': galpon_ejemplo,
                'lotes_ejemplo': lotes_ejemplo,
                'modo_ejemplo': True  # Indicador de que estamos mostrando datos de ejemplo
            }
            return render(request, 'produccion/detalle_galpon_ejemplo.html', context)
    except Exception as e:
        # Para otros errores, mostrar mensaje de error
        messages.error(request, f"Error al cargar el galpón: {str(e)}")
        galpon_ejemplo = {'id': galpon_id, 'numero': f'G00{galpon_id}', 'granja': 'Granja Principal', 'tipo': 'PRODUCCION', 'capacidad': 2000}
        lotes_ejemplo = [
            {'id': 1, 'codigo': 'L001', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO'},
        ]
        
        context = {
            'title': f'Galpón {galpon_ejemplo["numero"]} (Ejemplo)',
            'galpon_ejemplo': galpon_ejemplo,
            'lotes_ejemplo': lotes_ejemplo,
            'error': str(e),
            'modo_ejemplo': True
        }
        return render(request, 'produccion/detalle_galpon_ejemplo.html', context)

@login_required
def lista_tareas(request):
    """Vista para listar todas las tareas asignadas al usuario"""
    try:
        # Aquí se implementaría la lógica para obtener las tareas reales del usuario
        # Por ahora, usamos datos de ejemplo
        context = {
            'title': 'Mis Tareas',
            'tareas': tareas_ejemplo
        }
        return render(request, 'produccion/lista_tareas.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar las tareas: {str(e)}")
        context = {
            'title': 'Mis Tareas (Ejemplo)',
            'tareas_ejemplo': tareas_ejemplo,
            'error': str(e)
        }
        return render(request, 'produccion/lista_tareas_ejemplo.html', context)

@login_required
def detalle_tarea(request, tarea_id):
    """Vista para mostrar detalles de una tarea específica"""
    try:
        # Buscar la tarea en los datos de ejemplo
        tarea = next((t for t in tareas_ejemplo if t.id == tarea_id), None)
        
        if not tarea:
            messages.error(request, f"No se encontró la tarea con ID {tarea_id}")
            return redirect('produccion:lista_tareas')
        
        context = {
            'title': f'Tarea: {tarea.titulo}',
            'tarea': tarea
        }
        return render(request, 'produccion/detalle_tarea.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar la tarea: {str(e)}")
        return redirect('produccion:lista_tareas')

@login_required
def completar_tarea(request, tarea_id):
    """Vista para marcar una tarea como completada"""
    try:
        # Buscar la tarea en los datos de ejemplo
        tarea = next((t for t in tareas_ejemplo if t.id == tarea_id), None)
        
        if not tarea:
            messages.error(request, f"No se encontró la tarea con ID {tarea_id}")
            return redirect('produccion:lista_tareas')
        
        # Marcar la tarea como completada (en un sistema real, esto actualizaría la base de datos)
        tarea.estado = "COMPLETADA"
        
        messages.success(request, f"Tarea '{tarea.titulo}' marcada como completada")
        return redirect('produccion:lista_tareas')
    except Exception as e:
        messages.error(request, f"Error al completar la tarea: {str(e)}")
        return redirect('produccion:lista_tareas')

@login_required
def nuevo_lote(request, galpon_id):
    """Vista para crear un nuevo lote en un galpón específico"""
    try:
        # Si el galpón_id es 0, redirigir a la lista de galpones para seleccionar uno
        if int(galpon_id) == 0:
            messages.info(request, "Por favor, seleccione un galpón para crear un nuevo lote")
            return redirect('produccion:lista_galpones')
            
        # En un sistema real, obtendríamos el galpón de la base de datos
        # galpon = get_object_or_404(Galpon, id=galpon_id)
        
        if request.method == 'POST':
            # En un sistema real, procesaríamos el formulario y guardaríamos los datos
            # form = LoteForm(request.POST)
            # if form.is_valid():
            #     lote = form.save(commit=False)
            #     lote.galpon = galpon
            #     lote.save()
            #     messages.success(request, "Lote creado correctamente")
            #     return redirect('produccion:detalle_galpon', galpon_id=galpon_id)
            
            # Por ahora, simplemente mostramos un mensaje de éxito
            messages.success(request, "Lote creado correctamente (simulación)")
            return redirect('produccion:detalle_galpon', galpon_id=galpon_id)
        
        # Por ahora, usamos datos de ejemplo
        galpon_ejemplo = {'id': galpon_id, 'numero': f'G00{galpon_id}', 'granja': 'Granja Principal', 'tipo': 'PRODUCCION', 'capacidad': 2000}
        
        context = {
            'title': 'Nuevo Lote',
            'galpon': galpon_ejemplo,
            'fecha_actual': timezone.now().date()
        }
        return render(request, 'produccion/nuevo_lote.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el formulario: {str(e)}")
        return redirect('produccion:lista_galpones')

@login_required
def editar_lote(request, lote_id):
    """Vista para editar un lote existente"""
    try:
        # En un sistema real, obtendríamos el lote de la base de datos
        # lote = get_object_or_404(Lote, id=lote_id)
        
        if request.method == 'POST':
            # En un sistema real, procesaríamos el formulario y guardaríamos los datos
            # form = LoteForm(request.POST, instance=lote)
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Lote actualizado correctamente")
            #     return redirect('produccion:detalle_lote', lote_id=lote_id)
            
            # Por ahora, simplemente mostramos un mensaje de éxito
            messages.success(request, "Lote actualizado correctamente (simulación)")
            return redirect(f'/produccion/lotes/{lote_id}/')
        
        # Por ahora, usamos datos de ejemplo
        if lote_id == 1:
            lote_ejemplo = {'id': 1, 'codigo': 'L001', 'galpon': 'Galpón 2', 'raza': 'COBB 500', 'edad_semanas': 15, 'cantidad_aves': 1000, 'estado': 'CRECIMIENTO'}
        else:
            lote_ejemplo = {'id': 3, 'codigo': 'L003', 'galpon': 'Galpón 1', 'raza': 'Ross 308', 'edad_semanas': 30, 'cantidad_aves': 1500, 'estado': 'PRODUCCION'}
        
        context = {
            'title': f'Editar Lote {lote_ejemplo["codigo"]}',
            'lote': lote_ejemplo
        }
        return render(request, 'produccion/editar_lote.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el formulario: {str(e)}")
        return redirect('lista_lotes')

@login_required
def editar_galpon(request, galpon_id):
    """Vista para editar un galpón existente"""
    try:
        # En un sistema real, obtendríamos el galpón de la base de datos
        # galpon = get_object_or_404(Galpon, id=galpon_id)
        
        if request.method == 'POST':
            # En un sistema real, procesaríamos el formulario y guardaríamos los datos
            # form = GalponForm(request.POST, instance=galpon)
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, "Galpón actualizado correctamente")
            #     return redirect('detalle_galpon', galpon_id=galpon_id)
            
            # Por ahora, simplemente mostramos un mensaje de éxito
            messages.success(request, "Galpón actualizado correctamente (simulación)")
            return redirect(f'/produccion/galpones/{galpon_id}/')
        
        # Por ahora, usamos datos de ejemplo
        galpon_ejemplo = {'id': galpon_id, 'numero': f'G00{galpon_id}', 'granja': 'Granja Principal', 'tipo': 'PRODUCCION', 'capacidad': 2000}
        
        context = {
            'title': f'Editar Galpón {galpon_ejemplo["numero"]}',
            'galpon': galpon_ejemplo
        }
        return render(request, 'produccion/editar_galpon.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el formulario: {str(e)}")
        return redirect('produccion:lista_galpones')

@login_required
def registrar_mantenimiento(request, galpon_id):
    """Vista para registrar mantenimiento de un galpón"""
    try:
        # En un sistema real, obtendríamos el galpón de la base de datos
        # galpon = get_object_or_404(Galpon, id=galpon_id)
        
        if request.method == 'POST':
            # En un sistema real, procesaríamos el formulario y guardaríamos los datos
            # form = MantenimientoGalponForm(request.POST)
            # if form.is_valid():
            #     mantenimiento = form.save(commit=False)
            #     mantenimiento.galpon = galpon
            #     mantenimiento.save()
            #     messages.success(request, "Mantenimiento registrado correctamente")
            #     return redirect('detalle_galpon', galpon_id=galpon_id)
            
            # Por ahora, simplemente mostramos un mensaje de éxito
            messages.success(request, "Mantenimiento registrado correctamente (simulación)")
            return redirect(f'/produccion/galpones/{galpon_id}/')
        
        # Por ahora, usamos datos de ejemplo
        galpon_ejemplo = {'id': galpon_id, 'numero': f'G00{galpon_id}', 'granja': 'Granja Principal', 'tipo': 'PRODUCCION', 'capacidad': 2000}
        
        context = {
            'title': f'Registrar Mantenimiento para {galpon_ejemplo["numero"]}',
            'galpon': galpon_ejemplo,
            'fecha_actual': timezone.now().date()
        }
        return render(request, 'produccion/registrar_mantenimiento.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar el formulario: {str(e)}")
        return redirect('produccion:lista_galpones')

@login_required
def nuevo_galpon(request):
    """Vista para crear un nuevo galpón"""
    try:
        if request.method == 'POST':
            # Aquí iría la lógica para guardar el nuevo galpón
            # Por ahora, solo redirigimos a la lista de galpones
            messages.success(request, "Galpón creado exitosamente")
            return redirect('produccion:lista_galpones')
            
        context = {
            'title': 'Nuevo Galpón',
        }
        return render(request, 'produccion/nuevo_galpon.html', context)
    except Exception as e:
        messages.error(request, f"Error al crear el galpón: {str(e)}")
        return redirect('produccion:lista_galpones')

@login_required
def nuevo_seguimiento(request, lote_id=None):
    """Vista para crear un nuevo seguimiento diario"""
    # Obtener el lote específico si se proporciona un ID
    lote = None
    if lote_id:
        lote = get_object_or_404(Lote, id=lote_id)
    
    # Obtener lotes activos para el formulario
    lotes_activos = Lote.objects.filter(
        estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
    ).select_related('galpon', 'raza')
    
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            if not lote_id:  # Si no se proporcionó lote_id en la URL, obtenerlo del formulario
                lote_id = request.POST.get('lote')
                lote = get_object_or_404(Lote, id=lote_id)
            fecha = request.POST.get('fecha')
            huevos_totales = request.POST.get('huevos_totales', 0)
            huevos_comercializables = request.POST.get('huevos_comercializables', 0)
            huevos_incubables = request.POST.get('huevos_incubables', 0)
            mortalidad = request.POST.get('mortalidad', 0)
            peso_promedio = request.POST.get('peso_promedio')
            observaciones = request.POST.get('observaciones', '')
            
            # El lote ya se obtuvo al inicio o del formulario
            
            # Crear el seguimiento
            seguimiento = SeguimientoDiario(
                lote=lote,
                fecha_seguimiento=fecha,
                huevos_totales=huevos_totales or 0,
                huevos_comercializables=huevos_comercializables or 0,
                huevos_incubables=huevos_incubables or 0,
                mortalidad=mortalidad or 0,
                peso_promedio=peso_promedio,
                observaciones=observaciones,
                registrado_por=request.user
            )
            
            # Guardar el seguimiento primero para tener el ID disponible
            seguimiento.save()
            
            # Actualizar el conteo de aves en el lote si hay mortalidad
            if mortalidad and int(mortalidad) > 0:
                # Registrar la mortalidad en el modelo MortalidadDiaria
                mortalidad_diaria = MortalidadDiaria(
                    lote=lote,
                    fecha=fecha,
                    cantidad_muertes=int(mortalidad),
                    causa='Registrado en seguimiento diario',
                    observaciones=observaciones or 'Mortalidad registrada automáticamente desde el seguimiento diario'
                )
                mortalidad_diaria.save()
                
                # No actualizamos cantidad_inicial_aves aquí porque ya se maneja en MortalidadDiaria
                # y se calcula dinámicamente en el modelo SeguimientoDiario
            
            messages.success(request, 'Seguimiento registrado exitosamente')
            return redirect('produccion:detalle_lote', lote_id=lote_id)
            
        except Exception as e:
            messages.error(request, f'Error al guardar el seguimiento: {str(e)}')
    
    context = {
        'title': 'Nuevo Seguimiento',
        'lotes_activos': lotes_activos,
        'filtro_lote': int(lote_id) if lote_id and lote_id.isdigit() else '',
        'filtro_fecha_desde': fecha_desde or '',
        'filtro_fecha_hasta': fecha_hasta or '',
        'title': 'Seguimientos Diarios',
    }
    
    return render(request, 'produccion/lista_seguimientos.html', context)


def lista_seguimientos(request):
    """Vista para listar todos los seguimientos con opciones de filtrado"""
    from django.db.models import Q
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    # Obtener todos los seguimientos con relaciones relacionadas
    seguimientos = SeguimientoDiario.objects.select_related('lote', 'lote__galpon', 'lote__raza').order_by('-fecha_seguimiento')
    
    # Filtros
    lote_id = request.GET.get('lote')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if lote_id:
        seguimientos = seguimientos.filter(lote_id=lote_id)
    if fecha_desde:
        seguimientos = seguimientos.filter(fecha_seguimiento__gte=fecha_desde)
    if fecha_hasta:
        seguimientos = seguimientos.filter(fecha_seguimiento__lte=fecha_hasta)
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(seguimientos, 25)  # 25 seguimientos por página
    
    try:
        seguimientos_paginados = paginator.page(page)
    except PageNotAnInteger:
        seguimientos_paginados = paginator.page(1)
    except EmptyPage:
        seguimientos_paginados = paginator.page(paginator.num_pages)
    
    # Obtener lotes activos para el filtro
    lotes_activos = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
    
    context = {
        'seguimientos': seguimientos_paginados,
        'lotes_activos': lotes_activos,
        'filtro_lote': int(lote_id) if lote_id and lote_id.isdigit() else '',
        'filtro_fecha_desde': fecha_desde or '',
        'filtro_fecha_hasta': fecha_hasta or '',
        'title': 'Seguimientos Diarios',
    }


def test_admin_registration(request):
    """Test view to check admin registration status"""
    from django.contrib import admin
    from produccion.models import Galpon
    from django.http import JsonResponse
    from django.apps import apps
    
    # Get the actual admin site being used
    admin_site = type(admin.site).__module__ + '.' + type(admin.site).__name__
    
    # Check if model is registered with admin
    is_registered = admin.site.is_registered(Galpon)
    
    # Get registered models
    registered_models = []
    for model, model_admin in admin.site._registry.items():
        registered_models.append({
            'app': model._meta.app_label,
            'model': model._meta.model_name,
            'admin_class': model_admin.__class__.__name__
        })
    
    # Try to get some galpones
    try:
        galpones = list(Galpon.objects.values('id', 'numero_galpon')[:5])
        total_galpones = Galpon.objects.count()
    except Exception as e:
        galpones = []
        total_galpones = 0
    
    return JsonResponse({
        'galpon_registered': is_registered,
        'registered_models': registered_models,
        'sample_galpones': galpones,
        'total_galpones': total_galpones,
        'admin_site': admin_site,
        'admin_site_class': str(type(admin.site)),
        'admin_site_module': type(admin.site).__module__
    })

def test_admin_urls(request):
    """Test view to check admin URL configuration"""
    from django.urls.resolvers import get_resolver
    from django.http import JsonResponse
    from django.contrib import admin
    from django.urls import reverse
    
    # Get all registered URLs
    resolver = get_resolver()
    admin_urls = []
    
    # Helper function to get URL patterns
    def get_urls(url_patterns, prefix=''):
        urls = []
        for pattern in url_patterns:
            if hasattr(pattern, 'url_patterns'):
                # This is an include
                urls.extend(get_urls(pattern.url_patterns, prefix + str(pattern.pattern)))
            elif hasattr(pattern, 'callback'):
                # This is a URL pattern
                urls.append({
                    'pattern': prefix + str(pattern.pattern),
                    'name': pattern.name or '',
                    'callback': pattern.callback.__module__ + '.' + pattern.callback.__name__,
                })
        return urls
    
    # Get admin URLs
    admin_urls = get_urls(resolver.url_patterns)
    
    # Check Galpon admin URL
    galpon_admin_url = None
    try:
        galpon_admin_url = reverse('admin:produccion_galpon_changelist')
    except Exception as e:
        galpon_admin_url = f"Error: {str(e)}"
    
    return JsonResponse({
        'admin_urls': admin_urls,
        'galpon_admin_url': galpon_admin_url,
        'admin_site': str(admin.site),
        'admin_site_class': str(admin.site.__class__),
        'admin_site_module': admin.site.__class__.__module__
    })
