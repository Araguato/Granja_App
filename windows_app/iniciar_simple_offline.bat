@echo off
echo ======================================================
echo    INICIANDO APP GRANJA (MODO SIMPLE OFFLINE)
echo ======================================================

:: Asegurarse de estar en el directorio correcto
cd %~dp0

:: Configurar modo offline simple
echo Configurando modo offline simple...
echo {> config.json
echo   "is_offline": true,>> config.json
echo   "api_url": "http://127.0.0.1:8000/api",>> config.json
echo   "username": "admin",>> config.json
echo   "password": "admin123">> config.json
echo }>> config.json

:: Iniciar la aplicacion con argumentos simples
echo.
echo Iniciando aplicacion en modo offline simple...
python main.py --offline --simple

echo.
echo Aplicacion cerrada.
pause
