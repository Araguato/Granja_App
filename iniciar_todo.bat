@echo off
echo ======================================================
echo    INICIANDO SISTEMA COMPLETO APP_GRANJA
echo ======================================================

:: Iniciar el servidor Django en una nueva ventana
echo Iniciando servidor Django...
start cmd /k "cd %~dp0 && python manage.py runserver 0.0.0.0:8000"

:: Esperar a que el servidor se inicie
echo Esperando a que el servidor Django se inicie...
timeout /t 5 /nobreak

:: Configurar la aplicación Windows para modo online
echo Configurando aplicación Windows para modo online...
cd %~dp0\windows_app
echo {> config.json
echo   "is_offline": false,>> config.json
echo   "api_url": "http://127.0.0.1:8000/api",>> config.json
echo   "username": "",>> config.json
echo   "password": "",>> config.json
echo   "show_stats": true>> config.json
echo }>> config.json

:: Iniciar la aplicación Windows
echo.
echo Iniciando aplicación Windows...
python main.py

echo.
echo Aplicación cerrada.
pause
