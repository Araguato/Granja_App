@echo off
echo ======================================================
echo    INICIANDO APP GRANJA (MODO ONLINE)
echo ======================================================

:: Asegurarse de estar en el directorio correcto
cd %~dp0

:: Configurar modo online en config.json
echo Configurando modo online...
echo {> config.json
echo   "is_offline": false,>> config.json
echo   "api_url": "http://127.0.0.1:8000/api",>> config.json
echo   "username": "",>> config.json
echo   "password": "">> config.json
echo }>> config.json

:: Iniciar la aplicacion en modo normal
echo.
echo Iniciando aplicacion en modo online...
python main.py --online

echo.
echo Aplicacion cerrada.
pause
