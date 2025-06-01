@echo off
REM Script para ejecutar el sistema de respaldo de App_Granja
REM Este archivo puede ser programado en el Programador de tareas de Windows

echo Iniciando respaldo de App_Granja - %date% %time%
cd /d "%~dp0"
call .\venv\Scripts\python.exe backup_system.py --backup-all --notify
echo Respaldo completado - %date% %time%
