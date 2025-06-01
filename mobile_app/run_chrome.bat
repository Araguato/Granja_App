@echo off
echo ===================================
echo Ejecutando la aplicacion Flutter en Chrome
echo ===================================

REM Cambiar al directorio del proyecto Flutter
cd /d %~dp0
echo Directorio actual: %CD%

REM Verificar si Flutter está instalado
where flutter >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flutter no está instalado o no está en el PATH.
    echo Por favor, instale Flutter y asegúrese de que esté en el PATH.
    echo Visite https://flutter.dev/docs/get-started/install para más información.
    pause
    exit /b 1
)

echo Obteniendo dependencias...
flutter pub get

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudieron obtener las dependencias.
    pause
    exit /b 1
)

echo.
echo Ejecutando la aplicación en Chrome...
flutter run -d chrome

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo ejecutar la aplicación en Chrome.
    echo Asegúrese de que Chrome esté instalado y disponible.
    pause
    exit /b 1
)

echo.
echo La aplicación se ha ejecutado correctamente.
pause
