@echo off
echo ======================================================
echo    INICIANDO APP GRANJA CON CONEXION A DJANGO
echo ======================================================

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

:: Configurar para modo normal con manejo de errores mejorado
echo Configurando modo normal (con conexion al banco de datos)...
echo {
  "is_offline": false,
  "api_url": "http://127.0.0.1:8000/api",
  "username": "admin",
  "password": "admin123",
  "auto_offline": true
} > config.json

echo.
echo ======================================================
echo    IMPORTANTE: INFORMACION DE CONEXION
echo ======================================================
echo La aplicacion intentara conectarse a: http://127.0.0.1:8000/api
echo.
echo Si el servidor Django no esta disponible, la aplicacion
echo activara automaticamente el modo offline y mostrara
echo datos de ejemplo sin mostrar mensajes de error.
echo.
echo Si desea conectarse a otra URL de API, modifique el
echo archivo config.json antes de iniciar la aplicacion.
echo ======================================================
echo.

:: Iniciar la aplicacion
echo Iniciando aplicacion...
python main.py

:: Desactivar entorno virtual al salir
call venv\Scripts\deactivate.bat

echo Aplicacion cerrada.
pause
