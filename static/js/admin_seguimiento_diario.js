(function($) {
    $(document).ready(function() {
        // Función para mostrar/ocultar campos según el tipo de seguimiento
        function toggleFields() {
            var tipoSeguimiento = $('#id_tipo_seguimiento').val();
            
            // Campos de producción de huevos
            if (tipoSeguimiento === 'PRODUCCION') {
                $('.produccion-fields').show();
                // Ocultar inline de engorde si existe
                $('.inline-related.has_original').filter(function() {
                    return $(this).find('h3').text().indexOf('Detalles de Engorde') !== -1;
                }).hide();
            } else if (tipoSeguimiento === 'ENGORDE') {
                $('.produccion-fields').hide();
            } else {
                // MIXTO
                $('.produccion-fields').show();
            }
        }
        
        // Ejecutar al cargar la página
        toggleFields();
        
        // Ejecutar cuando cambie el tipo de seguimiento
        $('#id_tipo_seguimiento').change(toggleFields);
        
        // Calcular automáticamente la conversión alimenticia si es posible
        function calcularConversionAlimenticia() {
            var $gananciaInput = $('#id_detalle_engorde-0-ganancia_diaria_peso');
            var $conversionInput = $('#id_detalle_engorde-0-conversion_alimenticia');
            var $consumoInput = $('#id_consumo_alimento_kg');
            
            if ($gananciaInput.length && $conversionInput.length && $consumoInput.length) {
                var ganancia = parseFloat($gananciaInput.val());
                var consumo = parseFloat($consumoInput.val());
                
                if (!isNaN(ganancia) && !isNaN(consumo) && ganancia > 0) {
                    var conversion = consumo / (ganancia / 1000); // Convertir ganancia de g a kg
                    if (!isNaN(conversion)) {
                        $conversionInput.val(conversion.toFixed(2));
                    }
                }
            }
        }
        
        // Calcular cuando cambien los valores relevantes
        $('#id_detalle_engorde-0-ganancia_diaria_peso, #id_consumo_alimento_kg').change(function() {
            calcularConversionAlimenticia();
        });
    });
})(django.jQuery);
