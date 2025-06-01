from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.db.models import Sum
from django.utils import timezone
import datetime

@receiver(pre_save, sender='produccion.ConsumoEnergia')
def set_consumo_energia_creator(sender, instance, **kwargs):
    """
    Signal to set the registrado_por field if not set
    """
    if not instance.pk and not instance.registrado_por:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            # Try to get the first superuser
            admin = User.objects.filter(is_superuser=True).first()
            if admin:
                instance.registrado_por = admin
        except:
            # If there's any error, just ignore it
            pass

@receiver([post_save, post_delete], sender='produccion.MortalidadDiaria')
def update_mortalidad_semanal(sender, instance, **kwargs):
    """
    Update or create a weekly mortality record when a daily mortality record is saved or deleted
    """
    # Get the week number and year from the mortality date
    week = instance.fecha.isocalendar()[1]
    year = instance.fecha.year
    
    # Get all daily mortality records for this lote in the same week
    daily_records = instance.lote.mortalidades_diarias.filter(
        fecha__year=year,
        fecha__week=week
    )
    
    # Calculate total deaths for the week
    total_muertes = daily_records.aggregate(total=Sum('cantidad_muertes'))['total'] or 0
    
    # Calculate mortality percentage (assuming we have the initial number of birds in the lote)
    if instance.lote.cantidad_inicial_aves > 0:  # Corregido el nombre del campo
        porcentaje_mortalidad = (total_muertes / instance.lote.cantidad_inicial_aves) * 100  # Corregido el nombre del campo
    else:
        porcentaje_mortalidad = 0
    
    # Get or create the weekly record
    MortalidadSemanal = apps.get_model('produccion', 'MortalidadSemanal')
    mortalidad_semanal, created = MortalidadSemanal.objects.update_or_create(
        lote=instance.lote,
        semana=week,
        anio=year,
        defaults={
            'total_muertes': total_muertes,
            'porcentaje_mortalidad': round(porcentaje_mortalidad, 2)
        }
    )
