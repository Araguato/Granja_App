from rest_framework import serializers
from inventario.models import Proveedor, Raza, Alimento, Vacuna, Insumo, GuiaDesempenoRaza

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = '__all__'


class AlimentoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre', default='')
    
    class Meta:
        model = Alimento
        fields = '__all__'


class VacunaSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre', default='')
    
    class Meta:
        model = Vacuna
        fields = '__all__'


class InsumoSerializer(serializers.ModelSerializer):
    proveedor_nombre = serializers.ReadOnlyField(source='proveedor.nombre', default='')
    tipo_insumo_display = serializers.ReadOnlyField(source='get_tipo_insumo_display')
    
    class Meta:
        model = Insumo
        fields = '__all__'


class GuiaDesempenoRazaSerializer(serializers.ModelSerializer):
    raza_nombre = serializers.ReadOnlyField(source='raza.nombre')
    
    class Meta:
        model = GuiaDesempenoRaza
        fields = '__all__'
