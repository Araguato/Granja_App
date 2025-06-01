from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator, MaxValueValidator # No se usan aquí directamente aún
# from django.core.exceptions import ValidationError # No se usan aquí directamente aún
# from django.utils import timezone # No se usan aquí directamente aún

class Empresa(models.Model):
    rif = models.CharField(max_length=20, unique=True, verbose_name="RIF")
    nombre = models.CharField(max_length=100, verbose_name="Nombre Legal")
    direccion = models.TextField(verbose_name="Dirección Fiscal")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    encargado = models.CharField(max_length=100, verbose_name="Representante")
    pais = models.CharField(max_length=50, default="Venezuela")
    moneda = models.CharField(max_length=10, default="USD", verbose_name="Moneda Base")

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nombre']
        permissions = [("view_dashboard", "Puede ver el dashboard empresarial")]

    def __str__(self):
        return f"{self.rif} | {self.nombre}"

class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('SUPERVISOR', 'Supervisor'),
        ('VETERINARIO', 'Veterinario'),
        ('OPERARIO', 'Operario'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='OPERARIO', verbose_name="Tipo de Usuario")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    # Removed granja_asignada to avoid circular dependencies
    
    # Explicitly define groups and user_permissions to ensure they appear in admin
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="userprofile_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="userprofile_set",
        related_query_name="user",
    )

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        # Considera añadir ordering si es relevante, ej: ordering = ['username']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"