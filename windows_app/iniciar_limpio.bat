@echo off
echo ======================================================
echo    INICIANDO APP GRANJA (MODO LIMPIO)
echo ======================================================

:: Reemplazar el archivo config.json corrupto con uno nuevo
echo Reemplazando archivo de configuracion...
copy /Y config_nuevo.json config.json

:: Iniciar la aplicacion en modo offline
echo.
echo Iniciando aplicacion en modo offline...
python main.py --offline

echo.
echo Aplicacion cerrada.
pause
