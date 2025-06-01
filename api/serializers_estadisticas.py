from rest_framework import serializers

class EstadisticasSerializer(serializers.Serializer):
    """
    Serializador para las estadísticas del dashboard
    """
    # Producción de huevos
    produccion_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    produccion_datos = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    # Mortalidad
    mortalidad_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    mortalidad_datos = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    # Ventas
    ventas_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    ventas_datos = serializers.ListField(
        child=serializers.FloatField(),
        required=False
    )
    
    # Distribución de tipos de huevo
    tipos_huevo_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    tipos_huevo_datos = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
    
    # Resumen de inventario
    lotes_totales = serializers.IntegerField(required=False)
    lotes_activos = serializers.IntegerField(required=False)
    alimentos_count = serializers.IntegerField(required=False)
    vacunas_count = serializers.IntegerField(required=False)
    
    # Estadísticas de engorde
    engorde_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    engorde_peso = serializers.ListField(
        child=serializers.FloatField(),
        required=False
    )
    engorde_ganancia = serializers.ListField(
        child=serializers.FloatField(),
        required=False
    )
    engorde_conversion = serializers.ListField(
        child=serializers.FloatField(),
        required=False
    )
    
    # Estadísticas por galpón
    galpon_labels = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    galpon_peso = serializers.ListField(
        child=serializers.FloatField(),
        required=False
    )
    galpon_mortalidad = serializers.ListField(
        child=serializers.IntegerField(),
        required=False
    )
