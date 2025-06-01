import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import json
from PyQt6.QtCore import QObject, pyqtSignal
import logging

class DatabaseListener(QObject):
    """Listens for database changes using PostgreSQL's LISTEN/NOTIFY"""
    
    # Signal emitted when data changes
    data_changed = pyqtSignal(str, dict)  # table_name, change_data
    
    def __init__(self, db_config):
        super().__init__()
        self.db_config = db_config
        self.conn = None
        self.running = False
        self.logger = logging.getLogger(__name__)
        
    def start_listening(self):
        """Start listening for database changes"""
        try:
            # Connect to the database
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.conn.cursor()
            
            # Listen for notifications
            self.cursor.execute("LISTEN data_change;")
            self.running = True
            self.logger.info("Database listener started")
            
            # Start listening in a separate thread
            from threading import Thread
            self.thread = Thread(target=self._listen, daemon=True)
            self.thread.start()
            
        except Exception as e:
            self.logger.error(f"Error starting database listener: {e}")
            raise
    
    def stop_listening(self):
        """Stop listening for database changes"""
        self.running = False
        if self.conn:
            self.conn.close()
        self.logger.info("Database listener stopped")
    
    def _listen(self):
        """Internal method to listen for notifications"""
        while self.running and self.conn:
            try:
                self.conn.poll()
                while self.conn.notifies:
                    notify = self.conn.notifies.pop(0)
                    try:
                        change_data = json.loads(notify.payload)
                        table_name = change_data.get('table')
                        if table_name:
                            self.data_changed.emit(table_name, change_data)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Error decoding notification: {e}")
                
                # Small sleep to prevent high CPU usage
                import time
                time.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Error in database listener: {e}")
                if self.conn:
                    self.conn.close()
                    self.conn = None
                # Try to reconnect after a delay
                time.sleep(5)
                if self.running:
                    try:
                        self.conn = psycopg2.connect(**self.db_config)
                        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                        self.cursor = self.conn.cursor()
                        self.cursor.execute("LISTEN data_change;")
                    except Exception as e:
                        self.logger.error(f"Error reconnecting to database: {e}")

# Example usage:
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    def on_data_changed(table_name, data):
        print(f"Data changed in {table_name}: {data}")
    
    app = QApplication(sys.argv)
    
    # Example database configuration
    db_config = {
        'dbname': 'DB_Avicola',
        'user': 'usuario_avicola',
        'password': 'Aves2025',
        'host': 'localhost',
        'port': '5432'
    }
    
    listener = DatabaseListener(db_config)
    listener.data_changed.connect(on_data_changed)
    listener.start_listening()
    
    print("Listening for database changes. Press Ctrl+C to exit.")
    
    sys.exit(app.exec())
