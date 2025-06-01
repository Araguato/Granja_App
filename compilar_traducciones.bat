@echo off
echo ===============================================================
echo COMPILANDO ARCHIVOS DE TRADUCCION PARA APP_GRANJA
echo ===============================================================
echo.

REM Compilar archivos de traducción
echo Compilando archivos de traducción...
python manage.py compilemessages
echo.

echo ===============================================================
echo TRADUCCIONES COMPILADAS CORRECTAMENTE
echo ===============================================================
echo.
echo Los archivos de traducción han sido compilados correctamente.
echo Ahora puede reiniciar el servidor Django para aplicar los cambios.
echo.
echo Para reiniciar el servidor Django, ejecute:
echo.
echo    iniciar_servidor_django.bat
echo.
echo ===============================================================

pause
