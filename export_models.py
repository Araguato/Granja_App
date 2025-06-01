import os
import sys
import traceback
import django
import json
from django.core.wsgi import get_wsgi_application

# Configurar ruta del proyecto
project_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_path)

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granja.settings')
try:
    django.setup()
except Exception as e:
    print(f'Error configurando Django: {e}')
    print(traceback.format_exc())
    sys.exit(1)

# Importar todos los modelos
from avicola.models import Empresa, UserProfile
from inventario.models import Proveedor, Raza, Alimento, Vacuna, Insumo
from produccion.models import Granja, Galpon, Lote
from ventas.models import Cliente, TipoHuevo, Venta

def export_model_to_json(model_class, filename):
    """Exportar modelo a JSON para facilitar migración"""
    data = []
    for obj in model_class.objects.all():
        item = {}
        for field in obj._meta.fields:
            value = getattr(obj, field.name)
            item[field.name] = str(value)
        data.append(item)
    
    with open(f'export_{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Exportar modelos
models_to_export = [
    (Empresa, 'empresa'),
    (UserProfile, 'user_profile'),
    (Proveedor, 'proveedor'),
    (Raza, 'raza'),
    (Alimento, 'alimento'),
    (Vacuna, 'vacuna'),
    (Granja, 'granja'),
    (Galpon, 'galpon'),
    (Cliente, 'cliente'),
    (TipoHuevo, 'tipo_huevo')
]

for model, name in models_to_export:
    export_model_to_json(model, name)

print("Exportación completada. Archivos JSON generados.")
