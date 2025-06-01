# App Granja - Sistema de Gestión Avícola

## Descripción
Sistema de gestión integral para granjas avícolas, desarrollado en Django 5.0.6 con PostgreSQL.

## Estructura del Proyecto

### Módulos Principales

1. **avicola**: Gestión de usuarios y empresa
   - `UserProfile`: Extiende AbstractUser con roles (Admin, Supervisor, Veterinario, Operario)
   - `Empresa`: Datos de la empresa (RIF, nombre, dirección)

2. **inventario**: Control de inventario
   - `Proveedor`: Gestión de proveedores
   - `Raza`: Tipos de razas de aves (Ponedora, Engorde, Doble Propósito)
   - `Alimento`: Tipos de alimentos y sus características
   - `Vacuna`: Control de vacunas y lotes
   - `Insumo`: Medicamentos, equipos y otros insumos
   - `GuiaDesempenoRaza`: Estándares de desempeño por raza y día

3. **produccion**: Gestión de producción
   - `Granja`: Instalaciones físicas
   - `Galpon`: Divisiones dentro de la granja
   - `Lote`: Grupos de aves
   - `SeguimientoDiario`: Registro diario de producción y mortalidad

4. **ventas**: Gestión comercial
   - `Cliente`: Datos de clientes
   - `TipoHuevo`: Clasificación de huevos
   - `InventarioHuevos`: Control de stock
   - `Venta`: Registro de ventas

5. **reportes**: Generación de informes

### Configuración

El proyecto utiliza el archivo `granja/settings.py` como configuración principal.

### Dependencias Principales
- Python 3.13.0
- Django 5.0.6
- PostgreSQL
- django-admin-interface
- django-crispy-forms
- django-import-export

## Instrucciones de Ejecución

1. Activar el entorno virtual: `venv\Scripts\activate`
2. Ejecutar el servidor: `py manage.py runserver`
3. Acceder al admin: http://127.0.0.1:8000/admin/

## Mantenimiento

### Migraciones
Para crear nuevas migraciones: `py manage.py makemigrations`
Para aplicar migraciones: `py manage.py migrate`

### Respaldos
Los respaldos del proyecto se encuentran en la carpeta `backups/`
