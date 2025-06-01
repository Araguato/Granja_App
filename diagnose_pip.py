import sys
import subprocess
import platform

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(f"Command: {command}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        print("Return Code:", result.returncode)
    except Exception as e:
        print(f"Error running {command}: {e}")

def diagnose_pip():
    print("Python Diagnostic Tool")
    print("=" * 30)
    
    # System Information
    print("\nSystem Information:")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Executable: {sys.executable}")
    
    # PIP Diagnostics
    print("\nPIP Diagnostics:")
    run_command("python -m pip --version")
    run_command("python -m pip list")
    
    # Attempt to upgrade pip
    print("\nAttempting to upgrade pip:")
    run_command("python -m pip install --upgrade pip")

if __name__ == "__main__":
    diagnose_pip()
