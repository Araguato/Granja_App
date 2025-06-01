@echo off
echo ======================================================
echo    SOLUCION COMPLETA APP_GRANJA
echo ======================================================

:: Configurar modo offline con estadísticas y comparación de razas
echo Configurando aplicación...

:: Crear archivo de configuración
echo {> config.json
echo   "is_offline": true,>> config.json
echo   "api_url": "http://127.0.0.1:8000/api",>> config.json
echo   "username": "admin",>> config.json
echo   "password": "admin123",>> config.json
echo   "show_stats": true,>> config.json
echo   "enable_comparacion_razas": true>> config.json
echo }>> config.json

:: Iniciar la aplicación
echo.
echo Iniciando aplicación...
python main.py --offline --stats --comparacion

echo.
echo Aplicación cerrada.
pause
