@echo off
echo Generando aplicacion Flutter para App Granja...

REM Verificar si Flutter esta instalado
where flutter >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Flutter no esta instalado o no esta en el PATH.
    echo Por favor, instale Flutter desde https://flutter.dev/docs/get-started/install
    exit /b 1
)

REM Crear directorio para la aplicacion Flutter
set APP_DIR=app_granja_mobile
if exist %APP_DIR% (
    echo El directorio %APP_DIR% ya existe.
    set /p CONTINUE=Desea continuar y sobrescribir? (S/N): 
    if /i "%CONTINUE%" NEQ "S" exit /b 0
    rmdir /s /q %APP_DIR%
)

REM Crear nueva aplicacion Flutter
echo Creando nueva aplicacion Flutter...
flutter create --org com.appgranja --project-name app_granja %APP_DIR%

REM Copiar archivos de la estructura a la aplicacion
echo Copiando archivos de la estructura a la aplicacion...
xcopy /E /I /Y flutter_app_structure\models %APP_DIR%\lib\models
xcopy /E /I /Y flutter_app_structure\providers %APP_DIR%\lib\providers
xcopy /E /I /Y flutter_app_structure\screens %APP_DIR%\lib\screens
xcopy /E /I /Y flutter_app_structure\services %APP_DIR%\lib\services
xcopy /E /I /Y flutter_app_structure\widgets %APP_DIR%\lib\widgets
copy /Y flutter_app_structure\main.dart %APP_DIR%\lib\main.dart

REM Actualizar pubspec.yaml con las dependencias necesarias
echo Actualizando pubspec.yaml con las dependencias necesarias...
echo dependencies: > temp.txt
echo   flutter: >> temp.txt
echo     sdk: flutter >> temp.txt
echo   provider: ^6.0.5 >> temp.txt
echo   http: ^1.1.0 >> temp.txt
echo   intl: ^0.18.1 >> temp.txt
echo   flutter_secure_storage: ^8.0.0 >> temp.txt
echo   shared_preferences: ^2.2.0 >> temp.txt
echo   path_provider: ^2.1.0 >> temp.txt
echo   url_launcher: ^6.1.12 >> temp.txt
echo   flutter_svg: ^2.0.7 >> temp.txt
echo   cached_network_image: ^3.2.3 >> temp.txt

findstr /v "dependencies:" %APP_DIR%\pubspec.yaml > %APP_DIR%\pubspec_temp.yaml
type temp.txt >> %APP_DIR%\pubspec_temp.yaml
findstr /B /C:"dev_dependencies:" /C:"flutter:" /C:"  uses-material-design:" %APP_DIR%\pubspec.yaml >> %APP_DIR%\pubspec_temp.yaml
move /Y %APP_DIR%\pubspec_temp.yaml %APP_DIR%\pubspec.yaml
del temp.txt

REM Obtener dependencias
echo Obteniendo dependencias...
cd %APP_DIR%
flutter pub get

echo.
echo Aplicacion Flutter generada correctamente en el directorio %APP_DIR%.
echo Para ejecutar la aplicacion:
echo   cd %APP_DIR%
echo   flutter run
echo.

pause
