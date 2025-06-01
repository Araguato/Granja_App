@echo off
echo ===================================
echo Iniciando App Granja en modo offline
echo ===================================

REM Cambiar al directorio del script
cd /d %~dp0

echo Este modo no intenta conectarse al servidor Django
echo y muestra solo datos de ejemplo.
echo.
echo Presione cualquier tecla para continuar...
pause > nul

REM Ejecutar la aplicación en modo offline
python offline_mode.py

pause
