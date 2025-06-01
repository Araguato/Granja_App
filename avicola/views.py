from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.translation import get_language, activate, gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.contrib import messages, auth
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth import logout as auth_logout
from django.db.models import Sum, Avg, Count, F, Q
from datetime import datetime, timedelta
from django.utils import timezone
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria
from django.urls import reverse, reverse_lazy

def custom_login(request, *args, **kwargs):
    """
    Custom login view that handles authentication and redirection based on user role.
    """
    # If user is already authenticated, redirect to appropriate dashboard
    if request.user.is_authenticated:
        return redirect(redirect_to_dashboard(request.user))
    
    from django.contrib.auth.forms import AuthenticationForm
    
    # Initialize form with request.POST if it's a POST request, otherwise None
    form = AuthenticationForm(request, data=request.POST or None)
    next_url = request.GET.get('next', '')
    
    if request.method == 'POST':
        if form.is_valid():
            from django.contrib.auth import login
            
            # Get the user from the form
            user = form.get_user()
            
            # Log the user in
            login(request, user)
            
            # Get the next URL if provided
            next_url = request.POST.get('next', '')
            
            # Redirect to 'next' URL if it's provided and safe
            if next_url and is_safe_url(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
                
            # Otherwise, redirect based on user role
            return redirect(redirect_to_dashboard(user))
        else:
            # Form is invalid, show error messages
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
    
    # For GET requests or failed login attempts, show the login form
    context = {
        'form': form,
        'next': next_url,
        'title': 'Iniciar Sesión'
    }
    return render(request, 'registration/login.html', context)

def redirect_to_dashboard(user):
    """
    Helper function to redirect users to their appropriate dashboard.
    Returns the URL name to redirect to, not a response object.
    """
    if user.is_superuser or (hasattr(user, 'groups') and 
            user.groups.filter(name__in=['Supervisores', 'Administradores']).exists()):
        return 'core:dashboard_supervisor'
    elif hasattr(user, 'groups') and user.groups.filter(name='Operarios').exists():
        return 'core:dashboard_operario'
    return 'core:home'

def is_safe_url(url, allowed_hosts):
    """
    Return `True` if the url is a safe redirection (i.e. it doesn't point to
    a different host).
    """
    from django.utils.http import url_has_allowed_host_and_scheme
    return url_has_allowed_host_and_scheme(url=url, allowed_hosts=allowed_hosts)


class CustomLogoutView(BaseLogoutView):
    """
    Custom logout view that handles the logout process and redirects to the login page.
    """
    next_page = reverse_lazy('avicola:login')
    
    def dispatch(self, request, *args, **kwargs):
        # Add a success message before logging out
        messages.success(request, 'Has cerrado sesión correctamente.')
        return super().dispatch(request, *args, **kwargs)


def logout_view(request):
    """
    Logout view that handles the logout process and redirects to the login page.
    This function ensures proper session cleanup and displays a success message.
    """
    # Add a success message before logging out
    messages.success(request, 'Has cerrado sesión correctamente.')
    
    # Clear session data
    if hasattr(request, 'session'):
        request.session.flush()
    
    # Log the user out
    auth_logout(request)
    
    # Redirect to login page with next parameter if provided
    next_page = request.GET.get('next', None)
    if next_page:
        return redirect(f"{reverse('avicola:login')}?next={next_page}")
    return redirect('avicola:login')


@login_required
def pagina_principal(request):
    # Verificar si el usuario es operario y redirigir al dashboard de operario
    if request.user.groups.filter(name='Operarios').exists():
        return redirect('avicola:dashboard_operario')
    return render(request, 'principal.html')

@login_required
def reportes(request):
    return render(request, 'reportes.html')

@login_required
def dashboard_operario(request):
    """Dashboard específico para operarios"""
    # Verificar si el usuario es operario
    if not request.user.groups.filter(name='Operarios').exists() and not request.user.is_superuser:
        return redirect('core:home')
    
    from produccion.models import Galpon, Lote, SeguimientoDiario
    from django.db.models import Count, Q, Sum, F
    from django.utils import timezone
    from datetime import timedelta
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener galpones con información de lotes activos
    galpones = Galpon.objects.annotate(
        lotes_activos=Count('lotes', filter=Q(lotes__estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']), distinct=True)
    ).select_related('granja')
    
    # Obtener lotes activos
    lotes_activos = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
    
    # Obtener seguimientos recientes (últimos 5 días)
    fecha_limite = hoy - timedelta(days=5)
    ultimos_seguimientos = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite
    ).select_related('lote', 'lote__galpon').order_by('-fecha_seguimiento')[:10]
    
    # Calcular estadísticas de producción de hoy
    produccion_hoy = SeguimientoDiario.objects.filter(
        fecha_seguimiento=hoy
    ).aggregate(
        total_huevos=Sum('huevos_totales'),
        total_mortalidad=Sum('mortalidad')
    )
    
    # Obtener estadísticas de energía (ejemplo con datos reales si existen)
    estadisticas_energia = {
        'consumo_diario': 120.5,
        'consumo_mensual': 2500.75,
        'costo_estimado': 1850.30
    }
    
    context = {
        'title': 'Dashboard Operativo',
        'user': request.user,
        'galpones': galpones,
        'lotes_activos': lotes_activos,
        'galpones_activos': galpones.count(),
        'total_huevos_hoy': produccion_hoy['total_huevos'] or 0,
        'mortalidad_hoy': produccion_hoy['total_mortalidad'] or 0,
        'estadisticas_energia': estadisticas_energia,
        'ultimos_seguimientos': ultimos_seguimientos,
        'es_admin': request.user.is_superuser or request.user.groups.filter(name='Administradores').exists(),
        'hoy': hoy,
    }
    
    # Añadir mensaje de depuración
    print(f"[DEBUG] Dashboard - Galpones: {galpones.count()}, Lotes: {lotes_activos.count()}, Seguimientos: {ultimos_seguimientos.count()}")
    
    return render(request, 'avicola/dashboard_supervisor.html', context)

def set_language(request, lang_code):
    """Establece el idioma seleccionado y redirecciona a la página anterior"""
    # Verificar que el idioma esté en los idiomas disponibles
    if lang_code not in [code for code, name in settings.LANGUAGES]:
        lang_code = settings.LANGUAGE_CODE
    
    # Establecer idioma en la sesión
    request.session['language'] = lang_code
    
    # Activar idioma
    translation.activate(lang_code)
    
    # Obtener URL de redirección
    next_url = request.GET.get('next', '/')
    
    # Redireccionar a la página anterior
    return redirect(next_url)

from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from produccion.models import Lote, Galpon, SeguimientoDiario
from django.shortcuts import get_object_or_404

@login_required
def listar_lotes(request):
    """Lista todos los lotes activos"""
    # Check if user is in Supervisores group or is superuser
    if not request.user.groups.filter(name='Supervisores').exists() and not request.user.is_superuser:
        return redirect('avicola:dashboard')
        
    lotes = Lote.objects.filter(estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION'])
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(lotes, 10)  # 10 lotes por página
    
    try:
        lotes_paginados = paginator.page(page)
    except PageNotAnInteger:
        lotes_paginados = paginator.page(1)
    except EmptyPage:
        lotes_paginados = paginator.page(paginator.num_pages)
    
    context = {
        'lotes': lotes_paginados,
        'title': 'Lotes Activos',
    }
    return render(request, 'avicola/lotes/listar.html', context)

@login_required
def listar_galpones(request):
    """Lista todos los galpones"""
    galpones = Galpon.objects.select_related('granja').all()
    
    # Paginación
    page = request.GET.get('page', 1)
    paginator = Paginator(galpones, 10)  # 10 galpones por página
    
    try:
        galpones_paginados = paginator.page(page)
    except PageNotAnInteger:
        galpones_paginados = paginator.page(1)
    except EmptyPage:
        galpones_paginados = paginator.page(paginator.num_pages)
    
    context = {
        'galpones': galpones_paginados,
        'title': 'Galpones',
    }
    return render(request, 'avicola/galpones/listar.html', context)

@login_required
def seguimientos_recientes(request):
    """Muestra los seguimientos recientes"""
    from datetime import timedelta
    from django.utils import timezone
    
    hoy = timezone.now().date()
    fecha_limite = hoy - timedelta(days=7)  # Últimos 7 días
    
    seguimientos = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite
    ).select_related('lote', 'lote__galpon').order_by('-fecha_seguimiento')
    
    context = {
        'seguimientos': seguimientos,
        'title': 'Seguimientos Recientes',
    }
    return render(request, 'avicola/seguimientos/recientes.html', context)

@login_required
@permission_required('avicola.es_supervisor', raise_exception=True)
def dashboard_supervisor(request):
    """Dashboard específico para supervisores"""
    from produccion.models import Galpon, Lote, SeguimientoDiario
    from django.db.models import Count, Q, Sum, F, Avg
    from django.utils import timezone
    from datetime import timedelta
    
    # Fechas para cálculos
    hoy = timezone.now().date()
    inicio_mes = hoy.replace(day=1)
    
    # Obtener estadísticas generales
    total_galpones = Galpon.objects.count()
    # Contar galpones con lotes activos (INICIAL, CRECIMIENTO o PRODUCCION)
    galpones_activos = Galpon.objects.filter(
        lotes__estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
    ).distinct().count()
    
    # Obtener lotes por estado
    lotes_por_estado = Lote.objects.values('estado').annotate(
        total=Count('id')
    ).order_by('estado')
    
    # Obtener lotes activos con información relacionada
    lotes_activos = Lote.objects.filter(
        estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
    ).select_related('galpon', 'raza').order_by('galpon__numero_galpon', 'fecha_ingreso')[:10]  # Limit to 10 items for the dashboard
    
    # Obtener estadísticas de producción del mes actual
    produccion_mes = SeguimientoDiario.objects.filter(
        fecha_seguimiento__year=inicio_mes.year,
        fecha_seguimiento__month=inicio_mes.month
    ).aggregate(
        total_huevos=Sum('huevos_totales'),
        promedio_ponedoras=Avg('huevos_totales')
    )
    
    # Obtener seguimientos recientes (últimos 7 días)
    fecha_limite = hoy - timedelta(days=7)
    ultimos_seguimientos = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite
    ).select_related('lote', 'lote__galpon').order_by('-fecha_seguimiento')[:15]
    
    # Calcular porcentaje de mortalidad promedio
    mortalidad_promedio = SeguimientoDiario.objects.filter(
        fecha_seguimiento__gte=fecha_limite
    ).aggregate(
        promedio_mortalidad=Avg(
            F('mortalidad') * 100.0 / F('lote__cantidad_inicial_aves'),
            output_field=models.FloatField()
        )
    )['promedio_mortalidad'] or 0
    
    context = {
        'title': 'Panel de Supervisor',
        'user': request.user,
        'total_galpones': total_galpones,
        'galpones_activos': galpones_activos,
        'lotes_por_estado': lotes_por_estado,
        'total_huevos_mes': produccion_mes['total_huevos'] or 0,
        'promedio_ponedoras': round(produccion_mes['promedio_ponedoras'] or 0, 2),
        'mortalidad_promedio': round(mortalidad_promedio, 2) if mortalidad_promedio else 0,
        'ultimos_seguimientos': ultimos_seguimientos,
        'lotes_activos': lotes_activos,
        'hoy': hoy,
    }
    
    return render(request, 'avicola/dashboard_operario.html', context)

@login_required
def detalle_lote(request, lote_id):
    """Muestra el detalle de un lote específico"""
    lote = get_object_or_404(Lote.objects.select_related('galpon', 'raza'), id=lote_id)
    
    # Obtener los últimos 10 seguimientos del lote
    seguimientos = SeguimientoDiario.objects.filter(lote=lote).order_by('-fecha_seguimiento')[:10]
    
    context = {
        'lote': lote,
        'seguimientos': seguimientos,
        'title': f'Lote {lote.codigo_lote or lote.id}'
    }
    return render(request, 'avicola/lotes/detalle.html', context)

@login_required
def perfil(request):
    """Vista para ver y editar el perfil del usuario"""
    if request.method == 'POST':
        # Aquí iría la lógica para actualizar el perfil
        pass
    return render(request, 'avicola/perfil.html', {'user': request.user})

@require_http_methods(["POST"])
@login_required
def set_language_ajax(request):
    """Establece el idioma seleccionado vía AJAX"""
    if request.is_ajax():
        lang_code = request.POST.get('language', settings.LANGUAGE_CODE)
        if lang_code in [lang[0] for lang in settings.LANGUAGES]:
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response = JsonResponse({'status': 'error', 'message': 'Sessions not enabled'})
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
                return response
            
            translation.activate(lang_code)
            response = JsonResponse({'status': 'success', 'message': 'Idioma cambiado correctamente'})
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            return response
    
    return JsonResponse({'status': 'error', 'message': 'Solicitud inválida'}, status=400)

@login_required
def estadisticas_view(request):
    """Vista para mostrar estadísticas de la granja"""
    # Obtener fechas para filtros
    today = timezone.now().date()
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Estadísticas generales
    total_granjas = Granja.objects.count()
    total_galpones = Galpon.objects.count()
    total_lotes = Lote.objects.count()
    
    # Lotes activos (basado en el campo 'estado')
    lotes_activos_qs = Lote.objects.filter(
        estado__in=['INICIAL', 'CRECIMIENTO', 'PRODUCCION']
    ).select_related('galpon', 'raza').order_by('galpon__numero_galpon', 'fecha_ingreso')
    
    lotes_activos_count = lotes_activos_qs.count()
    
    # Obtener datos para gráficos
    # 1. Producción semanal de huevos (últimas 4 semanas)
    semanas = []
    produccion_semanal = []
    
    for i in range(4, 0, -1):
        fecha_inicio = today - timedelta(weeks=i)
        fecha_fin = fecha_inicio + timedelta(weeks=1)
        semana_label = f"{fecha_inicio.day}/{fecha_inicio.month}-{fecha_fin.day}/{fecha_fin.month}"
        
        produccion = SeguimientoDiario.objects.filter(
            fecha_seguimiento__range=[fecha_inicio, fecha_fin],
            tipo_seguimiento__in=['PRODUCCION', 'MIXTO']
        ).aggregate(total=Sum('huevos_totales'))['total'] or 0
        
        semanas.append(semana_label)
        produccion_semanal.append(produccion)
    
    # 2. Mortalidad por galpón (últimos 30 días)
    mortalidad_por_galpon = Galpon.objects.annotate(
        total_mortalidad=Sum(
            'lotes__mortalidades_diarias__cantidad_muertes',
            filter=Q(lotes__mortalidades_diarias__fecha__gte=last_month)
        )
    ).filter(total_mortalidad__gt=0).values('numero_galpon', 'total_mortalidad')
    
    galpones = [f"Galpón {g['numero_galpon']}" for g in mortalidad_por_galpon]
    mortalidades = [g['total_mortalidad'] for g in mortalidad_por_galpon]
    
    # 3. Consumo de alimento por lote (últimos 7 días)
    consumo_alimento = Lote.objects.annotate(
        total_consumo=Sum(
            'seguimientos_diarios__consumo_alimento_kg',
            filter=Q(seguimientos_diarios__fecha_seguimiento__gte=last_week)
        )
    ).filter(total_consumo__gt=0).values('codigo_lote', 'total_consumo')
    
    lotes = [f"Lote {c['codigo_lote']}" for c in consumo_alimento]
    consumos = [float(c['total_consumo']) for c in consumo_alimento]
    
    context = {
        'title': 'Estadísticas',
        'user': request.user,
        'total_granjas': total_granjas,
        'total_galpones': total_galpones,
        'total_lotes': total_lotes,
        'lotes_activos': lotes_activos_count,
        'lotes_activos_list': lotes_activos_qs[:10],  # Mostrar solo los 10 primeros
        'semanas': semanas,
        'produccion_semanal': produccion_semanal,
        'galpones': galpones,
        'mortalidades': mortalidades,
        'lotes': lotes,
        'consumos': consumos,
    }
    
    return render(request, 'avicola/estadisticas.html', context)

def recomendaciones_view(request):
    """Vista para mostrar recomendaciones para la granja"""
    context = {
        'title': 'Recomendaciones',
        'user': request.user,
    }
    return render(request, 'avicola/recomendaciones.html', context)


def configuracion(request):
    """Vista para la página de configuración"""
    context = {
        'title': 'Configuración',
        'user': request.user,
    }
    return render(request, 'avicola/configuracion.html', context)
