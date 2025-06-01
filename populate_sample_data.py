import os
import django
import random
from datetime import datetime, timedelta

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
django.setup()

# Import models
from avicola.models import Empresa, UserProfile
from produccion.models import Granja, Galpon, Lote
from inventario.models import Proveedor, Raza, Alimento, Vacuna
from ventas.models import Cliente, TipoHuevo

def populate_avicola_data():
    # Create Empresa
    empresa = Empresa.objects.create(
        rif='J-12345678-9',
        nombre='Granja Avícola El Paraíso',
        direccion='Km 5 Vía Nacional, Estado Portuguesa',
        telefono='+58 412-1234567',
        encargado='Juan Pérez',
        pais='Venezuela',
        moneda='USD'
    )

    # Create UserProfiles
    users_data = [
        {'username': 'admin', 'first_name': 'Admin', 'last_name': 'Principal', 'user_type': 'ADMIN', 'email': 'admin@granja.com'},
        {'username': 'supervisor', 'first_name': 'Maria', 'last_name': 'Rodriguez', 'user_type': 'SUPERVISOR', 'email': 'supervisor@granja.com'},
        {'username': 'veterinario', 'first_name': 'Carlos', 'last_name': 'Mendez', 'user_type': 'VETERINARIO', 'email': 'veterinario@granja.com'},
        {'username': 'operario', 'first_name': 'Luis', 'last_name': 'Garcia', 'user_type': 'OPERARIO', 'email': 'operario@granja.com'}
    ]

    users = []
    for user_data in users_data:
        user = UserProfile.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password='granja2025',  # Change this in production!
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            user_type=user_data['user_type']
        )
        users.append(user)

def populate_produccion_data():
    # Get existing data
    empresa = Empresa.objects.first()
    admin_user = UserProfile.objects.filter(user_type='ADMIN').first()

    # Create Granja
    granja = Granja.objects.create(
        empresa=empresa,
        codigo_granja='GRP-001',
        nombre='Granja Principal',
        direccion='Km 5 Vía Nacional, Estado Portuguesa',
        ubicacion_geografica='9.0°N, 69.0°W',
        telefono='+58 412-1234567',
        encargado=admin_user,
        capacidad_total_aves=5000,
        estado='ACTIVA'
    )

    # Create Galpones
    galpones_data = [
        {'numero_galpon': 'G1', 'tipo_galpon': 'PRODUCCION', 'capacidad_aves': 1000},
        {'numero_galpon': 'G2', 'tipo_galpon': 'CRIA', 'capacidad_aves': 500},
        {'numero_galpon': 'G3', 'tipo_galpon': 'RECRIA', 'capacidad_aves': 750}
    ]

    galpones = []
    for galpon_data in galpones_data:
        galpon = Galpon.objects.create(
            granja=granja,
            numero_galpon=galpon_data['numero_galpon'],
            tipo_galpon=galpon_data['tipo_galpon'],
            capacidad_aves=galpon_data['capacidad_aves'],
            area_metros_cuadrados=random.uniform(100, 500),
            responsable=admin_user
        )
        galpones.append(galpon)

def populate_inventario_data():
    # Create Proveedores
    proveedores_data = [
        {'nombre': 'Alimentos Balanceados SA', 'rif': 'J-87654321-0'},
        {'nombre': 'Veterinaria El Gallo', 'rif': 'J-23456789-1'}
    ]

    proveedores = []
    for proveedor_data in proveedores_data:
        proveedor = Proveedor.objects.create(
            nombre=proveedor_data['nombre'],
            rif=proveedor_data['rif'],
            telefono='+58 412-' + ''.join(random.choices('0123456789', k=7)),
            email=proveedor_data['nombre'].lower().replace(' ', '_') + '@ejemplo.com'
        )
        proveedores.append(proveedor)

    # Create Razas
    razas_data = [
        {'nombre': 'Hy-Line Brown', 'tipo_raza': 'PONEDORA'},
        {'nombre': 'Ross 308', 'tipo_raza': 'ENGORDE'}
    ]

    razas = []
    for raza_data in razas_data:
        raza = Raza.objects.create(
            nombre=raza_data['nombre'],
            tipo_raza=raza_data['tipo_raza']
        )
        razas.append(raza)

    # Create Alimentos
    alimentos_data = [
        {'nombre': 'Iniciador Ponedoras', 'tipo_alimento': 'Iniciador', 'contenido_proteina': 18.5, 'etapa': 'INICIADOR'},
        {'nombre': 'Alimento Crecimiento', 'tipo_alimento': 'Crecimiento', 'contenido_proteina': 16.0, 'etapa': 'CRECIMIENTO'}
    ]

    alimentos = []
    for alimento_data in alimentos_data:
        alimento = Alimento.objects.create(
            nombre=alimento_data['nombre'],
            tipo_alimento=alimento_data['tipo_alimento'],
            contenido_proteina=alimento_data['contenido_proteina'],
            etapa=alimento_data['etapa'],
            proveedor=proveedores[0]
        )
        alimentos.append(alimento)

def populate_ventas_data():
    # Create TipoHuevo
    tipos_huevo_data = [
        {'clasificacion': 'AA', 'descripcion': 'Extra Grande > 69g'},
        {'clasificacion': 'A', 'descripcion': 'Grande 60-68g'},
        {'clasificacion': 'B', 'descripcion': 'Mediano 53-59g'}
    ]

    tipos_huevo = []
    for tipo_data in tipos_huevo_data:
        tipo = TipoHuevo.objects.create(
            clasificacion=tipo_data['clasificacion'],
            descripcion=tipo_data['descripcion']
        )
        tipos_huevo.append(tipo)

    # Create Clientes
    clientes_data = [
        {'nombre_razon_social': 'Supermercados Unidos', 'rif_cedula': 'J-11223344-5'},
        {'nombre_razon_social': 'Distribuidora El Huevo', 'rif_cedula': 'J-55667788-9'}
    ]

    clientes = []
    for cliente_data in clientes_data:
        cliente = Cliente.objects.create(
            nombre_razon_social=cliente_data['nombre_razon_social'],
            rif_cedula=cliente_data['rif_cedula'],
            telefono_principal='+58 412-' + ''.join(random.choices('0123456789', k=7)),
            direccion_fiscal='Dirección en Venezuela'
        )
        clientes.append(cliente)

def main():
    # Clear existing data
    UserProfile.objects.all().delete()
    Empresa.objects.all().delete()
    Granja.objects.all().delete()
    Galpon.objects.all().delete()
    Proveedor.objects.all().delete()
    Raza.objects.all().delete()
    Alimento.objects.all().delete()
    TipoHuevo.objects.all().delete()
    Cliente.objects.all().delete()

    # Populate data
    populate_avicola_data()
    populate_produccion_data()
    populate_inventario_data()
    populate_ventas_data()

    print("Sample data populated successfully!")

if __name__ == '__main__':
    main()
