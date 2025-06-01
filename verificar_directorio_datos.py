import os
from pathlib import Path

# Ruta al directorio de datos
data_dir = os.path.join(Path(__file__).resolve().parent, 'data')

try:
    # Crear directorio si no existe
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Directorio de datos creado en: {data_dir}")
    else:
        print(f"El directorio de datos ya existe en: {data_dir}")
    
    # Verificar permisos de escritura
    test_file = os.path.join(data_dir, 'test.txt')
    with open(test_file, 'w') as f:
        f.write('test')
    os.remove(test_file)
    print("Permisos de escritura verificados correctamente.")
    
except Exception as e:
    print(f"Error al verificar el directorio de datos: {e}")
