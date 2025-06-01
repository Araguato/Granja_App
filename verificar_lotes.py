import os
import sys
import django
from django.db import connection

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

# Importar los modelos después de configurar Django
from produccion.models import Lote, Galpon
from inventario.models import Raza
from django.contrib.auth import get_user_model
from django.utils import timezone

UserProfile = get_user_model()

def verificar_tablas():
    """Verifica si las tablas necesarias existen en la base de datos"""
    print("Verificando tablas en la base de datos...")
    
    with connection.cursor() as cursor:
        # Verificar tabla de lotes
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'produccion_lote'
            );
        """)
        existe_lote = cursor.fetchone()[0]
        
        # Verificar tabla de galpones
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'produccion_galpon'
            );
        """)
        existe_galpon = cursor.fetchone()[0]
        
        # Verificar tabla de razas
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'inventario_raza'
            );
        """)
        existe_raza = cursor.fetchone()[0]
    
    print(f"Tabla 'produccion_lote': {'Existe' if existe_lote else 'No existe'}")
    print(f"Tabla 'produccion_galpon': {'Existe' if existe_galpon else 'No existe'}")
    print(f"Tabla 'inventario_raza': {'Existe' if existe_raza else 'No existe'}")
    
    return existe_lote and existe_galpon and existe_raza

def verificar_registros():
    """Verifica si hay registros en las tablas principales"""
    print("\nVerificando registros existentes...")
    
    try:
        num_lotes = Lote.objects.count()
        print(f"Lotes: {num_lotes}")
        
        if num_lotes > 0:
            print("\nLotes existentes:")
            for lote in Lote.objects.all():
                print(f"  - ID: {lote.id}, Código: {getattr(lote, 'codigo', 'N/A')}, Galpón: {getattr(lote.galpon, 'numero', 'N/A')}, Raza: {getattr(lote.raza, 'nombre', 'N/A')}")
    except Exception as e:
        print(f"Error al verificar lotes: {e}")
    
    try:
        num_galpones = Galpon.objects.count()
        print(f"Galpones: {num_galpones}")
        
        if num_galpones > 0:
            print("\nGalpones existentes:")
            for galpon in Galpon.objects.all():
                print(f"  - ID: {galpon.id}, Número: {getattr(galpon, 'numero', 'N/A')}")
    except Exception as e:
        print(f"Error al verificar galpones: {e}")
    
    try:
        num_razas = Raza.objects.count()
        print(f"Razas: {num_razas}")
        
        if num_razas > 0:
            print("\nRazas existentes:")
            for raza in Raza.objects.all():
                print(f"  - ID: {raza.id}, Nombre: {getattr(raza, 'nombre', 'N/A')}")
    except Exception as e:
        print(f"Error al verificar razas: {e}")
    
    return {
        'lotes': num_lotes if 'num_lotes' in locals() else 0,
        'galpones': num_galpones if 'num_galpones' in locals() else 0,
        'razas': num_razas if 'num_razas' in locals() else 0
    }

def crear_datos_prueba():
    """Crea datos de prueba si no existen registros"""
    print("\n¿Deseas crear datos de prueba? (S/N)")
    respuesta = input().strip().upper()
    
    if respuesta != 'S':
        print("No se crearán datos de prueba.")
        return
    
    print("\nCreando datos de prueba...")
    
    try:
        # Verificar si hay un usuario administrador
        try:
            admin = UserProfile.objects.filter(is_superuser=True).first()
            if not admin:
                print("Creando usuario administrador...")
                admin = UserProfile.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                print(f"Usuario administrador creado: {admin.username}")
            else:
                print(f"Usando usuario administrador existente: {admin.username}")
        except Exception as e:
            print(f"Error al crear/obtener usuario administrador: {e}")
            admin = None
        
        # Crear razas si no existen
        razas_count = Raza.objects.count()
        if razas_count == 0:
            print("Creando razas...")
            razas = [
                {'nombre': 'COBB 500', 'descripcion': 'Pollo de engorde de rápido crecimiento'},
                {'nombre': 'Ross 308', 'descripcion': 'Pollo de engorde con buena conversión alimenticia'},
                {'nombre': 'Hy-Line Brown', 'descripcion': 'Gallina ponedora de huevos marrones'},
                {'nombre': 'Isa Brown', 'descripcion': 'Gallina ponedora de alta producción'}
            ]
            
            for raza_data in razas:
                raza = Raza.objects.create(**raza_data)
                print(f"  - Raza creada: {raza.nombre}")
        else:
            print(f"Ya existen {razas_count} razas, no se crearán nuevas.")
        
        # Crear galpones si no existen
        galpones_count = Galpon.objects.count()
        if galpones_count == 0:
            print("Creando galpones...")
            
            # Verificar si el modelo Galpon tiene los campos esperados
            galpon_fields = [f.name for f in Galpon._meta.get_fields()]
            print(f"Campos disponibles en el modelo Galpon: {galpon_fields}")
            
            # Crear galpones con los campos disponibles
            galpon_data = {
                'numero': 'G001',
                'capacidad': 2000
            }
            
            # Agregar campos opcionales si existen en el modelo
            if 'tipo' in galpon_fields:
                galpon_data['tipo'] = 'PRODUCCION'
            
            if 'encargado' in galpon_fields and admin:
                galpon_data['encargado'] = admin
            
            galpon = Galpon.objects.create(**galpon_data)
            print(f"  - Galpón creado: {galpon.numero}")
            
            # Crear un segundo galpón
            galpon_data['numero'] = 'G002'
            galpon2 = Galpon.objects.create(**galpon_data)
            print(f"  - Galpón creado: {galpon2.numero}")
        else:
            print(f"Ya existen {galpones_count} galpones, no se crearán nuevos.")
        
        # Crear lotes si no existen
        lotes_count = Lote.objects.count()
        if lotes_count == 0:
            print("Creando lotes...")
            
            # Obtener galpones y razas
            galpones = Galpon.objects.all()
            razas = Raza.objects.all()
            
            if galpones.exists() and razas.exists():
                # Verificar si el modelo Lote tiene los campos esperados
                lote_fields = [f.name for f in Lote._meta.get_fields()]
                print(f"Campos disponibles en el modelo Lote: {lote_fields}")
                
                # Crear lotes con los campos disponibles
                lote_data = {
                    'galpon': galpones.first(),
                    'raza': razas.first(),
                    'fecha_inicio': timezone.now().date(),
                    'cantidad_inicial_aves': 1000
                }
                
                # Agregar campos opcionales si existen en el modelo
                if 'codigo' in lote_fields:
                    lote_data['codigo'] = 'L001'
                
                if 'estado' in lote_fields:
                    lote_data['estado'] = 'CRECIMIENTO'
                
                lote = Lote.objects.create(**lote_data)
                print(f"  - Lote creado: {getattr(lote, 'codigo', 'ID: ' + str(lote.id))}")
                
                # Crear un segundo lote
                if len(galpones) > 1 and len(razas) > 1:
                    lote_data['galpon'] = galpones[1]
                    lote_data['raza'] = razas[1]
                    if 'codigo' in lote_fields:
                        lote_data['codigo'] = 'L002'
                    lote2 = Lote.objects.create(**lote_data)
                    print(f"  - Lote creado: {getattr(lote2, 'codigo', 'ID: ' + str(lote2.id))}")
            else:
                print("No se pueden crear lotes porque no hay galpones o razas disponibles.")
        else:
            print(f"Ya existen {lotes_count} lotes, no se crearán nuevos.")
        
        print("\nDatos de prueba creados correctamente.")
    except Exception as e:
        print(f"Error al crear datos de prueba: {e}")

def main():
    print("===================================================")
    print("    VERIFICACIÓN DE DATOS EN LA BASE DE DATOS")
    print("===================================================")
    
    # Verificar si las tablas existen
    tablas_existen = verificar_tablas()
    
    if not tablas_existen:
        print("\n[ADVERTENCIA] No todas las tablas necesarias existen en la base de datos.")
        print("Esto puede indicar que las migraciones no se han aplicado correctamente.")
        
        print("\n¿Deseas aplicar las migraciones? (S/N)")
        respuesta = input().strip().upper()
        
        if respuesta == 'S':
            print("\nAplicando migraciones...")
            try:
                from django.core.management import execute_from_command_line
                execute_from_command_line(['manage.py', 'migrate'])
                print("[OK] Migraciones aplicadas correctamente.")
                
                # Verificar tablas nuevamente
                tablas_existen = verificar_tablas()
                if not tablas_existen:
                    print("[ERROR] Algunas tablas siguen sin existir después de aplicar las migraciones.")
                    print("Esto puede indicar un problema con los modelos o las migraciones.")
                    return
            except Exception as e:
                print(f"[ERROR] No se pudieron aplicar las migraciones: {e}")
                return
    
    # Verificar si hay registros
    registros = verificar_registros()
    
    # Si no hay registros, ofrecer crear datos de prueba
    if registros['lotes'] == 0 or registros['galpones'] == 0 or registros['razas'] == 0:
        crear_datos_prueba()
    else:
        print("\nYa existen datos en la base de datos. No es necesario crear datos de prueba.")
    
    print("\nVerificación completada.")

if __name__ == "__main__":
    main()
