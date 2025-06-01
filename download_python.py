import urllib.request
import os

url = 'https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe'
output_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'python-3.10.11-amd64.exe')

print(f"Descargando Python 3.10.11 en {output_path}")
urllib.request.urlretrieve(url, output_path)
print("Descarga completada")
