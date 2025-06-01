@echo off
echo Reiniciando el servidor Django...

REM Activar el entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo No se encontro el entorno virtual en venv\Scripts\activate.bat
    echo Intentando continuar sin activar el entorno virtual...
)

REM Detener cualquier proceso de Django en ejecución (opcional)
taskkill /f /im python.exe /fi "WINDOWTITLE eq Django*" 2>nul

REM Iniciar el servidor Django
echo Iniciando el servidor Django...
start "Django Server" cmd /k python manage.py runserver 0.0.0.0:8000

echo Servidor reiniciado correctamente.
echo Accede a http://127.0.0.1:8000/ para ver la aplicación.
