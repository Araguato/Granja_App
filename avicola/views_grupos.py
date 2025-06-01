from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from produccion.models import Lote, Galpon, SeguimientoDiario
from inventario.models import Vacuna, Alimento, Raza
from avicola.models import Empresa, UserProfile

def is_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_superuser or user.user_type == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def verificar_permisos_grupo(request, grupo_nombre="Supervisores"):
    """
    Vista para verificar y configurar los permisos de un grupo específico.
    Por defecto, verifica el grupo 'Supervisores'.
    Solo accesible para administradores.
    """
    # Intentar obtener el grupo
    try:
        grupo = Group.objects.get(name=grupo_nombre)
    except Group.DoesNotExist:
        # Si el grupo no existe, crearlo
        grupo = Group.objects.create(name=grupo_nombre)
        messages.success(request, f"Se ha creado el grupo '{grupo_nombre}'.")    
    # Obtener los permisos actuales del grupo
    permisos_actuales = grupo.permissions.all()
    
    # Definir los modelos y sus permisos
    modelos_info = [
        {'modelo': Lote, 'nombre': 'Lote', 'app': 'produccion'},
        {'modelo': Galpon, 'nombre': 'Galpón', 'app': 'produccion'},
        {'modelo': SeguimientoDiario, 'nombre': 'Seguimiento Diario', 'app': 'produccion'},
        {'modelo': Vacuna, 'nombre': 'Vacuna', 'app': 'inventario'},
        {'modelo': Alimento, 'nombre': 'Alimento', 'app': 'inventario'},
        {'modelo': Raza, 'nombre': 'Raza', 'app': 'inventario'},
        {'modelo': Empresa, 'nombre': 'Empresa', 'app': 'avicola'},
    ]
    
    # Preparar la estructura de permisos para la plantilla
    permisos_por_modelo = []
    for modelo_info in modelos_info:
        modelo = modelo_info['modelo']
        content_type = ContentType.objects.get_for_model(modelo)
        
        # Obtener todos los permisos disponibles para este modelo
        permisos = Permission.objects.filter(content_type=content_type)
        
        # Organizar los permisos por tipo (ver, añadir, cambiar, eliminar)
        permisos_organizados = {
            'ver': next((p for p in permisos if p.codename.startswith('view_')), None),
            'anadir': next((p for p in permisos if p.codename.startswith('add_')), None),
            'cambiar': next((p for p in permisos if p.codename.startswith('change_')), None),
            'eliminar': next((p for p in permisos if p.codename.startswith('delete_')), None),
        }
        
        # Verificar cuáles permisos ya están asignados al grupo
        permisos_asignados = {
            tipo: (permiso in permisos_actuales) if permiso else False
            for tipo, permiso in permisos_organizados.items()
        }
        
        # Añadir a la lista de permisos por modelo
        permisos_por_modelo.append({
            'nombre': modelo_info['nombre'],
            'app': modelo_info['app'],
            'permisos': permisos_organizados,
            'asignados': permisos_asignados,
        })
    
    if request.method == 'POST':
        # Obtener los permisos seleccionados del formulario
        permisos_seleccionados = request.POST.getlist('permisos')
        
        # Primero, eliminar todos los permisos actuales del grupo
        grupo.permissions.clear()
        
        # Luego, añadir los permisos seleccionados
        for perm_id in permisos_seleccionados:
            try:
                permiso = Permission.objects.get(id=perm_id)
                grupo.permissions.add(permiso)
            except Permission.DoesNotExist:
                pass
        
        # Si el grupo es 'Supervisores', asegurarse de que tengan los permisos necesarios para el admin
        if grupo_nombre.lower() == 'supervisores':
            # Asegurarse de que los supervisores tengan is_staff=True
            supervisores = UserProfile.objects.filter(groups=grupo)
            for supervisor in supervisores:
                if not supervisor.is_staff:
                    supervisor.is_staff = True
                    supervisor.save()
            
            # Asegurarse de que tengan permisos para acceder a Ventas y Mortalidad
            modelos_admin = [
                # Ventas
                {'app': 'ventas', 'modelo': 'venta'},
                {'app': 'ventas', 'modelo': 'cliente'},
                {'app': 'ventas', 'modelo': 'tipohuevo'},
                {'app': 'ventas', 'modelo': 'inventariohuevos'},
                # Producción (para mortalidad)
                {'app': 'produccion', 'modelo': 'seguimientodiario'},
            ]
            
            # Permisos que queremos asignar para cada modelo
            tipos_permisos = ['view', 'add', 'change', 'delete']
            
            # Obtener y asignar todos los permisos necesarios
            permisos_admin_asignados = 0
            for modelo_info in modelos_admin:
                app = modelo_info['app']
                modelo = modelo_info['modelo']
                
                try:
                    content_type = ContentType.objects.get(app_label=app, model=modelo)
                    
                    for tipo in tipos_permisos:
                        codename = f"{tipo}_{modelo}"
                        try:
                            permiso = Permission.objects.get(content_type=content_type, codename=codename)
                            if permiso not in grupo.permissions.all():
                                grupo.permissions.add(permiso)
                                permisos_admin_asignados += 1
                        except Permission.DoesNotExist:
                            pass
                
                except ContentType.DoesNotExist:
                    pass
            
            if permisos_admin_asignados > 0:
                messages.info(request, f"Se han asignado {permisos_admin_asignados} permisos adicionales para acceso a Ventas y Mortalidad.")
        
        messages.success(request, f"Se han actualizado los permisos del grupo '{grupo_nombre}'.")
        
        # Actualizar los permisos de los usuarios en el grupo
        usuarios_grupo = UserProfile.objects.filter(groups=grupo)
        for usuario in usuarios_grupo:
            # Refrescar los permisos del usuario
            usuario.save()        
        
        # Redirigir a la misma página para mostrar los cambios
        return redirect('verificar_permisos_grupo', grupo_nombre=grupo_nombre)
    
    # Preparar el contexto para la plantilla
    context = {
        'title': f'Gestionar Permisos del Grupo: {grupo_nombre}',
        'grupo': grupo,
        'permisos_actuales': permisos_actuales,
        'permisos_por_modelo': permisos_por_modelo,
    }
    
    return render(request, 'avicola/verificar_permisos_grupo.html', context)


@login_required
@user_passes_test(is_admin)
def usuarios_grupo(request, grupo_nombre="Supervisores"):
    """
    Vista para mostrar y gestionar los usuarios que pertenecen a un grupo específico.
    Por defecto, muestra el grupo 'Supervisores'.
    Solo accesible para administradores.
    """
    # Intentar obtener el grupo
    try:
        grupo = Group.objects.get(name=grupo_nombre)
    except Group.DoesNotExist:
        # Si el grupo no existe, crearlo
        grupo = Group.objects.create(name=grupo_nombre)
        messages.success(request, f"Se ha creado el grupo '{grupo_nombre}'.")
    
    # Obtener los usuarios que pertenecen al grupo
    usuarios = UserProfile.objects.filter(groups=grupo).order_by('first_name', 'last_name')
    
    # Obtener los usuarios que no pertenecen al grupo
    usuarios_disponibles = UserProfile.objects.exclude(groups=grupo).order_by('first_name', 'last_name')
    
    # Preparar el contexto para la plantilla
    context = {
        'title': f'Usuarios del Grupo: {grupo_nombre}',
        'grupo': grupo,
        'usuarios': usuarios,
        'usuarios_disponibles': usuarios_disponibles,
    }
    
    return render(request, 'avicola/usuarios_grupo.html', context)


@login_required
@user_passes_test(is_admin)
def agregar_usuario_grupo(request, grupo_nombre):
    """
    Vista para agregar un usuario a un grupo específico.
    Solo accesible para administradores.
    """
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        
        try:
            grupo = Group.objects.get(name=grupo_nombre)
            usuario = UserProfile.objects.get(id=usuario_id)
            
            # Agregar el usuario al grupo
            usuario.groups.add(grupo)
            
            # Si el grupo es 'Supervisores', actualizar el tipo de usuario
            if grupo_nombre.lower() == 'supervisores' and usuario.user_type != 'ADMIN':
                usuario.user_type = 'SUPERVISOR'
                usuario.save()
            
            messages.success(request, f"Se ha agregado a {usuario.get_full_name()} al grupo '{grupo_nombre}'.")
        except (Group.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "No se pudo agregar el usuario al grupo. Verifique los datos.")
    
    return redirect('usuarios_grupo', grupo_nombre=grupo_nombre)


@login_required
@user_passes_test(is_admin)
def quitar_usuario_grupo(request, grupo_nombre, usuario_id):
    """
    Vista para quitar un usuario de un grupo específico.
    Solo accesible para administradores.
    """
    if request.method == 'POST':
        try:
            grupo = Group.objects.get(name=grupo_nombre)
            usuario = UserProfile.objects.get(id=usuario_id)
            
            # Quitar el usuario del grupo
            usuario.groups.remove(grupo)
            
            messages.success(request, f"Se ha quitado a {usuario.get_full_name()} del grupo '{grupo_nombre}'.")
        except (Group.DoesNotExist, UserProfile.DoesNotExist):
            messages.error(request, "No se pudo quitar el usuario del grupo. Verifique los datos.")
    
    return redirect('usuarios_grupo', grupo_nombre=grupo_nombre)
