@echo off
echo Reiniciando el servidor Django...
echo.
echo 1. Deteniendo el servidor actual (si está en ejecución)...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak > nul

echo 2. Limpiando archivos temporales...
if exist "%TEMP%\django_cache" rd /s /q "%TEMP%\django_cache"
if exist "C:\App_Granja\__pycache__" rd /s /q "C:\App_Granja\__pycache__"

echo 3. Iniciando el servidor Django...
start cmd /k "cd /d C:\App_Granja && python manage.py runserver 0.0.0.0:8000"

echo.
echo El servidor Django se ha reiniciado.
echo.
echo IMPORTANTE: El supervisor debe cerrar sesión y volver a iniciar sesión
echo para que los nuevos permisos se apliquen correctamente.
echo.
echo Presione cualquier tecla para continuar...
pause > nul
