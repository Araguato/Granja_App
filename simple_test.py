import sys
import os

# Add the windows_app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import just the get_example_data function
from windows_app.api_client import ApiClient

def test_get_example_data():
    print("Testing get_example_data method...")
    
    # Create an instance of ApiClient
    client = ApiClient()
    
    # Mock the imports that would normally be at the top of the file
    import sys
    sys.modules['requests'] = type('MockRequests', (), {'get': lambda *args, **kwargs: None})()
    
    # Test getting different types of example data
    data_types = [
        'usuarios',
        'empresas',
        'lotes',
        'galpones',
        'seguimientos',
        'tareas',
        'grupos',
        'razas',
        'alimentos',
        'vacunas'
    ]
    
    for data_type in data_types:
        print(f"\nTesting data type: {data_type}")
        try:
            data = client.get_example_data(data_type)
            if isinstance(data, list):
                print(f"✓ Success! Retrieved {len(data)} items")
                if data:
                    print(f"   First item: {data[0]}")
            else:
                print(f"✗ Error: Expected a list, got {type(data).__name__}")
        except Exception as e:
            print(f"✗ Error getting {data_type}: {str(e)}")

if __name__ == "__main__":
    test_get_example_data()
