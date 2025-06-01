@echo off
echo ======================================================
echo    INICIANDO APP GRANJA CON ESTADISTICAS
echo ======================================================

:: Asegurarse de estar en el directorio correcto
cd %~dp0

:: Configurar modo offline con estadísticas
echo Configurando modo offline con estadísticas...
echo {> config.json
echo   "is_offline": true,>> config.json
echo   "api_url": "http://127.0.0.1:8000/api",>> config.json
echo   "username": "admin",>> config.json
echo   "password": "admin123",>> config.json
echo   "show_stats": true>> config.json
echo }>> config.json

:: Iniciar la aplicacion
echo.
echo Iniciando aplicacion...
python main.py --offline

echo.
echo Aplicacion cerrada.
pause
