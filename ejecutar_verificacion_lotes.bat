@echo off
echo Ejecutando verificacion de lotes en la base de datos...

REM Activar el entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo No se encontro el entorno virtual en venv\Scripts\activate.bat
    echo Intentando continuar sin activar el entorno virtual...
)

REM Ejecutar el script de Python
python verificar_lotes.py

pause
