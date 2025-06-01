@echo off
echo Iniciando App Granja en modo offline...

:: Verificar si existe el entorno virtual
if not exist venv\Scripts\python.exe (
    echo No se encontro el entorno virtual. Creando uno nuevo...
    python -m venv venv
)

:: Activar entorno virtual
call venv\Scripts\activate.bat

:: Instalar todas las dependencias necesarias
echo Instalando todas las dependencias necesarias...

:: Dependencias principales
pip install PyQt5 PyQtChart requests pillow

:: Dependencias adicionales
pip install qrcode pandas matplotlib

:: Crear archivo de configuración para forzar modo offline
echo Configurando modo offline...
echo {"is_offline": true, "api_url": "http://127.0.0.1:8000/api", "username": "admin", "password": "admin123"} > config.json

:: Iniciar la aplicación
echo Iniciando aplicacion en modo offline...
python main.py --offline

:: Desactivar entorno virtual al salir
call venv\Scripts\deactivate.bat

echo Aplicacion cerrada.
pause
