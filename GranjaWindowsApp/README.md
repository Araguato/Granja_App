# Sistema de Gestión Avícola - Aplicación de Escritorio

Aplicación de escritorio para la gestión de una granja avícola, desarrollada con Python y PyQt6.

## Características

- Gestión de granjas y galpones
- Control de lotes de aves
- Seguimiento de producción diaria
- Gestión de inventario
- Control de ventas
- Generación de reportes

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio o descarga los archivos
2. Crea un entorno virtual (recomendado):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Ejecución

1. Activa el entorno virtual si no está activado:
   ```
   venv\Scripts\activate
   ```
2. Ejecuta la aplicación:
   ```
   python main.py
   ```

## Estructura del Proyecto

- `main.py` - Punto de entrada de la aplicación
- `database.py` - Configuración y modelos de la base de datos
- `requirements.txt` - Dependencias del proyecto
- `ui/` - Módulos de interfaz de usuario
- `models/` - Modelos de datos
- `controllers/` - Lógica de negocio
- `utils/` - Utilidades varias

## Base de Datos

La aplicación utiliza SQLite como base de datos. El archivo de base de datos (`granja.db`) se creará automáticamente en el directorio raíz del proyecto la primera vez que se ejecute la aplicación.

## Licencia

Este proyecto está bajo la Licencia MIT.
