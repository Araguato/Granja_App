@echo off
echo Configurando y ejecutando App Granja para Windows...

REM Verificar si existe el entorno virtual
echo Verificando entorno virtual...
if not exist ..\venv\Scripts\python.exe (
    echo No se encontro el entorno virtual en ..\venv
    echo Por favor, asegurese de que el entorno virtual este correctamente configurado.
    pause
    exit /b 1
)

REM Establecer ruta al Python del entorno virtual
echo Usando Python del entorno virtual...
set PYTHON_PATH=..\venv\Scripts\python.exe

REM Instalar dependencias
echo Instalando dependencias...
%PYTHON_PATH% -m pip install PyQt5 PyQtChart requests pillow

REM Verificar si el servidor Django esta en ejecucion
echo Verificando si el servidor Django esta en ejecucion...
curl -s http://localhost:8000/api/ >nul
if %ERRORLEVEL% NEQ 0 (
    echo ADVERTENCIA: El servidor Django no parece estar en ejecucion.
    echo Para una funcionalidad completa, asegurese de que el servidor este ejecutandose.
    echo Puede iniciar el servidor con el comando: python manage.py runserver
    echo.
    echo Presione cualquier tecla para continuar de todos modos...
    pause >nul
)

REM Ejecutar la aplicacion
echo Iniciando App Granja para Windows...
%PYTHON_PATH% main.py

echo Aplicacion cerrada.
pause
