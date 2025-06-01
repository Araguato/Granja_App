import json
import logging
import threading
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from database import Database

class DatabaseListener:
    def __init__(self, db_config, callback=None):
        self.db_config = db_config
        self.callback = callback
        self.connection = None
        self.running = False
        self.thread = None
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger('DatabaseListener')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def start(self):
        """Inicia el listener en un hilo separado"""
        if self.running:
            self.logger.warning("El listener ya está en ejecución")
            return

        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.daemon = True
        self.thread.start()
        self.logger.info("Listener de base de datos iniciado")

    def stop(self):
        """Detiene el listener"""
        self.running = False
        if self.connection and not self.connection.closed:
            self.connection.close()
        if self.thread:
            self.thread.join(timeout=1)
        self.logger.info("Listener de base de datos detenido")

    def _listen(self):
        """Método principal que escucha las notificaciones"""
        while self.running:
            try:
                if not self.connection or self.connection.closed:
                    self._connect()

                self.connection.poll()
                while self.connection.notifies:
                    notify = self.connection.notifies.pop(0)
                    self._handle_notification(notify)

            except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
                self.logger.error(f"Error de conexión: {str(e)}")
                self._reconnect()
            except Exception as e:
                self.logger.error(f"Error inesperado: {str(e)}")
                self._reconnect()

    def _connect(self):
        """Establece la conexión a la base de datos"""
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()

            self.connection = psycopg2.connect(**self.db_config)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            
            with self.connection.cursor() as cursor:
                cursor.execute("LISTEN data_change;")
            
            self.logger.info("Conexión a la base de datos establecida")

        except Exception as e:
            self.logger.error(f"Error al conectar a la base de datos: {str(e)}")
            raise

    def _reconnect(self, max_retries=3, delay=5):
        """Intenta reconectarse a la base de datos"""
        import time
        for attempt in range(max_retries):
            try:
                self.logger.info(f"Intentando reconectar... Intento {attempt + 1}/{max_retries}")
                self._connect()
                return True
            except Exception as e:
                self.logger.error(f"Error en el intento {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
        return False

    def _handle_notification(self, notification):
        """Procesa una notificación recibida"""
        try:
            data = json.loads(notification.payload)
            self.logger.info(f"Notificación recibida: {data}")
            
            if self.callback:
                self.callback(data)

        except json.JSONDecodeError:
            self.logger.error(f"No se pudo decodificar la notificación: {notification.payload}")
        except Exception as e:
            self.logger.error(f"Error al procesar la notificación: {str(e)}")

def example_callback(data):
    """Función de ejemplo para manejar las notificaciones"""
    print(f"\n¡Cambio detectado!")
    print(f"Tabla: {data.get('table')}")
    print(f"Operación: {data.get('operation')}")
    print(f"ID del registro: {data.get('id')}")
    print(f"Timestamp: {data.get('timestamp')}")
    print("Datos completos:", data.get('data'))
    print("-" * 50)

if __name__ == "__main__":
    # Configuración de ejemplo
    from database import Database
    db = Database()
    
    # Crear e iniciar el listener
    listener = DatabaseListener(db.db_config, callback=example_callback)
    listener.start()
    
    try:
        # Mantener el script en ejecución
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDeteniendo el listener...")
        listener.stop()