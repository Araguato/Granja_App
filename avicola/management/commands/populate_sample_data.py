from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import random

# Import models
from avicola.models import Empresa, UserProfile
from produccion.models import Granja, Galpon, Lote
from inventario.models import Proveedor, Raza, Alimento, Vacuna
from ventas.models import Cliente, TipoHuevo

class Command(BaseCommand):
    help = 'Populate database with sample data for App_Granja'

    def handle(self, *args, **kwargs):
        # Optional: Add logging or skip deletion
        self.stdout.write('Populating sample data...')

        # Create Empresa
        empresa, created = Empresa.objects.get_or_create(
            rif='J-12345678-9',
            defaults={
                'nombre': 'Granja Avícola El Paraíso',
                'direccion': 'Km 5 Vía Nacional, Estado Portuguesa',
                'telefono': '+58 412-1234567',
                'encargado': 'Juan Pérez',
                'pais': 'Venezuela',
                'moneda': 'USD'
            }
        )
        if created:
            self.stdout.write(f'Created Empresa: {empresa.nombre}')
        else:
            self.stdout.write(f'Empresa already exists: {empresa.nombre}')

        # Create UserProfiles
        users_data = [
            {'username': 'admin', 'first_name': 'Admin', 'last_name': 'Principal', 'user_type': 'ADMIN', 'email': 'admin@granja.com'},
            {'username': 'supervisor', 'first_name': 'Maria', 'last_name': 'Rodriguez', 'user_type': 'SUPERVISOR', 'email': 'supervisor@granja.com'},
            {'username': 'veterinario', 'first_name': 'Carlos', 'last_name': 'Mendez', 'user_type': 'VETERINARIO', 'email': 'veterinario@granja.com'},
            {'username': 'operario', 'first_name': 'Luis', 'last_name': 'Garcia', 'user_type': 'OPERARIO', 'email': 'operario@granja.com'}
        ]

        users = []
        for user_data in users_data:
            try:
                user = UserProfile.objects.get(username=user_data['username'])
                self.stdout.write(f'User already exists: {user.username}')
            except UserProfile.DoesNotExist:
                user = UserProfile.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='granja2025',  # Change this in production!
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    user_type=user_data['user_type']
                )
                self.stdout.write(f'Created User: {user.username}')
            users.append(user)

        # Create Granja
        admin_user = UserProfile.objects.filter(user_type='ADMIN').first()
        granja, created = Granja.objects.get_or_create(
            codigo_granja='GRP-001',
            defaults={
                'empresa': empresa,
                'nombre': 'Granja Principal',
                'direccion': 'Km 5 Vía Nacional, Estado Portuguesa',
                'ubicacion_geografica': '9.0°N, 69.0°W',
                'telefono': '+58 412-1234567',
                'encargado': admin_user,
                'capacidad_total_aves': 5000,
                'estado': 'ACTIVA'
            }
        )
        if created:
            self.stdout.write(f'Created Granja: {granja.nombre}')
        else:
            self.stdout.write(f'Granja already exists: {granja.nombre}')

        # Create Galpones
        galpones_data = [
            {'numero_galpon': 'G1', 'tipo_galpon': 'PRODUCCION', 'capacidad_aves': 1000},
            {'numero_galpon': 'G2', 'tipo_galpon': 'CRIA', 'capacidad_aves': 500},
            {'numero_galpon': 'G3', 'tipo_galpon': 'RECRIA', 'capacidad_aves': 750}
        ]

        galpones = []
        for galpon_data in galpones_data:
            galpon, created = Galpon.objects.get_or_create(
                granja=granja,
                numero_galpon=galpon_data['numero_galpon'],
                defaults={
                    'tipo_galpon': galpon_data['tipo_galpon'],
                    'capacidad_aves': galpon_data['capacidad_aves'],
                    'area_metros_cuadrados': random.uniform(100, 500),
                    'responsable': admin_user
                }
            )
            galpones.append(galpon)
            if created:
                self.stdout.write(f'Created Galpon: {galpon.numero_galpon}')
            else:
                self.stdout.write(f'Galpon already exists: {galpon.numero_galpon}')

        # Create Proveedores
        proveedores_data = [
            {'nombre': 'Alimentos Balanceados SA', 'rif': 'J-87654321-0'},
            {'nombre': 'Veterinaria El Gallo', 'rif': 'J-23456789-1'}
        ]

        proveedores = []
        for proveedor_data in proveedores_data:
            proveedor, created = Proveedor.objects.get_or_create(
                rif=proveedor_data['rif'],
                defaults={
                    'nombre': proveedor_data['nombre'],
                    'telefono': '+58 412-' + ''.join(random.choices('0123456789', k=7)),
                    'email': proveedor_data['nombre'].lower().replace(' ', '_') + '@ejemplo.com'
                }
            )
            proveedores.append(proveedor)
            if created:
                self.stdout.write(f'Created Proveedor: {proveedor.nombre}')
            else:
                self.stdout.write(f'Proveedor already exists: {proveedor.nombre}')

        # Create Razas
        razas_data = [
            {'nombre': 'Hy-Line Brown', 'tipo_raza': 'PONEDORA'},
            {'nombre': 'Ross 308', 'tipo_raza': 'ENGORDE'}
        ]

        razas = []
        for raza_data in razas_data:
            raza, created = Raza.objects.get_or_create(
                nombre=raza_data['nombre'],
                defaults={'tipo_raza': raza_data['tipo_raza']}
            )
            razas.append(raza)
            if created:
                self.stdout.write(f'Created Raza: {raza.nombre}')
            else:
                self.stdout.write(f'Raza already exists: {raza.nombre}')

        # Create Alimentos
        alimentos_data = [
            {'nombre': 'Iniciador Ponedoras', 'tipo_alimento': 'Iniciador', 'proteina_cruda_min': 18.5},
            {'nombre': 'Alimento Crecimiento', 'tipo_alimento': 'Crecimiento', 'proteina_cruda_min': 16.0}
        ]

        alimentos = []
        for alimento_data in alimentos_data:
            alimento = Alimento.objects.create(
                nombre=alimento_data['nombre'],
                tipo_alimento=alimento_data['tipo_alimento'],
                proteina_cruda_min=alimento_data['proteina_cruda_min'],
                proveedor=proveedores[0]
            )
            alimentos.append(alimento)

        # Create TipoHuevo
        tipos_huevo_data = [
            {'clasificacion': 'AA', 'descripcion': 'Extra Grande > 69g'},
            {'clasificacion': 'A', 'descripcion': 'Grande 60-68g'},
            {'clasificacion': 'B', 'descripcion': 'Mediano 53-59g'}
        ]

        tipos_huevo = []
        for tipo_data in tipos_huevo_data:
            tipo, created = TipoHuevo.objects.get_or_create(
                clasificacion=tipo_data['clasificacion'],
                defaults={'descripcion': tipo_data['descripcion']}
            )
            tipos_huevo.append(tipo)
            if created:
                self.stdout.write(f'Created TipoHuevo: {tipo.clasificacion}')
            else:
                self.stdout.write(f'TipoHuevo already exists: {tipo.clasificacion}')

        # Create Clientes
        clientes_data = [
            {'nombre_razon_social': 'Supermercados Unidos', 'rif_cedula': 'J-11223344-5'},
            {'nombre_razon_social': 'Distribuidora El Huevo', 'rif_cedula': 'J-55667788-9'}
        ]

        clientes = []
        for cliente_data in clientes_data:
            cliente, created = Cliente.objects.get_or_create(
                rif_cedula=cliente_data['rif_cedula'],
                defaults={
                    'nombre_razon_social': cliente_data['nombre_razon_social'],
                    'telefono_principal': '+58 412-' + ''.join(random.choices('0123456789', k=7)),
                    'direccion_fiscal': 'Dirección en Venezuela'
                }
            )
            clientes.append(cliente)
            if created:
                self.stdout.write(f'Created Cliente: {cliente.nombre_razon_social}')
            else:
                self.stdout.write(f'Cliente already exists: {cliente.nombre_razon_social}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
