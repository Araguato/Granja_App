"""
Script para generar datos de prueba para la aplicación de gestión avícola.
"""

import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar modelos
from django.contrib.auth import get_user_model
from produccion.models import Granja, Galpon, Lote, SeguimientoDiario
from inventario.models import Proveedor, Raza, Alimento, Vacuna, Insumo

# Obtener el modelo de usuario personalizado
User = get_user_model()

def create_test_data():
    """
    Crea datos de prueba para todas las entidades principales del sistema.
    """
    print("Generando datos de prueba...")
    
    # Crear usuarios de prueba si no existen
    if User.objects.count() == 0:
        print("Creando usuarios de prueba...")
        admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        user1 = User.objects.create_user('operador1', 'operador1@example.com', 'password123')
        user2 = User.objects.create_user('supervisor1', 'supervisor1@example.com', 'password123')
        
        # Crear perfiles de usuario
        UserProfile.objects.create(user=admin, tipo_usuario='ADMINISTRADOR', telefono='1234567890')
        UserProfile.objects.create(user=user1, tipo_usuario='OPERADOR', telefono='0987654321')
        UserProfile.objects.create(user=user2, tipo_usuario='SUPERVISOR', telefono='5555555555')
        
        print(f"Creados {User.objects.count()} usuarios con sus perfiles")
    
    # Crear proveedores de prueba
    if Proveedor.objects.count() == 0:
        print("Creando proveedores de prueba...")
        proveedores = [
            {'rif': 'J-12345678-9', 'nombre': 'Avícola El Dorado', 'direccion': 'Calle 123, Ciudad', 'telefono': '1234567890', 'email': 'eldorado@example.com'},
            {'rif': 'J-87654321-0', 'nombre': 'Distribuidora Avícola Central', 'direccion': 'Av. Principal 456, Ciudad', 'telefono': '0987654321', 'email': 'central@example.com'},
            {'rif': 'J-55555555-5', 'nombre': 'Insumos Agrícolas S.A.', 'direccion': 'Carrera 78, Ciudad', 'telefono': '5555555555', 'email': 'insumos@example.com'},
        ]
        
        for p in proveedores:
            Proveedor.objects.create(**p)
        
        print(f"Creados {Proveedor.objects.count()} proveedores")
    
    # Crear razas de aves
    if Raza.objects.count() == 0:
        print("Creando razas de aves...")
        razas = [
            {'nombre': 'Hy-Line Brown', 'tipo': 'PONEDORA', 'descripcion': 'Gallina ponedora de huevos marrones'},
            {'nombre': 'Hy-Line W-36', 'tipo': 'PONEDORA', 'descripcion': 'Gallina ponedora de huevos blancos'},
            {'nombre': 'Ross 308', 'tipo': 'ENGORDE', 'descripcion': 'Pollo de engorde de rápido crecimiento'},
            {'nombre': 'Cobb 500', 'tipo': 'ENGORDE', 'descripcion': 'Pollo de engorde con buena conversión alimenticia'},
        ]
        
        for r in razas:
            Raza.objects.create(**r)
        
        print(f"Creadas {Raza.objects.count()} razas de aves")
    
    # Crear alimentos
    if Alimento.objects.count() == 0:
        print("Creando alimentos...")
        proveedor1 = Proveedor.objects.first()
        alimentos = [
            {'nombre': 'Iniciador', 'tipo_alimento': 'CONCENTRADO', 'descripcion': 'Alimento para pollitos de 0-4 semanas', 'proveedor': proveedor1, 'etapa': 'INICIADOR'},
            {'nombre': 'Crecimiento', 'tipo_alimento': 'CONCENTRADO', 'descripcion': 'Alimento para pollos de 5-10 semanas', 'proveedor': proveedor1, 'etapa': 'CRECIMIENTO'},
            {'nombre': 'Engorde', 'tipo_alimento': 'CONCENTRADO', 'descripcion': 'Alimento para pollos de engorde', 'proveedor': proveedor1, 'etapa': 'ENGORDE_FINALIZADOR'},
            {'nombre': 'Ponedoras', 'tipo_alimento': 'CONCENTRADO', 'descripcion': 'Alimento para gallinas ponedoras', 'proveedor': proveedor1, 'etapa': 'POSTURA_FASE1'},
        ]
        
        for a in alimentos:
            Alimento.objects.create(**a)
        
        print(f"Creados {Alimento.objects.count()} alimentos")
    
    # Crear vacunas
    if Vacuna.objects.count() == 0:
        print("Creando vacunas...")
        proveedor2 = Proveedor.objects.all()[1] if Proveedor.objects.count() > 1 else Proveedor.objects.first()
        vacunas = [
            {'nombre_comercial': 'Newcastle B1', 'tipo_vacuna': 'VIRAL', 'descripcion': 'Vacuna contra la enfermedad de Newcastle', 'proveedor': proveedor2},
            {'nombre_comercial': 'Bronquitis H120', 'tipo_vacuna': 'VIRAL', 'descripcion': 'Vacuna contra la bronquitis infecciosa', 'proveedor': proveedor2},
            {'nombre_comercial': 'Gumboro D78', 'tipo_vacuna': 'VIRAL', 'descripcion': 'Vacuna contra la enfermedad de Gumboro', 'proveedor': proveedor2},
            {'nombre_comercial': 'Marek HVT', 'tipo_vacuna': 'VIRAL', 'descripcion': 'Vacuna contra la enfermedad de Marek', 'proveedor': proveedor2},
        ]
        
        for v in vacunas:
            Vacuna.objects.create(**v)
        
        print(f"Creadas {Vacuna.objects.count()} vacunas")
    
    # Crear granjas
    if Granja.objects.count() == 0:
        print("Creando granjas...")
        granjas = [
            {'nombre': 'Granja Las Palmas', 'ubicacion': 'Km 15 vía a la Costa', 'capacidad_total': 10000},
            {'nombre': 'Granja El Paraíso', 'ubicacion': 'Km 20 vía a la Sierra', 'capacidad_total': 15000},
        ]
        
        for g in granjas:
            Granja.objects.create(**g)
        
        print(f"Creadas {Granja.objects.count()} granjas")
    
    # Crear galpones
    if Galpon.objects.count() == 0:
        print("Creando galpones...")
        for granja in Granja.objects.all():
            for i in range(1, 4):  # 3 galpones por granja
                Galpon.objects.create(
                    granja=granja,
                    nombre=f"Galpón {i}",
                    capacidad=granja.capacidad_total // 3,
                    tipo='PONEDORA' if i <= 2 else 'ENGORDE'
                )
        
        print(f"Creados {Galpon.objects.count()} galpones")
    
    # Crear lotes
    if Lote.objects.count() == 0:
        print("Creando lotes...")
        razas = list(Raza.objects.all())
        
        for galpon in Galpon.objects.all():
            fecha_ingreso = timezone.now() - timedelta(days=random.randint(30, 120))
            cantidad_inicial = galpon.capacidad - random.randint(0, 500)
            raza = random.choice(razas)
            
            # Asegurarse de que el tipo de raza coincida con el tipo de galpón
            while raza.tipo != galpon.tipo:
                raza = random.choice(razas)
            
            Lote.objects.create(
                galpon=galpon,
                raza=raza,
                fecha_ingreso=fecha_ingreso,
                cantidad_inicial=cantidad_inicial,
                edad_inicial=random.randint(1, 10),
                estado='ACTIVO',
                observaciones=f"Lote de prueba para {galpon.nombre} en {galpon.granja.nombre}"
            )
        
        print(f"Creados {Lote.objects.count()} lotes")
    
    # Crear seguimientos diarios
    if SeguimientoDiario.objects.count() == 0:
        print("Creando seguimientos diarios...")
        for lote in Lote.objects.all():
            # Crear seguimientos para los últimos 30 días
            for i in range(30, 0, -1):
                fecha = timezone.now() - timedelta(days=i)
                
                # Valores aleatorios para los seguimientos
                if lote.galpon.tipo == 'PONEDORA':
                    SeguimientoDiario.objects.create(
                        lote=lote,
                        fecha=fecha,
                        mortalidad=random.randint(0, 5),
                        consumo_alimento=random.uniform(40.0, 50.0),
                        produccion_huevos=random.randint(lote.cantidad_inicial - 200, lote.cantidad_inicial),
                        peso_promedio=random.uniform(1.5, 2.0),
                        temperatura=random.uniform(20.0, 25.0),
                        observaciones="Registro de prueba"
                    )
                else:  # ENGORDE
                    SeguimientoDiario.objects.create(
                        lote=lote,
                        fecha=fecha,
                        mortalidad=random.randint(0, 10),
                        consumo_alimento=random.uniform(80.0, 100.0),
                        peso_promedio=random.uniform(2.0, 4.0),
                        temperatura=random.uniform(20.0, 25.0),
                        observaciones="Registro de prueba"
                    )
        
        print(f"Creados {SeguimientoDiario.objects.count()} seguimientos diarios")
    
    print("Generación de datos de prueba completada.")

if __name__ == "__main__":
    create_test_data()
