import sys
import os

def print_system_info():
    print("Python Executable:", sys.executable)
    print("Python Version:", sys.version)
    print("Current Working Directory:", os.getcwd())
    print("Python Path:")
    for path in sys.path:
        print(f"  - {path}")

def check_django_import():
    try:
        import django
        print("\nDjango Version:", django.get_version())
    except Exception as e:
        print("\nError importing Django:", e)

def check_project_structure():
    print("\nProject Structure:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == "__main__":
    print_system_info()
    check_django_import()
    check_project_structure()
