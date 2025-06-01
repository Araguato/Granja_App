import os
import sys

def deep_debug():
    print("Deep Debug Tool")
    print("=" * 30)
    
    # Check Python executable
    print("\nPython Executable:")
    print(sys.executable)
    
    # Check virtual environment
    print("\nVirtual Environment:")
    print(f"Activated: {sys.prefix != sys.base_prefix}")
    print(f"Prefix: {sys.prefix}")
    print(f"Base Prefix: {sys.base_prefix}")
    
    # Check Django installation
    try:
        import django
        print("\nDjango:")
        print(f"Version: {django.__version__}")
        print(f"Path: {django.__file__}")
    except ImportError:
        print("\nDjango not found")
    
    # Check project structure
    print("\nProject Structure:")
    for root, dirs, files in os.walk('.'):
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            if file.endswith('.py'):
                print(f"{subindent}{file}")

if __name__ == "__main__":
    deep_debug()
