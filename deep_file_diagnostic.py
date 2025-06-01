import os
import sys

def diagnose_file(filepath):
    print(f"Diagnosing file: {filepath}")
    try:
        # Intentar leer el archivo en modo binario
        with open(filepath, 'rb') as f:
            content = f.read()
            
        # Imprimir información detallada
        print(f"File size: {len(content)} bytes")
        print("Byte representation:")
        
        # Mostrar primeros 50 bytes
        print("First 50 bytes:", content[:50])
        
        # Contar bytes nulos
        null_count = content.count(b'\x00')
        print(f"Number of null bytes: {null_count}")
        
        # Intentar decodificar
        try:
            decoded = content.decode('utf-8', errors='strict')
            print("File can be decoded as UTF-8")
        except UnicodeDecodeError:
            print("Cannot decode file as UTF-8")
            try:
                decoded = content.decode('utf-8', errors='replace')
                print("File can be decoded with replacement")
            except:
                print("Cannot decode file with replacement")
    
    except Exception as e:
        print(f"Error reading file: {e}")

def diagnose_project(root_dir):
    print(f"Diagnosing project in {root_dir}")
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file == '__init__.py':
                filepath = os.path.join(root, file)
                diagnose_file(filepath)

if __name__ == "__main__":
    diagnose_project('.')
