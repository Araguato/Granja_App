#!/usr/bin/env python
"""
Sistema de respaldo para App_Granja
-----------------------------------
Este script realiza respaldos completos de:
1. Base de datos PostgreSQL
2. Archivos de medios
3. Configuraciones importantes

Uso:
    python backup_system.py [opciones]

Opciones:
    --backup-db       Respaldar solo la base de datos
    --backup-media    Respaldar solo los archivos de medios
    --backup-all      Respaldar todo (por defecto)
    --restore=FILE    Restaurar desde un archivo de respaldo
    --list            Listar respaldos disponibles
    --encrypt         Cifrar el respaldo (requiere contraseña)
    --notify          Enviar notificación por correo al completar
"""

import os
import sys
import time
import shutil
import argparse
import subprocess
import logging
import json
import zipfile
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("backups/backup.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("backup_system")

# Configuración
BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backups"
MEDIA_DIR = BASE_DIR / "media"
CONFIG_FILE = BASE_DIR / "backup_config.json"

# Asegurarse de que el directorio de respaldos existe
if not BACKUP_DIR.exists():
    BACKUP_DIR.mkdir(parents=True)
    logger.info(f"Directorio de respaldos creado: {BACKUP_DIR}")

# Cargar configuración
def load_config():
    """Cargar configuración desde el archivo JSON"""
    if not CONFIG_FILE.exists():
        # Configuración por defecto
        config = {
            "db_settings": {
                "name": "granja_db",
                "user": "postgres",
                "password": "",
                "host": "localhost",
                "port": "5432"
            },
            "backup_settings": {
                "max_backups": 10,
                "compress": True,
                "encrypt": False,
                "encrypt_password": "",
                "include_media": True
            },
            "notification_settings": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "smtp_user": "",
                "smtp_password": "",
                "recipients": []
            }
        }
        
        # Guardar configuración por defecto
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        
        logger.info(f"Archivo de configuración creado: {CONFIG_FILE}")
        return config
    
    # Cargar configuración existente
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Función para respaldar la base de datos
def backup_database(config):
    """Respaldar la base de datos PostgreSQL"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        db_settings = config["db_settings"]
        backup_file = BACKUP_DIR / f"db_backup_{timestamp}.sql"
        
        # Configurar variables de entorno para pg_dump
        env = os.environ.copy()
        if db_settings["password"]:
            env["PGPASSWORD"] = db_settings["password"]
        
        # Comando pg_dump
        cmd = [
            "pg_dump",
            "-h", db_settings["host"],
            "-p", db_settings["port"],
            "-U", db_settings["user"],
            "-d", db_settings["name"],
            "-f", str(backup_file),
            "--verbose"
        ]
        
        logger.info(f"Iniciando respaldo de base de datos: {db_settings['name']}")
        process = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if process.returncode != 0:
            logger.error(f"Error al respaldar la base de datos: {process.stderr}")
            return None
        
        logger.info(f"Respaldo de base de datos completado: {backup_file}")
        return backup_file
    
    except Exception as e:
        logger.error(f"Error al respaldar la base de datos: {str(e)}")
        return None

# Función para respaldar archivos de medios
def backup_media(config):
    """Respaldar archivos de medios"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = BACKUP_DIR / f"media_backup_{timestamp}.zip"
        
        if not MEDIA_DIR.exists():
            logger.warning(f"Directorio de medios no encontrado: {MEDIA_DIR}")
            return None
        
        logger.info(f"Iniciando respaldo de archivos de medios desde: {MEDIA_DIR}")
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(MEDIA_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, BASE_DIR)
                    zipf.write(file_path, arcname)
        
        logger.info(f"Respaldo de archivos de medios completado: {backup_file}")
        return backup_file
    
    except Exception as e:
        logger.error(f"Error al respaldar archivos de medios: {str(e)}")
        return None

# Función para crear un respaldo completo
def create_full_backup(config):
    """Crear un respaldo completo (DB + medios)"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"full_backup_{timestamp}.zip"
    
    logger.info("Iniciando respaldo completo")
    
    # Respaldo temporal de la base de datos
    db_backup = backup_database(config)
    
    # Crear archivo ZIP con todos los respaldos
    with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Incluir respaldo de base de datos
        if db_backup:
            arcname = os.path.basename(db_backup)
            zipf.write(db_backup, arcname)
        
        # Incluir archivos de medios si está configurado
        if config["backup_settings"]["include_media"]:
            for root, _, files in os.walk(MEDIA_DIR):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.join("media", os.path.relpath(file_path, MEDIA_DIR))
                    zipf.write(file_path, arcname)
        
        # Incluir archivo de configuración
        zipf.write(CONFIG_FILE, os.path.basename(CONFIG_FILE))
    
    # Eliminar archivo temporal de respaldo de base de datos
    if db_backup and os.path.exists(db_backup):
        os.remove(db_backup)
    
    logger.info(f"Respaldo completo creado: {backup_file}")
    
    # Rotar respaldos antiguos
    rotate_backups(config)
    
    return backup_file

# Función para rotar respaldos antiguos
def rotate_backups(config):
    """Eliminar respaldos antiguos según la configuración"""
    max_backups = config["backup_settings"]["max_backups"]
    
    # Listar todos los respaldos completos
    full_backups = sorted(
        [f for f in BACKUP_DIR.glob("full_backup_*.zip")],
        key=os.path.getmtime
    )
    
    # Eliminar respaldos antiguos si hay más del máximo configurado
    if len(full_backups) > max_backups:
        for backup in full_backups[:-max_backups]:
            os.remove(backup)
            logger.info(f"Respaldo antiguo eliminado: {backup}")

# Función para restaurar un respaldo
def restore_backup(backup_file, config):
    """Restaurar desde un archivo de respaldo"""
    if not os.path.exists(backup_file):
        logger.error(f"Archivo de respaldo no encontrado: {backup_file}")
        return False
    
    logger.info(f"Iniciando restauración desde: {backup_file}")
    
    # Directorio temporal para la extracción
    temp_dir = BACKUP_DIR / "temp_restore"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    try:
        # Extraer archivo de respaldo
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(temp_dir)
        
        # Restaurar base de datos
        db_backup = next(temp_dir.glob("db_backup_*.sql"), None)
        if db_backup:
            restore_database(db_backup, config)
        
        # Restaurar archivos de medios
        media_dir = temp_dir / "media"
        if media_dir.exists():
            if MEDIA_DIR.exists():
                shutil.rmtree(MEDIA_DIR)
            shutil.copytree(media_dir, MEDIA_DIR)
            logger.info("Archivos de medios restaurados")
        
        logger.info("Restauración completada con éxito")
        return True
    
    except Exception as e:
        logger.error(f"Error durante la restauración: {str(e)}")
        return False
    
    finally:
        # Limpiar directorio temporal
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

# Función para restaurar la base de datos
def restore_database(db_backup, config):
    """Restaurar la base de datos desde un archivo SQL"""
    db_settings = config["db_settings"]
    
    # Configurar variables de entorno para psql
    env = os.environ.copy()
    if db_settings["password"]:
        env["PGPASSWORD"] = db_settings["password"]
    
    # Comando psql para restaurar
    cmd = [
        "psql",
        "-h", db_settings["host"],
        "-p", db_settings["port"],
        "-U", db_settings["user"],
        "-d", db_settings["name"],
        "-f", str(db_backup)
    ]
    
    logger.info(f"Restaurando base de datos desde: {db_backup}")
    process = subprocess.run(cmd, env=env, capture_output=True, text=True)
    
    if process.returncode != 0:
        logger.error(f"Error al restaurar la base de datos: {process.stderr}")
        return False
    
    logger.info("Base de datos restaurada con éxito")
    return True

# Función para listar respaldos disponibles
def list_backups():
    """Listar todos los respaldos disponibles"""
    backups = []
    
    # Respaldos completos
    full_backups = sorted(
        [f for f in BACKUP_DIR.glob("full_backup_*.zip")],
        key=os.path.getmtime,
        reverse=True
    )
    
    # Respaldos de base de datos
    db_backups = sorted(
        [f for f in BACKUP_DIR.glob("db_backup_*.sql")],
        key=os.path.getmtime,
        reverse=True
    )
    
    # Respaldos de medios
    media_backups = sorted(
        [f for f in BACKUP_DIR.glob("media_backup_*.zip")],
        key=os.path.getmtime,
        reverse=True
    )
    
    # Mostrar respaldos
    print("\n=== RESPALDOS DISPONIBLES ===")
    
    print("\nRespaldos completos:")
    for i, backup in enumerate(full_backups):
        size = os.path.getsize(backup) / (1024 * 1024)  # Tamaño en MB
        date = datetime.datetime.fromtimestamp(os.path.getmtime(backup))
        print(f"{i+1}. {backup.name} - {date.strftime('%Y-%m-%d %H:%M:%S')} - {size:.2f} MB")
    
    print("\nRespaldos de base de datos:")
    for i, backup in enumerate(db_backups):
        size = os.path.getsize(backup) / (1024 * 1024)  # Tamaño en MB
        date = datetime.datetime.fromtimestamp(os.path.getmtime(backup))
        print(f"{i+1}. {backup.name} - {date.strftime('%Y-%m-%d %H:%M:%S')} - {size:.2f} MB")
    
    print("\nRespaldos de medios:")
    for i, backup in enumerate(media_backups):
        size = os.path.getsize(backup) / (1024 * 1024)  # Tamaño en MB
        date = datetime.datetime.fromtimestamp(os.path.getmtime(backup))
        print(f"{i+1}. {backup.name} - {date.strftime('%Y-%m-%d %H:%M:%S')} - {size:.2f} MB")
    
    return full_backups + db_backups + media_backups

# Función para enviar notificación por correo
def send_notification(backup_file, config):
    """Enviar notificación por correo sobre el respaldo"""
    if not config["notification_settings"]["enabled"]:
        return
    
    settings = config["notification_settings"]
    
    if not settings["smtp_user"] or not settings["recipients"]:
        logger.warning("Configuración de notificaciones incompleta")
        return
    
    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = settings["smtp_user"]
        msg['To'] = ", ".join(settings["recipients"])
        msg['Subject'] = f"Respaldo de App_Granja completado - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        # Cuerpo del mensaje
        body = f"""
        <html>
        <body>
            <h2>Respaldo de App_Granja completado</h2>
            <p>Se ha completado un respaldo del sistema con los siguientes detalles:</p>
            <ul>
                <li><strong>Archivo:</strong> {os.path.basename(backup_file)}</li>
                <li><strong>Tamaño:</strong> {os.path.getsize(backup_file) / (1024 * 1024):.2f} MB</li>
                <li><strong>Fecha:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>Este es un mensaje automático, por favor no responda a este correo.</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(body, 'html'))
        
        # Conectar al servidor SMTP
        server = smtplib.SMTP(settings["smtp_server"], settings["smtp_port"])
        server.starttls()
        server.login(settings["smtp_user"], settings["smtp_password"])
        
        # Enviar correo
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Notificación enviada a: {', '.join(settings['recipients'])}")
    
    except Exception as e:
        logger.error(f"Error al enviar notificación: {str(e)}")

# Función principal
def main():
    """Función principal del sistema de respaldo"""
    parser = argparse.ArgumentParser(description="Sistema de respaldo para App_Granja")
    parser.add_argument("--backup-db", action="store_true", help="Respaldar solo la base de datos")
    parser.add_argument("--backup-media", action="store_true", help="Respaldar solo los archivos de medios")
    parser.add_argument("--backup-all", action="store_true", help="Respaldar todo (por defecto)")
    parser.add_argument("--restore", help="Restaurar desde un archivo de respaldo")
    parser.add_argument("--list", action="store_true", help="Listar respaldos disponibles")
    parser.add_argument("--encrypt", action="store_true", help="Cifrar el respaldo (requiere contraseña)")
    parser.add_argument("--notify", action="store_true", help="Enviar notificación por correo al completar")
    
    args = parser.parse_args()
    config = load_config()
    
    # Actualizar configuración con argumentos de línea de comandos
    if args.encrypt:
        config["backup_settings"]["encrypt"] = True
    
    if args.notify:
        config["notification_settings"]["enabled"] = True
    
    # Ejecutar acción según argumentos
    if args.list:
        list_backups()
    elif args.restore:
        restore_backup(args.restore, config)
    elif args.backup_db:
        backup_file = backup_database(config)
        if args.notify and backup_file:
            send_notification(backup_file, config)
    elif args.backup_media:
        backup_file = backup_media(config)
        if args.notify and backup_file:
            send_notification(backup_file, config)
    else:  # Por defecto, hacer respaldo completo
        backup_file = create_full_backup(config)
        if args.notify and backup_file:
            send_notification(backup_file, config)

if __name__ == "__main__":
    main()
