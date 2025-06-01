from rest_framework import serializers
from produccion.models import Lote, Galpon, SeguimientoDiario, Granja

class GranjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Granja
        fields = ['id', 'nombre', 'direccion', 'telefono', 'email']

class GalponSerializer(serializers.ModelSerializer):
    granja_nombre = serializers.ReadOnlyField(source='granja.nombre')
    
    class Meta:
        model = Galpon
        fields = ['id', 'codigo', 'capacidad', 'estado', 'granja', 'granja_nombre', 'fecha_creacion']

class LoteSerializer(serializers.ModelSerializer):
    galpon_nombre = serializers.ReadOnlyField(source='galpon.codigo')
    raza_nombre = serializers.ReadOnlyField(source='raza.nombre')
    
    class Meta:
        model = Lote
        fields = [
            'id', 'codigo', 'fecha_inicio', 'cantidad_inicial_aves', 'estado',
            'galpon', 'galpon_nombre', 'raza', 'raza_nombre', 'observaciones',
            'fecha_creacion', 'fecha_actualizacion'
        ]

class SeguimientoDiarioSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.ReadOnlyField(source='lote.codigo')
    
    class Meta:
        model = SeguimientoDiario
        fields = [
            'id', 'lote', 'lote_codigo', 'fecha_seguimiento', 'huevos_producidos',
            'aves_muertas', 'consumo_alimento', 'peso_promedio', 'observaciones',
            'fecha_creacion'
        ]
