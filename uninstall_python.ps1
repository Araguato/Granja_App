# Script de limpieza de instalaciones de Python

# Función para eliminar Python
function Remove-PythonInstallation {
    # Desinstalar paquetes de Python
    Get-AppxPackage *python* | Remove-AppxPackage

    # Eliminar claves de registro
    Remove-Item -Path "HKLM:\SOFTWARE\Python" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "HKLM:\SOFTWARE\WOW6432Node\Python" -Recurse -Force -ErrorAction SilentlyContinue

    # Eliminar directorios
    Remove-Item -Path "C:\Python*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Users\$env:USERNAME\AppData\Local\Programs\Python" -Recurse -Force -ErrorAction SilentlyContinue

    # Limpiar PATH
    $oldPath = [Environment]::GetEnvironmentVariable('PATH', 'Machine')
    $newPath = ($oldPath -split ';' | Where-Object { $_ -notmatch 'Python' }) -join ';'
    [Environment]::SetEnvironmentVariable('PATH', $newPath, 'Machine')

    Write-Host "Limpieza de Python completada."
}

# Ejecutar función de limpieza
Remove-PythonInstallation

# Verificar instalaciones restantes
Write-Host "Instalaciones de Python restantes:"
Get-Command python -ErrorAction SilentlyContinue
Get-Command pip -ErrorAction SilentlyContinue
