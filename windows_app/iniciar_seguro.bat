@echo off
echo ===================================
echo Iniciando App Granja en modo seguro
echo ===================================

REM Cambiar al directorio del script
cd /d %~dp0

REM Ejecutar el script de inicio seguro
python safe_start.py

pause
