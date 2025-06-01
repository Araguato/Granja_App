@echo off
echo ===================================
echo Iniciando App Granja Mobile
echo ===================================

cd /d %~dp0
echo Directorio: %CD%

echo.
echo Ejecutando en Chrome...
flutter run -d chrome --no-verbose

pause
