import os
import django

def create_consumo_energia_table():
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
    django.setup()
    
    from django.db import connection
    from django.db.utils import ProgrammingError
    
    print("Creating tables for ConsumoEnergia model...")
    
    # SQL to create the table
    sql = """
    CREATE TABLE IF NOT EXISTS produccion_consumoenergia (
        id SERIAL PRIMARY KEY,
        galpon_id INTEGER NOT NULL REFERENCES produccion_galpon(id) DEFERRABLE INITIALLY DEFERRED,
        fecha_registro DATE NOT NULL,
        hora_inicio TIME NOT NULL,
        hora_fin TIME NOT NULL,
        consumo_kwh NUMERIC(10, 2) NOT NULL,
        temperatura_ambiente NUMERIC(5, 2),
        humedad_relativa NUMERIC(5, 2),
        observaciones TEXT,
        registrado_por_id INTEGER REFERENCES avicola_userprofile(id) DEFERRABLE INITIALLY DEFERRED,
        fecha_creacion TIMESTAMP WITH TIME ZONE NOT NULL,
        fecha_actualizacion TIMESTAMP WITH TIME ZONE NOT NULL,
        costo_por_kwh NUMERIC(10, 4) DEFAULT 0,
        horas_funcionamiento INTEGER,
        temperatura_externa NUMERIC(5, 2)
    );
    
    -- Create the unique constraint
    CREATE UNIQUE INDEX IF NOT EXISTS produccion_consumoenergia_galpon_id_fecha_regis_1a9c0c5e_uniq 
    ON produccion_consumoenergia (galpon_id, fecha_registro, hora_inicio, hora_fin);
    
    -- Create the index on galpon_id
    CREATE INDEX IF NOT EXISTS produccion_consumoenergia_galpon_id_1a9c0c5e 
    ON produccion_consumoenergia (galpon_id);
    
    -- Create the index on registrado_por_id
    CREATE INDEX IF NOT EXISTS produccion_consumoenergia_registrado_por_id_1a9c0c5e 
    ON produccion_consumoenergia (registrado_por_id);
    """
    
    try:
        with connection.cursor() as cursor:
            # Split the SQL into individual statements and execute them one by one
            for statement in sql.split(';'):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)
        
        print('Successfully created tables for ConsumoEnergia model')
        return True
    except ProgrammingError as e:
        print(f'Error creating tables: {str(e)}')
        return False

if __name__ == "__main__":
    create_consumo_energia_table()
