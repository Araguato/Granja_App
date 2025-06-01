from rest_framework import serializers
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario, MortalidadDiaria, MortalidadSemanal

class GranjaSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.ReadOnlyField(source='empresa.nombre', default='')
    encargado_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Granja
        fields = '__all__'
    
    def get_encargado_nombre(self, obj):
        if obj.encargado:
            return f"{obj.encargado.first_name} {obj.encargado.last_name}".strip() or obj.encargado.username
        return ""


class GalponSerializer(serializers.ModelSerializer):
    granja_nombre = serializers.ReadOnlyField(source='granja.nombre')
    tipo_galpon_display = serializers.ReadOnlyField(source='get_tipo_galpon_display')
    responsable_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = Galpon
        fields = '__all__'
    
    def get_responsable_nombre(self, obj):
        if obj.responsable:
            return f"{obj.responsable.first_name} {obj.responsable.last_name}".strip() or obj.responsable.username
        return ""


class LoteSerializer(serializers.ModelSerializer):
    galpon_info = serializers.ReadOnlyField(source='galpon.__str__')
    raza_nombre = serializers.ReadOnlyField(source='raza.nombre')
    alimento_nombre = serializers.ReadOnlyField(source='alimento.nombre', default='')
    estado_display = serializers.ReadOnlyField(source='get_estado_lote_display')
    edad_actual = serializers.SerializerMethodField()
    
    class Meta:
        model = Lote
        fields = '__all__'
    
    def get_edad_actual(self, obj):
        return obj.calcular_edad_actual()


class SeguimientoDiarioSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.ReadOnlyField(source='lote.codigo_lote')
    tipo_seguimiento_display = serializers.ReadOnlyField(source='get_tipo_seguimiento_display')
    aves_presentes_count = serializers.SerializerMethodField()
    mortalidad_dia = serializers.SerializerMethodField()
    huevos_total = serializers.SerializerMethodField()
    
    class Meta:
        model = SeguimientoDiario
        fields = '__all__'
    
    def get_aves_presentes_count(self, obj):
        return obj.aves_presentes()
    
    def get_mortalidad_dia(self, obj):
        return obj.mortalidad_del_dia()
    
    def get_huevos_total(self, obj):
        return obj.huevos_total_dia()


class MortalidadDiariaSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.ReadOnlyField(source='lote.codigo_lote')
    
    class Meta:
        model = MortalidadDiaria
        fields = '__all__'


class MortalidadSemanalSerializer(serializers.ModelSerializer):
    lote_codigo = serializers.ReadOnlyField(source='lote.codigo_lote')
    
    class Meta:
        model = MortalidadSemanal
        fields = '__all__'
