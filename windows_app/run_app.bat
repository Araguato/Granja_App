@echo off
echo Iniciando App Granja - Aplicacion de Escritorio...

REM Activar entorno virtual
call ..\venv\Scripts\activate.bat

REM Ejecutar aplicacion
python main.py

REM Desactivar entorno virtual
deactivate
