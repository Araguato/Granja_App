import json
import logging
from datetime import datetime, timezone
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

class SyncService(QObject):
    """Handles data synchronization between the Windows app and the web app"""
    
    # Signal emitted when synchronization completes
    sync_completed = pyqtSignal(str, bool, str)  # table_name, success, message
    
    def __init__(self, db_engine):
        super().__init__()
        self.db_engine = db_engine
        self.Session = sessionmaker(bind=db_engine)
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        load_dotenv()
        
        # Initialize last sync time
        self.last_sync = {}
        
        # Setup periodic sync
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self.sync_all_tables)
        self.set_sync_interval(300)  # Default: 5 minutes
    
    def set_sync_interval(self, seconds):
        """Set the sync interval in seconds"""
        self.sync_timer.stop()
        if seconds > 0:
            self.sync_timer.start(seconds * 1000)  # Convert to milliseconds
    
    def sync_all_tables(self):
        """Synchronize all tables that have changed since last sync"""
        try:
            inspector = self.db_engine.dialect.get_inspector(self.db_engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                if table.startswith(('django_', 'auth_')):
                    continue  # Skip Django system tables
                self.sync_table(table)
                
            self.logger.info("Completed full synchronization")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during full synchronization: {e}")
            return False
    
    def sync_table(self, table_name):
        """Synchronize a specific table"""
        try:
            last_sync = self.last_sync.get(table_name, datetime.min.replace(tzinfo=timezone.utc))
            
            with self.Session() as session:
                # Get changes since last sync
                # Note: This assumes each table has 'created_at' and 'updated_at' timestamps
                query = f"""
                    SELECT * FROM {table_name}
                    WHERE updated_at > :last_sync
                    OR created_at > :last_sync
                """
                
                result = session.execute(text(query), {'last_sync': last_sync})
                changes = [dict(row._mapping) for row in result]
                
                if changes:
                    self.logger.info(f"Found {len(changes)} changes in {table_name}")
                    
                    # Process changes (in a real app, you might want to update the UI here)
                    for change in changes:
                        self._process_change(table_name, change)
                    
                    # Update last sync time
                    self.last_sync[table_name] = datetime.now(timezone.utc)
                    
                    self.sync_completed.emit(table_name, True, f"Synced {len(changes)} rows")
                    return True
                
                return False
                
        except Exception as e:
            error_msg = f"Error syncing table {table_name}: {e}"
            self.logger.error(error_msg)
            self.sync_completed.emit(table_name, False, error_msg)
            return False
    
    def _process_change(self, table_name, change_data):
        """Process a single change from the database"""
        # In a real app, you would update your local data store or UI here
        self.logger.debug(f"Processing change in {table_name}: {change_data}")
        
        # Example: Update a local SQLite cache or notify UI components
        # This is where you'd implement your specific synchronization logic
        
    # Methods for handling offline changes
    def queue_local_change(self, table_name, action, data):
        """Queue a local change to be synced with the server"""
        # In a real app, you would store this in a local queue or database
        # and process it when online
        self.logger.info(f"Queued {action} for {table_name}: {data}")
        
    def process_offline_queue(self):
        """Process any queued offline changes"""
        # In a real app, you would process any queued changes here
        pass

# Example usage:
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    def on_sync_completed(table_name, success, message):
        status = "succeeded" if success else "failed"
        print(f"Sync {status} for {table_name}: {message}")
    
    app = QApplication(sys.argv)
    
    # Example database configuration
    db_url = "postgresql://usuario_avicola:Aves2025@localhost:5432/DB_Avicola"
    engine = create_engine(db_url)
    
    # Create and start sync service
    sync_service = SyncService(engine)
    sync_service.sync_completed.connect(on_sync_completed)
    
    # Perform initial sync
    sync_service.sync_all_tables()
    
    sys.exit(app.exec())
