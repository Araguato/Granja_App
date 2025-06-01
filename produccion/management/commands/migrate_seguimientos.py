import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from produccion.models import Lote, SeguimientoDiario
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Migra los datos de seguimiento desde archivos JSON a la base de datos'

    def handle(self, *args, **options):
        # Directorio donde están los archivos JSON
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        
        # Buscar todos los archivos de seguimiento
        import glob
        json_files = glob.glob(os.path.join(data_dir, 'seguimientos_lote_*.json'))
        
        if not json_files:
            self.stdout.write(self.style.WARNING('No se encontraron archivos de seguimiento para migrar.'))
            return
        
        total_created = 0
        total_skipped = 0
        
        # Obtener o crear un usuario administrador para los registros
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
        
        for json_file in json_files:
            try:
                # Extraer el ID del lote del nombre del archivo
                lote_id = int(os.path.basename(json_file).split('_')[-1].split('.')[0])
                
                # Verificar si el lote existe
                try:
                    lote = Lote.objects.get(id=lote_id)
                except Lote.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Lote con ID {lote_id} no encontrado. Saltando archivo: {json_file}'))
                    total_skipped += 1
                    continue
                
                # Leer el archivo JSON
                with open(json_file, 'r', encoding='utf-8') as f:
                    seguimientos = json.load(f)
                
                # Procesar cada seguimiento
                for seguimiento_data in seguimientos:
                    # Verificar si ya existe un seguimiento para esta fecha
                    fecha_seguimiento = seguimiento_data.get('fecha')
                    if not fecha_seguimiento:
                        self.stdout.write(self.style.WARNING(f'Fecha de seguimiento no especificada en {json_file}. Saltando registro.'))
                        continue
                    
                    # Verificar si ya existe un seguimiento para esta fecha y lote
                    if SeguimientoDiario.objects.filter(
                        lote=lote, 
                        fecha_seguimiento=fecha_seguimiento
                    ).exists():
                        self.stdout.write(self.style.NOTICE(f'Seguimiento para lote {lote_id} en fecha {fecha_seguimiento} ya existe. Saltando.'))
                        total_skipped += 1
                        continue
                    
                    # Crear el nuevo seguimiento
                    try:
                        # Convertir gramos a kg para peso_promedio_ave
                        peso_kg = float(seguimiento_data.get('peso_promedio', 0)) / 1000
                        
                        SeguimientoDiario.objects.create(
                            lote=lote,
                            fecha_seguimiento=fecha_seguimiento,
                            registrado_por=admin_user,
                            tipo_seguimiento='ENGORDE',  # O el tipo apropiado
                            peso_promedio_ave=peso_kg,
                            consumo_alimento_kg=float(seguimiento_data.get('consumo_alimento', 0)),
                            mortalidad=seguimiento_data.get('mortalidad', 0),
                            observaciones=seguimiento_data.get('observaciones', '')
                        )
                        total_created += 1
                        self.stdout.write(self.style.SUCCESS(f'Creado seguimiento para lote {lote_id} en fecha {fecha_seguimiento}'))
                        
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error al crear seguimiento: {str(e)} para lote {lote_id} en fecha {fecha_seguimiento}'))
                        total_skipped += 1
            
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error procesando archivo {json_file}: {str(e)}'))
                total_skipped += 1
        
        self.stdout.write(self.style.SUCCESS(f'Migración completada. Creados: {total_created}, Saltados: {total_skipped}'))
