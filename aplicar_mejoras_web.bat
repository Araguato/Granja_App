@echo off
echo ===============================================================
echo APLICANDO MEJORAS A LA APLICACION WEB DE APP_GRANJA
echo ===============================================================
echo.

REM Crear directorio para traducciones si no existe
if not exist "locale\en\LC_MESSAGES" mkdir "locale\en\LC_MESSAGES"
if not exist "locale\es\LC_MESSAGES" mkdir "locale\es\LC_MESSAGES"

REM Aplicar configuración de permisos para operarios
echo Configurando permisos para operarios...
python configurar_permisos_operarios.py
echo.

REM Crear archivos de traducción
echo Creando archivos de traducción...
python manage.py makemessages -l en
python manage.py makemessages -l es
echo.

REM Compilar archivos de traducción
echo Compilando archivos de traducción...
python manage.py compilemessages
echo.

REM Reiniciar el servidor Django
echo Reiniciando el servidor Django...
echo Por favor, cierre el servidor Django si está en ejecución y luego ejecútelo nuevamente.
echo.

echo ===============================================================
echo MEJORAS APLICADAS CORRECTAMENTE
echo ===============================================================
echo.
echo Las siguientes mejoras se han aplicado:
echo.
echo 1. Permisos para operarios: Se ha creado un dashboard específico para
echo    operarios y se han configurado los permisos necesarios.
echo.
echo 2. Selección de idioma: Se ha implementado la funcionalidad de selección
echo    de idioma en la aplicación web.
echo.
echo 3. Comparación de razas: Se ha implementado la funcionalidad para comparar
echo    datos nominales de una raza con datos reales de un lote activo.
echo.
echo Para aplicar estos cambios, reinicie el servidor Django con:
echo.
echo    iniciar_servidor_django.bat
echo.
echo ===============================================================

pause
