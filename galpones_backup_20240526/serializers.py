from rest_framework import serializers
from .models import Galpon

class GalponSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Galpon"""
    
    # Campos de solo lectura para mostrar información relacionada
    granja_nombre = serializers.CharField(source='granja.nombre', read_only=True)
    responsable_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Galpon
        fields = [
            'id', 'numero', 'nombre', 'capacidad', 'tipo', 'estado',
            'ubicacion', 'fecha_creacion', 'fecha_actualizacion',
            'observaciones', 'granja', 'granja_nombre', 'responsable',
            'responsable_nombre'
        ]
        read_only_fields = ('fecha_creacion', 'fecha_actualizacion')
    
    def get_responsable_nombre(self, obj):
        """Obtiene el nombre completo del responsable"""
        if obj.responsable:
            return f"{obj.responsable.first_name} {obj.responsable.last_name}".strip()
        return None
    
    def validate_numero(self, value):
        """Valida que el número de galpón sea único"""
        queryset = Galpon.objects.filter(numero=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Ya existe un galpón con este número.")
        return value
