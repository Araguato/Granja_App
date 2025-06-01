# Plan de Mejoras para la Aplicación Web de App_Granja

## 1. Comparación de Razas Mejorada

### Descripción
Implementar una comparación entre los datos nominales de una raza (guía de desempeño) y los datos reales de un lote activo de la misma raza.

### Implementación
1. **Modelo de datos**:
   - Crear modelo `RazaDesempeño` para almacenar los datos nominales de cada raza por día de edad
   - Campos: raza, día_edad, peso_esperado, consumo_esperado, ganancia_esperada, etc.

2. **API Endpoints**:
   - Crear endpoint `/api/razas/desempeno/` para obtener los datos nominales de una raza
   - Modificar endpoint `/api/estadisticas/comparacion-razas/` para comparar datos nominales vs. reales

3. **Interfaz de usuario**:
   - Crear vista de comparación con:
     - Selector de raza (COBB 500, Ross 308, etc.)
     - Selector de lote activo de la misma raza
     - Gráficos comparativos para peso, consumo, mortalidad, etc.
     - Tabla de datos con valores nominales vs. reales

## 2. Selección de Idioma

### Descripción
Restaurar la funcionalidad de selección de idioma que existía anteriormente.

### Implementación
1. **Configuración de internacionalización**:
   - Configurar Django para soporte multiidioma (settings.py)
   - Crear archivos de traducción (.po) para español, inglés, etc.

2. **API Endpoints**:
   - Crear endpoint `/api/configuracion/idioma/` para cambiar el idioma del usuario

3. **Interfaz de usuario**:
   - Añadir selector de idioma en la barra de navegación
   - Guardar preferencia de idioma en el perfil del usuario
   - Aplicar traducciones a todos los textos de la interfaz

## 3. Permisos de Usuario

### Descripción
Solucionar el problema con los permisos de usuarios operarios para acceder a las áreas donde deben introducir datos.

### Implementación
1. **Sistema de permisos**:
   - Revisar y corregir los permisos asignados a los grupos (Administradores, Supervisores, Operarios)
   - Crear permisos específicos para acceso a dashboard, edición de lotes, etc.

2. **Dashboard por tipo de usuario**:
   - Implementar dashboard específico para operarios con:
     - Acceso directo a formularios de entrada de datos
     - Visualización de tareas asignadas
     - Acceso a lotes bajo su responsabilidad

3. **Interfaz de usuario**:
   - Modificar la navegación para mostrar solo las opciones permitidas según el rol
   - Crear accesos directos a formularios de entrada de datos en el dashboard de operarios

## Cronograma de Implementación

1. **Fase 1: Permisos de Usuario** (Prioridad Alta)
   - Corrección de permisos existentes
   - Implementación de dashboard para operarios
   - Pruebas con usuario "pedro"

2. **Fase 2: Comparación de Razas** (Prioridad Media)
   - Modelo de datos para desempeño de razas
   - API endpoints para comparación
   - Interfaz de usuario para visualización

3. **Fase 3: Selección de Idioma** (Prioridad Baja)
   - Configuración de internacionalización
   - Archivos de traducción
   - Selector de idioma en la interfaz

## Recursos Necesarios

1. **Datos de desempeño de razas**:
   - Guías oficiales de COBB 500, Ross 308, etc.
   - Datos por día de edad para peso, consumo, mortalidad, etc.

2. **Traducciones**:
   - Textos en español, inglés y otros idiomas requeridos
   - Traductor o herramienta de traducción

3. **Pruebas de usuario**:
   - Usuarios de diferentes roles para probar permisos
   - Feedback sobre la usabilidad de las nuevas funcionalidades
