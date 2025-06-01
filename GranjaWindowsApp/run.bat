@echo off
echo Iniciando Sistema de Gestión Avícola...

:: Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python no está instalado o no está en el PATH.
    echo Por favor instala Python 3.8 o superior desde https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if virtual environment exists, if not create it
if not exist "venv\" (
    echo Creando entorno virtual...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo Error al crear el entorno virtual.
        pause
        exit /b 1
    )
    
    echo Instalando dependencias...
    call venv\Scripts\activate.bat
    pip install --upgrade pip
    pip install -r requirements.txt
    if %ERRORLEVEL% neq 0 (
        echo Error al instalar las dependencias.
        pause
        exit /b 1
    )
) else (
    call venv\Scripts\activate.bat
)

:: Run the application
echo Iniciando la aplicación...
python main.py

:: Keep the window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo La aplicación se cerró con un error. Presione cualquier tecla para salir...
    pause >nul
)
