# Documentación del Proyecto App_Granja

## 1. Descripción General

App_Granja es un sistema integral para la gestión de granjas avícolas, diseñado para optimizar y controlar todos los procesos relacionados con la producción, inventario, ventas y administración de granjas dedicadas a la producción de huevos y crianza de aves. El sistema está compuesto por una aplicación web desarrollada en Django y una aplicación de escritorio para Windows que puede funcionar tanto en modo online como offline.

## 2. Propósito y Objetivos

El propósito principal de App_Granja es proporcionar una herramienta tecnológica que permita a los productores avícolas:

- **Gestionar eficientemente** todos los aspectos de la operación avícola
- **Monitorear en tiempo real** los indicadores clave de producción
- **Optimizar recursos** mediante el seguimiento detallado de insumos y resultados
- **Facilitar la toma de decisiones** con reportes y estadísticas detalladas
- **Mejorar la trazabilidad** de los productos desde la incubación hasta la venta

## 3. Entorno Tecnológico

### 3.1. Backend

- **Framework**: Django 5.0.6
- **Base de datos**: PostgreSQL
- **Lenguaje de programación**: Python
- **Autenticación**: Sistema de autenticación de Django con roles personalizados

### 3.2. Frontend Web

- **Framework CSS**: Bootstrap 5
- **Bibliotecas JavaScript**: Chart.js para visualizaciones gráficas
- **Plantillas**: Sistema de plantillas de Django con soporte para internacionalización

### 3.3. Aplicación de Escritorio

- **Framework**: PyQt para la interfaz gráfica
- **Comunicación**: API REST para sincronización con el servidor
- **Modo Offline**: Capacidad para trabajar sin conexión y sincronizar posteriormente

### 3.4. Integración y Despliegue

- **Scripts de automatización**: Archivos batch para iniciar servicios y aplicaciones
- **Sistema de respaldo**: Mecanismo automatizado para copias de seguridad
- **Internacionalización**: Soporte para múltiples idiomas (español e inglés)

## 4. Estructura del Proyecto

### 4.1. Aplicaciones Django

El proyecto está organizado en varias aplicaciones Django, cada una con responsabilidades específicas:

#### 4.1.1. Avicola (Core)

Contiene los modelos y funcionalidades centrales del sistema:
- Gestión de usuarios y permisos
- Perfiles de usuario con roles específicos (Administrador, Supervisor, Veterinario, Operario)
- Información de la empresa

#### 4.1.2. Producción

Gestiona todo lo relacionado con la producción avícola:
- Granjas y galpones
- Lotes de aves
- Seguimiento diario de producción
- Registro de mortalidad
- Monitoreo de parámetros productivos

#### 4.1.3. Inventario

Administra los recursos e insumos:
- Alimentos y sus características nutricionales
- Vacunas y medicamentos
- Proveedores
- Razas de aves y sus guías de desempeño
- Otros insumos y equipos

#### 4.1.4. Ventas

Controla la comercialización de productos:
- Gestión de clientes
- Clasificación de huevos
- Inventario de productos terminados
- Registro de ventas y facturación

#### 4.1.5. Reportes

Genera informes y análisis:
- Reportes de producción (diarios, semanales, mensuales)
- Reportes de mortalidad
- Reportes de inventario y costos
- Reportes de ventas y rendimiento

#### 4.1.6. Respaldos

Sistema de copias de seguridad:
- Respaldo automático programado
- Respaldo de base de datos y archivos de medios
- Rotación de respaldos
- Notificaciones por correo

#### 4.1.7. Core

Funcionalidades transversales:
- Middleware para gestión de permisos
- Estadísticas y dashboard
- Autenticación y autorización
- Manejo de errores

### 4.2. Aplicación Windows

Aplicación de escritorio que permite:
- Trabajar en modo online conectado al servidor Django
- Trabajar en modo offline con datos locales
- Sincronizar datos cuando se restablece la conexión
- Visualizar estadísticas y gráficos
- Realizar operaciones básicas sin necesidad del servidor

## 5. Modelos de Datos

### 5.1. Usuarios y Perfiles

- **UserProfile**: Extiende el modelo de usuario de Django con roles específicos (Administrador, Supervisor, Veterinario, Operario)
- **Empresa**: Información de la empresa propietaria de la granja

### 5.2. Producción

- **Granja**: Unidad principal de producción
- **Galpón**: Estructura física donde se alojan las aves
- **Lote**: Grupo de aves de la misma edad y características
- **SeguimientoDiario**: Registro diario de parámetros productivos
- **MortalidadDiaria**: Registro de mortalidad por día
- **MortalidadSemanal**: Consolidado semanal de mortalidad

### 5.3. Inventario

- **Proveedor**: Empresas que suministran insumos
- **Raza**: Tipos de aves y sus características
- **Alimento**: Productos alimenticios con sus propiedades nutricionales
- **Vacuna**: Productos veterinarios para prevención
- **Insumo**: Otros materiales y equipos
- **GuiaDesempenoRaza**: Parámetros ideales por raza y edad

### 5.4. Ventas

- **Cliente**: Compradores de los productos
- **TipoHuevo**: Clasificación de huevos según tamaño
- **InventarioHuevos**: Stock disponible para venta
- **Venta**: Registro de transacciones comerciales
- **DetalleVenta**: Ítems específicos de cada venta

## 6. Funcionalidades Principales

### 6.1. Gestión de Usuarios y Permisos

- Sistema de roles con permisos específicos
- Middleware personalizado para asignar permisos dinámicamente
- Acceso controlado a diferentes secciones según el rol

### 6.2. Dashboard y Estadísticas

- Visualización de indicadores clave de rendimiento
- Gráficos de producción de huevos
- Gráficos de mortalidad
- Estadísticas de ventas
- Distribución por tipo de huevo
- Resumen de inventario

### 6.3. Seguimiento de Lotes

- Registro de parámetros diarios
- Cálculo automático de indicadores de eficiencia
- Comparación con parámetros ideales
- Alertas sobre desviaciones significativas

### 6.4. Gestión de Inventario

- Control de stock de alimentos y medicamentos
- Registro de movimientos de inventario
- Alertas de punto de reorden
- Trazabilidad de insumos utilizados

### 6.5. Sistema de Ventas

- Registro de clientes y transacciones
- Facturación y control de pagos
- Descuento automático de inventario
- Reportes de ventas por período

### 6.6. Reportes y Análisis

- Generación de reportes en múltiples formatos (PDF, Excel, CSV)
- Plantillas personalizables
- Análisis comparativos
- Proyecciones y tendencias

### 6.7. Operación Offline

- Capacidad para trabajar sin conexión
- Almacenamiento local de datos
- Sincronización cuando se restablece la conexión
- Datos de ejemplo para pruebas

## 7. Interfaz de Usuario

### 7.1. Interfaz Web

- Diseño responsivo basado en Bootstrap
- Dashboard interactivo con gráficos y estadísticas
- Formularios optimizados para entrada rápida de datos
- Tablas con filtros y ordenamiento
- Soporte para múltiples idiomas

### 7.2. Aplicación Windows

- Interfaz nativa para Windows
- Acceso rápido a funciones principales
- Sincronización con el servidor
- Notificaciones y alertas
- Modo offline con funcionalidad completa

## 8. Seguridad

- Autenticación segura de usuarios
- Roles y permisos granulares
- Registro de actividades (logs)
- Respaldo automático de datos
- Cifrado de información sensible

## 9. Integración y APIs

- API REST para comunicación con aplicaciones externas
- Endpoints documentados para integración
- Autenticación mediante tokens JWT
- Soporte para operaciones CRUD en todos los modelos principales

## 10. Despliegue y Configuración

### 10.1. Requisitos del Sistema

- **Servidor Web**: Django con Gunicorn/WSGI
- **Base de Datos**: PostgreSQL
- **Sistema Operativo**: Compatible con Windows, Linux
- **Aplicación Windows**: Windows 7 o superior

### 10.2. Scripts de Inicio

- `iniciar_servidor_django.bat`: Inicia el servidor Django
- `iniciar_app_online.bat`: Inicia la aplicación Windows en modo online
- `iniciar_limpio.bat`: Inicia la aplicación Windows con configuración limpia
- `iniciar_modo_offline.bat`: Inicia la aplicación Windows en modo offline

## 11. Mantenimiento y Soporte

- Sistema de respaldo automatizado
- Rotación de copias de seguridad
- Notificaciones de errores
- Herramientas de diagnóstico
- Documentación técnica y de usuario

## 12. Extensibilidad

El sistema está diseñado para ser extensible mediante:

- Arquitectura modular
- Separación clara de responsabilidades
- Uso de patrones de diseño estándar
- Documentación del código
- APIs bien definidas

## 13. Conclusiones

App_Granja representa una solución integral para la gestión avícola, combinando la potencia de una aplicación web Django con la flexibilidad de una aplicación de escritorio. Su diseño modular y enfoque en la usabilidad lo hacen adecuado tanto para pequeñas granjas como para operaciones de mayor escala.

El sistema proporciona las herramientas necesarias para optimizar la producción, controlar costos, mejorar la trazabilidad y facilitar la toma de decisiones basada en datos, contribuyendo significativamente a la eficiencia y rentabilidad de las operaciones avícolas.
