"""
This module handles the registration of admin classes to avoid circular imports.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from avicola.custom_admin import custom_admin_site as admin_site

def register_models():
    """
    Register all models with their respective admin classes in the correct order
    to handle dependencies properly.
    """
    # Import models and admin classes inside the function to avoid circular imports
    from .models import (
        Granja, Galpon, Lote, SeguimientoDiario, 
        MortalidadDiaria, MortalidadSemanal, SeguimientoEngorde, ConsumoEnergia
    )
    
    from .admin import (
        GranjaAdmin, GalponAdmin, LoteAdmin, SeguimientoDiarioAdmin,
        SeguimientoEngordeAdmin, MortalidadDiariaAdmin, MortalidadSemanalAdmin,
        ConsumoEnergiaAdmin
    )
    
    # Register models in dependency order
    _safe_register(Granja, GranjaAdmin)  # No dependencies
    _safe_register(Galpon, GalponAdmin)  # Depends on Granja
    _safe_register(Lote, LoteAdmin)  # Depends on Galpon
    
    # Register remaining models
    _safe_register(SeguimientoDiario, SeguimientoDiarioAdmin)  # Depends on Lote
    _safe_register(SeguimientoEngorde, SeguimientoEngordeAdmin)  # Depends on SeguimientoDiario
    _safe_register(MortalidadDiaria, MortalidadDiariaAdmin)  # Depends on Lote
    _safe_register(MortalidadSemanal, MortalidadSemanalAdmin)  # Depends on Lote
    _safe_register(ConsumoEnergia, ConsumoEnergiaAdmin)  # Depends on Galpon
    
    # Handle User model registration
    _register_user_model()

def _register_user_model():
    """Register the User model with a custom admin class."""
    from django.contrib.auth import get_user_model
    from django.contrib import admin
    from django.contrib.admin.sites import AlreadyRegistered
    
    User = get_user_model()
    
    # Unregister if already registered
    if User in admin_site._registry:
        admin_site.unregister(User)
    
    class UserAdmin(admin.ModelAdmin):
        search_fields = ('username', 'first_name', 'last_name', 'email')
        list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
        list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    # Register with our custom admin site
    try:
        admin_site.register(User, UserAdmin)
    except AlreadyRegistered:
        pass
    
    # Also register with default admin site for fallback
    from django.contrib import admin as default_admin
    if User in default_admin.site._registry:
        default_admin.site.unregister(User)
    default_admin.site.register(User, UserAdmin)

def _safe_register(model, admin_class):
    """Safely register a model with its admin class if not already registered."""
    from django.contrib.admin.sites import AlreadyRegistered
    try:
        admin_site.register(model, admin_class)
    except AlreadyRegistered:
        # Skip if the model is already registered
        pass
