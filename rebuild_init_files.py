import os

def rebuild_init_files(directory):
    print(f"Rebuilding __init__.py files in {directory}")
    for root, dirs, files in os.walk(directory):
        if '__init__.py' in files:
            init_path = os.path.join(root, '__init__.py')
            try:
                # Verificar si el archivo está vacío o contiene bytes nulos
                with open(init_path, 'rb') as f:
                    content = f.read()
                
                # Si el archivo está vacío o contiene bytes nulos, reconstruirlo
                if len(content) == 0 or b'\x00' in content:
                    print(f"Rebuilding {init_path}")
                    with open(init_path, 'w') as f:
                        f.write('# Django app initialization\n')
            except Exception as e:
                print(f"Error processing {init_path}: {e}")

if __name__ == "__main__":
    rebuild_init_files('.')
