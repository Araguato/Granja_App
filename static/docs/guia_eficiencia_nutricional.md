# Guía de Eficiencia Nutricional para Aves de Engorde

## Introducción

Esta guía proporciona información sobre los indicadores de eficiencia nutricional implementados en el sistema de gestión avícola App_Granja. Estos indicadores son herramientas valiosas para evaluar el rendimiento de los lotes de aves y optimizar la alimentación.

## Indicadores Principales

### 1. Eficiencia Energética (kcal/g)

**Definición**: Cantidad de energía (kcal) consumida por cada gramo de ganancia de peso.

**Cálculo**: `Consumo de energía (kcal) ÷ Ganancia de peso (g)`

**Interpretación**:
- **< 3.0**: Excelente eficiencia (verde)
- **3.0 - 3.5**: Eficiencia aceptable (amarillo)
- **> 3.5**: Eficiencia deficiente (rojo)

**Objetivo**: Valores más bajos indican mejor eficiencia, ya que el ave necesita menos energía para producir un gramo de carne.

### 2. Eficiencia Proteica (g/g)

**Definición**: Cantidad de proteína (g) consumida por cada gramo de ganancia de peso.

**Cálculo**: `Consumo de proteína (g) ÷ Ganancia de peso (g)`

**Interpretación**:
- **< 0.40**: Excelente eficiencia (verde)
- **0.40 - 0.45**: Eficiencia aceptable (amarillo)
- **> 0.45**: Eficiencia deficiente (rojo)

**Objetivo**: Valores más bajos indican mejor eficiencia, ya que el ave utiliza menos proteína para producir un gramo de carne.

### 3. Relación Energía/Proteína

**Definición**: Proporción entre la energía y la proteína en la dieta.

**Cálculo**: `Consumo de energía (kcal) ÷ Consumo de proteína (g)`

**Interpretación**:
- **140 - 160**: Relación óptima (verde)
- **130 - 140 o 160 - 170**: Relación aceptable (amarillo)
- **< 130 o > 170**: Relación desequilibrada (rojo)

**Objetivo**: Mantener un equilibrio adecuado entre energía y proteína para optimizar el crecimiento y la salud de las aves.

## Factores que Afectan la Eficiencia Nutricional

1. **Calidad del alimento**: Ingredientes de alta calidad y correctamente procesados mejoran la digestibilidad y la eficiencia.

2. **Condiciones ambientales**: Temperatura, humedad y ventilación óptimas reducen el estrés y mejoran la eficiencia.

3. **Estado sanitario**: Aves sanas utilizan los nutrientes de manera más eficiente.

4. **Genética**: Diferentes razas tienen diferentes capacidades para convertir alimento en carne.

5. **Manejo alimenticio**: Horarios de alimentación, disponibilidad de agua y presentación del alimento afectan la eficiencia.

## Cómo Mejorar la Eficiencia Nutricional

1. **Formulación precisa**: Ajustar las dietas según la edad, etapa de crecimiento y necesidades específicas.

2. **Control de calidad**: Monitorear regularmente la calidad de los ingredientes y del alimento terminado.

3. **Ambiente controlado**: Mantener condiciones ambientales óptimas para minimizar el estrés.

4. **Prevención de enfermedades**: Implementar programas de bioseguridad y vacunación efectivos.

5. **Monitoreo regular**: Seguimiento constante de los indicadores para detectar problemas tempranamente.

## Uso del Sistema

El sistema App_Granja calcula automáticamente estos indicadores basándose en:
- Consumo de alimento registrado
- Ganancia de peso diaria
- Valores nutricionales del alimento (energía metabolizable y contenido proteico)

Los indicadores se muestran en:
1. **Panel de estadísticas**: Gráficos de evolución temporal y comparativas por galpón
2. **Administración**: Vista detallada en los registros de seguimiento de engorde

Para actualizar los valores de eficiencia nutricional en registros existentes, use el comando:
```
python manage.py actualizar_eficiencia_nutricional
```

O para actualizar solo los registros recientes:
```
python manage.py actualizar_eficiencia_nutricional --dias=30
```

## Contacto

Para más información o asistencia, contacte al equipo de soporte técnico.
