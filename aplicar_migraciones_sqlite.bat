@echo off
echo Aplicando migraciones a la base de datos SQLite...

REM Activar el entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo No se encontró el entorno virtual en venv\Scripts\activate.bat
    echo Intentando continuar sin activar el entorno virtual...
)

REM Aplicar migraciones
python manage.py migrate

REM Crear superusuario si no existe
echo.
echo Si no existe un superusuario, puedes crear uno ahora:
python manage.py createsuperuser --username admin

REM Iniciar el servidor Django
echo.
echo Iniciando el servidor Django...
python manage.py runserver 0.0.0.0:8000

pause
