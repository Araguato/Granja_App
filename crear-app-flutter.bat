@echo off
echo Configurando entorno para Flutter...
set PATH=%PATH%;C:\Program Files\Git\bin;C:\Program Files\Git\cmd
echo.
echo Entorno configurado correctamente!
echo.
echo Creando proyecto Flutter para App_Granja...
echo.

mkdir C:\App_Granja_Flutter_API
cd /d C:\src\flutter
call bin\flutter.bat create --org com.granja --project-name app_granja_flutter_api C:\App_Granja_Flutter_API

echo.
echo Proyecto creado en C:\App_Granja_Flutter_API
echo.
echo Instalando dependencias necesarias...
cd /d C:\App_Granja_Flutter_API

:: Agregar dependencias necesarias
call flutter pub add http
call flutter pub add provider
call flutter pub add flutter_secure_storage
call flutter pub add intl
call flutter pub add flutter_dotenv
call flutter pub add connectivity_plus
call flutter pub add cached_network_image

echo.
echo Proyecto configurado con dependencias básicas.
echo.
echo Presiona cualquier tecla para cerrar esta ventana.
pause > nul
