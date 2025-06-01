"""
Script simplificado para generar datos de prueba básicos para la aplicación.
"""

import os
import django
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Importar modelos
from inventario.models import Proveedor, Raza, Alimento
from produccion.models import Granja, Galpon

def create_basic_test_data():
    """
    Crea datos de prueba básicos para la aplicación.
    """
    print("Generando datos de prueba básicos...")
    
    # Crear proveedores
    if Proveedor.objects.count() == 0:
        print("Creando proveedores...")
        Proveedor.objects.create(
            rif="J-12345678-9",
            nombre="Avícola El Dorado",
            contacto_principal="Juan Pérez",
            telefono="1234567890",
            email="info@eldorado.com",
            direccion="Calle Principal #123, Ciudad"
        )
        Proveedor.objects.create(
            rif="J-87654321-0",
            nombre="Distribuidora Avícola Central",
            contacto_principal="María López",
            telefono="0987654321",
            email="contacto@central.com",
            direccion="Avenida Central #456, Ciudad"
        )
        print(f"Creados {Proveedor.objects.count()} proveedores")
    
    # Crear razas
    if Raza.objects.count() == 0:
        print("Creando razas...")
        Raza.objects.create(
            nombre="Hy-Line Brown",
            tipo_raza="PONEDORA",
            descripcion="Gallina ponedora de huevos marrones, alta productividad"
        )
        Raza.objects.create(
            nombre="Ross 308",
            tipo_raza="ENGORDE",
            descripcion="Pollo de engorde de rápido crecimiento"
        )
        print(f"Creadas {Raza.objects.count()} razas")
    
    # Crear alimentos
    if Alimento.objects.count() == 0:
        print("Creando alimentos...")
        proveedor = Proveedor.objects.first()
        if proveedor:
            Alimento.objects.create(
                nombre="Iniciador",
                tipo_alimento="CONCENTRADO",
                etapa="INICIADOR",
                descripcion="Alimento para pollitos de 0-3 semanas",
                proveedor=proveedor
            )
            Alimento.objects.create(
                nombre="Crecimiento",
                tipo_alimento="CONCENTRADO",
                etapa="CRECIMIENTO",
                descripcion="Alimento para pollos de 3-6 semanas",
                proveedor=proveedor
            )
            print(f"Creados {Alimento.objects.count()} alimentos")
    
    # Crear granjas
    if Granja.objects.count() == 0:
        print("Creando granjas...")
        Granja.objects.create(
            nombre="Granja Las Palmas",
            ubicacion="Km 15 vía a la Costa",
            capacidad_total=10000
        )
        print(f"Creadas {Granja.objects.count()} granjas")
    
    # Crear galpones
    if Galpon.objects.count() == 0:
        print("Creando galpones...")
        granja = Granja.objects.first()
        if granja:
            Galpon.objects.create(
                granja=granja,
                nombre="Galpón 1",
                capacidad=3000,
                tipo="PONEDORA"
            )
            Galpon.objects.create(
                granja=granja,
                nombre="Galpón 2",
                capacidad=3000,
                tipo="ENGORDE"
            )
            print(f"Creados {Galpon.objects.count()} galpones")
    
    print("Generación de datos de prueba básicos completada.")

if __name__ == "__main__":
    create_basic_test_data()
