from database import Database
from sqlalchemy import text

def setup_triggers():
    db = Database()
    with db.engine.connect() as conn:
        # Create the notification function if it doesn't exist
        conn.execute(text("""
        CREATE OR REPLACE FUNCTION notify_data_change()
        RETURNS TRIGGER AS $$
        DECLARE
            notification json;
            record_data json;
            operation text;
            table_name text;
            record_id bigint;
        BEGIN
            IF (TG_OP = 'DELETE') THEN
                operation := 'DELETE';
                record_data := row_to_json(OLD);
                record_id := OLD.id;
            ELSIF (TG_OP = 'UPDATE') THEN
                operation := 'UPDATE';
                record_data := row_to_json(NEW);
                record_id := NEW.id;
            ELSIF (TG_OP = 'INSERT') THEN
                operation := 'INSERT';
                record_data := row_to_json(NEW);
                record_id := NEW.id;
            END IF;
            
            table_name := TG_TABLE_SCHEMA || '.' || TG_TABLE_NAME;
            
            notification := json_build_object(
                'operation', operation,
                'table', table_name,
                'id', record_id,
                'data', record_data,
                'timestamp', CURRENT_TIMESTAMP
            );
            
            PERFORM pg_notify('data_change', notification::text);
            
            IF (TG_OP = 'DELETE') THEN
                RETURN OLD;
            ELSE
                RETURN NEW;
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """))

        # List of tables to create triggers for
        tables = [
            'produccion_galpon',
            'produccion_granja',
            'ventas_cliente',
            'inventario_alimento',
            'inventario_raza',
            'inventario_vacuna',
            'avicola_userprofile'
        ]

        # Create triggers for each table
        for table in tables:
            trigger_name = f"notify_{table}_change"
            conn.execute(text(f"""
            DROP TRIGGER IF EXISTS {trigger_name} ON {table};
            CREATE TRIGGER {trigger_name}
            AFTER INSERT OR UPDATE OR DELETE ON {table}
            FOR EACH ROW EXECUTE FUNCTION notify_data_change();
            """))
        
        conn.commit()
    
    print("Triggers set up successfully!")

if __name__ == "__main__":
    setup_triggers()