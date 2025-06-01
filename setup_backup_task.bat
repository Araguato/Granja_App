@echo off
echo Configurando tarea programada para respaldos automáticos...

REM Obtener la ruta actual del proyecto
set PROJECT_PATH=%~dp0
set PROJECT_PATH=%PROJECT_PATH:~0,-1%

REM Crear la tarea programada
schtasks /create /tn "AppGranja_AutoBackup" /tr "cmd /c cd /d %PROJECT_PATH% && python manage.py run_auto_backup" /sc HOURLY /mo 6 /ru SYSTEM /f

if %ERRORLEVEL% EQU 0 (
    echo La tarea de respaldo automático se ha configurado correctamente.
    echo Se ejecutará cada 6 horas.
) else (
    echo Error al configurar la tarea de respaldo automático.
    echo Por favor, ejecute este script como administrador.
)

pause
