@echo off
echo ===================================================
echo    DIAGNÓSTICO Y REPARACIÓN DE POSTGRESQL
echo ===================================================
echo.

REM Verificar si PostgreSQL está instalado
where psql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PostgreSQL no está instalado o no está en el PATH.
    echo Instala PostgreSQL desde: https://www.postgresql.org/download/windows/
    echo.
    echo O si ya está instalado, asegúrate de que esté en el PATH del sistema.
    goto :end
) else (
    echo [OK] PostgreSQL está instalado.
)

echo.
echo Verificando servicio de PostgreSQL...
sc query postgresql-x64-15 | findstr "RUNNING" >nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] El servicio de PostgreSQL no está en ejecución.
    echo.
    echo Intentando iniciar el servicio...
    net start postgresql-x64-15
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] No se pudo iniciar el servicio. Intenta iniciarlo manualmente.
        echo 1. Abre el Panel de Control
        echo 2. Ve a Herramientas Administrativas -^> Servicios
        echo 3. Busca el servicio de PostgreSQL y haz clic en "Iniciar"
    ) else (
        echo [OK] Servicio de PostgreSQL iniciado correctamente.
    )
) else (
    echo [OK] El servicio de PostgreSQL está en ejecución.
)

echo.
echo Verificando la base de datos y el usuario...
echo.

REM Activar el entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo No se encontró el entorno virtual en venv\Scripts\activate.bat
    echo Intentando continuar sin activar el entorno virtual...
)

REM Crear un script SQL temporal
echo \set ON_ERROR_STOP on > temp_script.sql
echo -- Verificar si el usuario existe >> temp_script.sql
echo \echo 'Verificando usuario usuario_avicola...' >> temp_script.sql
echo SELECT 1 FROM pg_roles WHERE rolname='usuario_avicola'; >> temp_script.sql
echo -- Verificar si la base de datos existe >> temp_script.sql
echo \echo 'Verificando base de datos DB_Avicola...' >> temp_script.sql
echo SELECT 1 FROM pg_database WHERE datname='DB_Avicola'; >> temp_script.sql

REM Ejecutar el script como superusuario postgres
echo Ejecutando verificaciones como usuario postgres...
psql -U postgres -f temp_script.sql

echo.
echo ¿Deseas crear el usuario y la base de datos si no existen? (S/N)
set /p crear=

if /i "%crear%"=="S" (
    echo Creando usuario y base de datos si no existen...
    
    echo \set ON_ERROR_STOP on > create_script.sql
    echo -- Crear usuario si no existe >> create_script.sql
    echo DO $$ >> create_script.sql
    echo BEGIN >> create_script.sql
    echo   IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname='usuario_avicola') THEN >> create_script.sql
    echo     CREATE USER usuario_avicola WITH PASSWORD 'Aves2025'; >> create_script.sql
    echo   END IF; >> create_script.sql
    echo END $$; >> create_script.sql
    
    echo -- Crear base de datos si no existe >> create_script.sql
    echo DO $$ >> create_script.sql
    echo BEGIN >> create_script.sql
    echo   IF NOT EXISTS (SELECT FROM pg_database WHERE datname='DB_Avicola') THEN >> create_script.sql
    echo     CREATE DATABASE "DB_Avicola" WITH OWNER = usuario_avicola; >> create_script.sql
    echo   END IF; >> create_script.sql
    echo END $$; >> create_script.sql
    
    echo -- Asignar permisos >> create_script.sql
    echo GRANT ALL PRIVILEGES ON DATABASE "DB_Avicola" TO usuario_avicola; >> create_script.sql
    
    REM Ejecutar el script como superusuario postgres
    psql -U postgres -f create_script.sql
    
    echo.
    echo Base de datos y usuario configurados. Ahora aplicaremos las migraciones...
    python manage.py migrate
)

echo.
echo ¿Deseas iniciar el servidor Django? (S/N)
set /p iniciar=

if /i "%iniciar%"=="S" (
    echo Iniciando el servidor Django...
    python manage.py runserver 0.0.0.0:8000
)

:end
echo.
echo Presiona cualquier tecla para salir...
pause > nul
del temp_script.sql 2>nul
del create_script.sql 2>nul
