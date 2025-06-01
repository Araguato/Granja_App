from rest_framework import serializers
from avicola.models import UserProfile
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario
from inventario.models import Raza, Alimento


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']
        read_only_fields = ['is_staff', 'is_superuser', 'date_joined', 'last_login']


class RazaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raza
        fields = '__all__'


class AlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimento
        fields = '__all__'


class GranjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Granja
        fields = '__all__'


class GalponSerializer(serializers.ModelSerializer):
    granja_nombre = serializers.ReadOnlyField(source='granja.nombre')
    
    class Meta:
        model = Galpon
        fields = '__all__'


class LoteSerializer(serializers.ModelSerializer):
    galpon_info = serializers.ReadOnlyField(source='galpon.__str__')
    raza_nombre = serializers.ReadOnlyField(source='raza.nombre')
    
    class Meta:
        model = Lote
        fields = '__all__'


class SeguimientoDiarioSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.ReadOnlyField(source='lote.codigo_lote')
    
    class Meta:
        model = SeguimientoDiario
        fields = '__all__'
