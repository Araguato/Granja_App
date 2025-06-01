from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.http import HttpResponse, Http404
import os

class TestStaticFilesView(LoginRequiredMixin, View):
    """Test view to verify static files are loading correctly."""
    template_name = 'core/test_static_files.html'
    
    def get(self, request, *args, **kwargs):
        # Check if admin static files exist in different locations
        admin_paths = [
            ('STATIC_ROOT/admin', os.path.join(settings.STATIC_ROOT, 'admin')),
            ('STATICFILES_DIRS', [os.path.join(d, 'admin') for d in settings.STATICFILES_DIRS]),
            ('Python site-packages', os.path.join(os.path.dirname(settings.BASE_DIR), 'Lib', 'site-packages', 'django', 'contrib', 'admin', 'static', 'admin'))
        ]
        
        # Check each path
        admin_files = {}
        for name, path in admin_paths:
            if isinstance(path, list):
                for p in path:
                    if os.path.exists(p):
                        admin_files[name] = p
                        break
            elif os.path.exists(path):
                admin_files[name] = path
        
        # Check specific files
        files_to_check = [
            ('admin/css/base.css', 'CSS base file'),
            ('admin/js/admin/RelatedObjectLookups.js', 'Admin JS file'),
            ('admin/js/vendor/jquery/jquery.min.js', 'jQuery file')
        ]
        
        file_checks = []
        for file_path, description in files_to_check:
            found_in = []
            for name, base_path in admin_files.items():
                full_path = os.path.join(base_path, file_path)
                if os.path.exists(full_path):
                    found_in.append(f'{name}: {full_path}')
            file_checks.append({
                'path': file_path,
                'description': description,
                'found_in': found_in
            })
        
        context = {
            'title': 'Prueba de Archivos Estáticos',
            'message': 'Esta es una página de prueba para verificar que los archivos estáticos se carguen correctamente.',
            'debug': settings.DEBUG,
            'static_url': settings.STATIC_URL,
            'static_root': settings.STATIC_ROOT,
            'static_dirs': getattr(settings, 'STATICFILES_DIRS', []),
            'media_url': settings.MEDIA_URL,
            'media_root': settings.MEDIA_ROOT,
            'admin_paths': admin_files,
            'file_checks': file_checks,
            'installed_apps': settings.INSTALLED_APPS,
            'middleware': settings.MIDDLEWARE,
        }
        return render(request, self.template_name, context)

class TestAdminView(UserPassesTestMixin, View):
    """Test view to check admin access and static files."""
    template_name = 'core/test_admin.html'
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'title': 'Prueba de Acceso al Admin',
            'user': request.user,
            'is_staff': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        })
