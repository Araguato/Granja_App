@echo off
echo ======================================================
echo    INICIANDO SERVIDOR DJANGO
echo ======================================================

:: Activar entorno virtual
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo No se encontro el entorno virtual.
    echo Creando uno nuevo...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo Instalando dependencias de Django...
    pip install django djangorestframework django-cors-headers
)

:: Verificar si hay migraciones pendientes
echo Verificando migraciones...
python manage.py makemigrations
python manage.py migrate

:: Iniciar el servidor Django
echo.
echo ======================================================
echo    SERVIDOR DJANGO INICIADO EN http://127.0.0.1:8000/
echo ======================================================
echo.
echo Para acceder a la interfaz de administracion:
echo http://127.0.0.1:8000/admin/
echo.
echo Para detener el servidor, presione Ctrl+C
echo.

python manage.py runserver 0.0.0.0:8000

:: Desactivar entorno virtual al salir
call venv\Scripts\deactivate.bat
