@echo off
echo ======================================================
echo    INICIANDO APP GRANJA (MODO SIMPLE)
echo ======================================================

:: Configurar para modo offline forzado para evitar errores
echo Configurando modo offline forzado...
echo {
  "is_offline": true,
  "api_url": "http://127.0.0.1:8000/api",
  "username": "admin",
  "password": "admin123"
} > config.json

echo.
echo Iniciando aplicacion en modo offline forzado...
echo (Esto evitara cualquier intento de conexion con el servidor)
echo.

:: Iniciar la aplicacion directamente
python main.py --offline

echo.
echo Aplicacion cerrada.
pause
