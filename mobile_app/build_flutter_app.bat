@echo off
echo ===================================================
echo Construccion de App Granja - Aplicacion Movil
echo ===================================================

echo.
echo Verificando Flutter...
where flutter >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Flutter no encontrado en el PATH.
    echo Por favor, instale Flutter y agregelo al PATH.
    echo Visite: https://flutter.dev/docs/get-started/install
    pause
    exit /b 1
)

echo.
echo Flutter encontrado. Verificando version...
flutter --version

echo.
echo Limpiando proyecto...
flutter clean

echo.
echo Obteniendo dependencias...
flutter pub get

echo.
echo Verificando problemas...
flutter analyze

echo.
echo Ejecutando pruebas...
flutter test

echo.
echo Construyendo APK...
flutter build apk --release

echo.
echo Construyendo Bundle AAB para Google Play...
flutter build appbundle --release

echo.
if exist "build\app\outputs\flutter-apk\app-release.apk" (
    echo APK generado correctamente en:
    echo build\app\outputs\flutter-apk\app-release.apk
) else (
    echo ERROR: No se pudo generar el APK.
)

echo.
if exist "build\app\outputs\bundle\release\app-release.aab" (
    echo Bundle AAB generado correctamente en:
    echo build\app\outputs\bundle\release\app-release.aab
) else (
    echo ERROR: No se pudo generar el Bundle AAB.
)

echo.
echo ===================================================
echo Para ejecutar la aplicacion en modo desarrollo:
echo flutter run
echo ===================================================

pause
