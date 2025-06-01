@echo off
echo ===================================
echo Diagnóstico de API App Granja
echo ===================================

REM Cambiar al directorio del script
cd /d %~dp0

REM Crear directorio de logs si no existe
if not exist logs mkdir logs

echo Ejecutando diagnóstico completo de la API...
echo Este proceso puede tardar unos segundos.
echo.
echo El resultado se guardará en la carpeta "logs"
echo.

REM Ejecutar el script de diagnóstico
python diagnostico_api.py

pause
