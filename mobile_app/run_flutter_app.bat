@echo off
echo ===================================
echo Ejecutando la aplicacion Flutter
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
echo Dispositivos disponibles:
flutter devices

echo.
echo Seleccione una opción:
echo 1 - Ejecutar en Chrome
echo 2 - Ejecutar en Windows
echo 3 - Ejecutar en dispositivo predeterminado
echo.

set /p opcion=Ingrese su opción (1, 2 o 3): 

if "%opcion%"=="1" (
    echo.
    echo Ejecutando la aplicación en Chrome...
    flutter run -d chrome
) else if "%opcion%"=="2" (
    echo.
    echo Ejecutando la aplicación en Windows...
    flutter run -d windows
) else (
    echo.
    echo Ejecutando la aplicación en el dispositivo predeterminado...
    flutter run
)

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo ejecutar la aplicación.
    echo Verifique que haya un dispositivo conectado o un emulador en ejecución.
    echo Para ver los dispositivos disponibles, ejecute 'flutter devices'.
    pause
    exit /b 1
)

echo.
echo La aplicación se ha ejecutado correctamente.
pause
