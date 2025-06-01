# avicola/admin.py
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django import forms
from .models import UserProfile, Empresa

# Import Group and Permission here to avoid circular imports
from django.contrib.auth.models import Group, Permission

# Custom Admin Site
class CustomAdminSite(AdminSite):
    site_header = 'Administración de Granja Avícola'
    site_title = 'Sistema de Gestión Avícola'
    index_title = 'Panel de Control'
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        # Get the original app list
        app_dict = self._build_app_dict(request)
        app_list = list(app_dict.values())
        
        # Define the desired order of apps
        app_ordering = {
            'avicola': 1,
            'produccion': 2,
            'ventas': 3,
            'reportes': 4,
            'inventario': 5,
            'auth': 6,
        }
        
        # Sort the app list based on our custom ordering
        app_list.sort(key=lambda x: app_ordering.get(x['app_label'].lower(), 100))
        
        # Sort models within each app
        for app in app_list:
            if 'models' in app:
                # You can customize the order of models within each app here if needed
                # For example, to always have UserProfile first in the avicola app:
                if app['app_label'].lower() == 'avicola':
                    app['models'].sort(key=lambda x: 0 if x['object_name'] == 'UserProfile' else 1)
        
        return app_list

# Create an instance of our custom admin site
admin_site = CustomAdminSite(name='custom_admin')

# Set as the default admin site
admin.site = admin_site

class GroupSelectionForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Grupos"
    )

class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'mostrar_grupos', 'acciones')
    list_filter = ('user_type', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'telefono')}),
        ('Tipo de Usuario', {'fields': ('user_type',)}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'user_type', 'telefono'),
        }),
    )
    
    def mostrar_grupos(self, obj):
        """Muestra los grupos a los que pertenece el usuario"""
        return ", ".join([g.name for g in obj.groups.all()]) if obj.groups.exists() else "Sin grupos"
    mostrar_grupos.short_description = 'Grupos'
    
    def acciones(self, obj):
        """Añade botones de acción para cada usuario"""
        change_password_url = reverse('admin:cambiar_password_usuario', args=[obj.pk])
        manage_groups_url = reverse('admin:gestionar_grupos_usuario', args=[obj.pk])
        return format_html(
            '<a class="button" href="{}">Cambiar contraseña</a> '
            '<a class="button" href="{}">Gestionar Grupos</a>',
            change_password_url,
            manage_groups_url
        )
    acciones.short_description = 'Acciones'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/cambiar-password/',
                self.admin_site.admin_view(self.cambiar_password_view),
                name='cambiar_password_usuario',
            ),
            path(
                '<int:user_id>/gestionar-grupos/',
                self.admin_site.admin_view(self.gestionar_grupos_view),
                name='gestionar_grupos_usuario',
            ),
        ]
        return custom_urls + urls
    
    def cambiar_password_view(self, request, user_id):
        """Vista para que el administrador cambie la contraseña de un usuario"""
        user = get_object_or_404(UserProfile, pk=user_id)
        if request.method == 'POST':
            form = AdminPasswordChangeForm(user, request.POST)
            if form.is_valid():
                form.save()
                self.message_user(request, f'Contraseña cambiada exitosamente para {user.username}')
                return redirect('admin:avicola_userprofile_changelist')
        else:
            form = AdminPasswordChangeForm(user)
        
        # Preparar el contexto con todos los datos necesarios
        context = {
            'title': f'Cambiar contraseña: {user.username}',
            'form': form,
            'is_popup': False,
            'add': False,
            'change': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_view_permission': True,
            'has_editable_inline_admin_formsets': False,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'show_save_and_continue': False,
            'user_id': user_id,
            'username': user.username,
        }
        return render(request, 'admin/auth/user/change_password.html', context)
        
    def gestionar_grupos_view(self, request, user_id):
        """Vista para gestionar los grupos de un usuario"""
        user = get_object_or_404(UserProfile, pk=user_id)
        
        if request.method == 'POST':
            form = GroupSelectionForm(request.POST)
            if form.is_valid():
                # Obtener los grupos seleccionados
                selected_groups = form.cleaned_data['groups']
                
                # Actualizar los grupos del usuario
                user.groups.set(selected_groups)
                user.save()
                
                self.message_user(request, f'Grupos actualizados exitosamente para {user.username}')
                return redirect('admin:avicola_userprofile_changelist')
        else:
            # Inicializar el formulario con los grupos actuales del usuario
            form = GroupSelectionForm(initial={'groups': user.groups.all()})
        
        # Obtener todos los grupos disponibles
        all_groups = Group.objects.all().order_by('name')
        
        # Preparar información adicional sobre cada grupo
        groups_info = []
        for group in all_groups:
            # Contar usuarios en el grupo
            users_count = UserProfile.objects.filter(groups=group).count()
            # Contar permisos del grupo
            permissions_count = group.permissions.count()
            # Verificar si el usuario pertenece al grupo
            is_member = group in user.groups.all()
            
            groups_info.append({
                'id': group.id,
                'name': group.name,
                'users_count': users_count,
                'permissions_count': permissions_count,
                'is_member': is_member
            })
        
        # Preparar el contexto
        context = {
            'title': f'Gestionar grupos para: {user.username}',
            'form': form,
            'user': user,
            'groups_info': groups_info,
            'opts': self.model._meta,
            'original': user,
            'app_label': self.model._meta.app_label,
            'has_change_permission': True,
        }
        
        return render(request, 'admin/avicola/userprofile/gestionar_grupos.html', context)

# Register models with our custom admin site
admin_site.register(UserProfile, UserProfileAdmin)

# Register auth models
from .auth_admin import register_auth_models
register_auth_models(admin_site)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rif', 'direccion')
    search_fields = ('nombre', 'rif')

# Register Empresa with our custom admin site
admin_site.register(Empresa, EmpresaAdmin)

# Register Wiki models
try:
    from wiki.models import Category, Article, Attachment
    from wiki.admin import CategoryAdmin, ArticleAdmin, AttachmentAdmin
    admin_site.register(Category, CategoryAdmin)
    admin_site.register(Article, ArticleAdmin)
    admin_site.register(Attachment, AttachmentAdmin)
    print("Registered Wiki admin")
except Exception as e:
    print(f"Error registering Wiki admin: {e}")

# Register FAQ models
try:
    from faq.models import FAQCategory, FAQ
    from faq.admin import FAQCategoryAdmin, FAQAdmin
    admin_site.register(FAQCategory, FAQCategoryAdmin)
    admin_site.register(FAQ, FAQAdmin)
    print("Registered FAQ admin")
except Exception as e:
    print(f"Error registering FAQ admin: {e}")

# Register Bot models
try:
    from bot.models import BotIntent, BotConversation, BotMessage
    from bot.admin import BotIntentAdmin, BotConversationAdmin, BotMessageAdmin
    admin_site.register(BotIntent, BotIntentAdmin)
    admin_site.register(BotConversation, BotConversationAdmin)
    admin_site.register(BotMessage, BotMessageAdmin)
    print("Registered Bot admin")
except Exception as e:
    print(f"Error registering Bot admin: {e}")

# Register Respaldos models
try:
    from respaldos.models import Backup, BackupConfiguration, RestoreLog
    from respaldos.admin import BackupAdmin, BackupConfigurationAdmin, RestoreLogAdmin
    admin_site.register(Backup, BackupAdmin)
    admin_site.register(BackupConfiguration, BackupConfigurationAdmin)
    admin_site.register(RestoreLog, RestoreLogAdmin)
    print("Registered Respaldos admin")
except Exception as e:
    print(f"Error registering Respaldos admin: {e}")

# Register Django Summernote
try:
    from django_summernote.models import Attachment as SummernoteAttachment
    from django_summernote.admin import SummernoteModelAdmin
    admin_site.register(SummernoteAttachment)
    print("Registered Django Summernote admin")
except Exception as e:
    print(f"Error registering Django Summernote admin: {e}")