import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from database import Database

def test_database_connection():
    """Test the database connection and show results in a message box"""
    app = QApplication(sys.argv)
    
    try:
        # Initialize database connection
        db = Database()
        session = db.get_session()
        
        # Test connection by querying a table
        # Try to get the list of tables first
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if tables:
            # Try to get row count from the first table as a test
            first_table = tables[0]
            result = session.execute(f"SELECT COUNT(*) FROM {first_table}")
            row_count = result.scalar()
            
            # Show success message
            msg = (
                "✅ Conexión exitosa a la base de datos!\n\n"
                f"📊 Tablas encontradas: {len(tables)}\n"
                f"📋 Primera tabla: {first_table}\n"
                f"📈 Filas en {first_table}: {row_count}"
            )
            QMessageBox.information(None, "Prueba de conexión exitosa", msg)
            return True
        else:
            QMessageBox.warning(None, "Advertencia", "La base de datos no contiene tablas.")
            return False
            
    except Exception as e:
        # Show error message
        error_msg = (
            "❌ Error al conectar a la base de datos\n\n"
            f"Error: {str(e)}\n\n"
            "Por favor verifica que:\n"
            "1. PostgreSQL esté en ejecución\n"
            "2. Las credenciales en el archivo .env sean correctas\n"
            "3. La base de datos exista y sea accesible"
        )
        QMessageBox.critical(None, "Error de conexión", error_msg)
        return False
    finally:
        try:
            session.close()
            db.close()
        except:
            pass
        
        # Don't exit immediately, let the user read the message
        app.exec()

if __name__ == "__main__":
    test_database_connection()
