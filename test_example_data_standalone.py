def get_example_data(data_type):
    """
    Returns example data for offline mode.
    
    Args:
        data_type (str): The type of data to retrieve (e.g., 'usuarios', 'empresas', etc.)
        
    Returns:
        list: A list of dictionaries containing example data for the requested type
    """
    examples = {
        'usuarios': [
            {
                'id': 1,
                'username': 'admin',
                'email': 'admin@example.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
                'groups': [1],
                'user_permissions': []
            },
            {
                'id': 2,
                'username': 'juan.perez',
                'email': 'juan.perez@example.com',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'is_active': True,
                'is_staff': True,
                'is_superuser': False,
                'groups': [2],
                'user_permissions': []
            },
            {
                'id': 3,
                'username': 'maria.gomez',
                'email': 'maria.gomez@example.com',
                'first_name': 'María',
                'last_name': 'Gómez',
                'is_active': True,
                'is_staff': False,
                'is_superuser': False,
                'groups': [3],
                'user_permissions': []
            }
        ],
        'empresas': [
            {'id': 1, 'nombre': 'Granja Avícola San José', 'rif': 'J-12345678-9', 'direccion': 'Carretera Nacional, km 12', 'telefono': '04141234567', 'email': 'contacto@granjasanjose.com'},
            {'id': 2, 'nombre': 'Avícola El Prado', 'rif': 'J-98765432-1', 'direccion': 'Vía El Prado, sector La Esperanza', 'telefono': '04241234567', 'email': 'info@avicolaelprado.com'}
        ],
        'lotes': [
            {'id': 1, 'codigo': 'L-2025-001', 'fecha_ingreso': '2025-01-15', 'cantidad_aves': 5000, 'edad_semanas': 5, 'estado': 'Activo', 'raza': 1, 'galpon': 1, 'empresa': 1},
            {'id': 2, 'codigo': 'L-2025-002', 'fecha_ingreso': '2025-02-01', 'cantidad_aves': 3000, 'edad_semanas': 3, 'estado': 'Activo', 'raza': 2, 'galpon': 2, 'empresa': 1}
        ],
        'galpones': [
            {'id': 1, 'codigo': 'G-001', 'capacidad': 6000, 'estado': 'Disponible', 'empresa': 1},
            {'id': 2, 'codigo': 'G-002', 'capacidad': 4000, 'estado': 'Ocupado', 'empresa': 1}
        ],
        'seguimientos': [
            {'id': 1, 'fecha': '2025-03-01', 'cantidad_actual': 4480, 'mortalidad': 20, 'produccion_huevos': 4100, 'peso_promedio': 1.8, 'lote': 1},
            {'id': 2, 'fecha': '2025-03-02', 'cantidad_actual': 4475, 'mortalidad': 5, 'produccion_huevos': 4150, 'peso_promedio': 1.82, 'lote': 1}
        ],
        'tareas': [
            {'id': 1, 'titulo': 'Vacunación Newcastle', 'descripcion': 'Aplicar vacuna de Newcastle a lote L-2025-001', 'fecha_creacion': '2025-03-01', 'fecha_vencimiento': '2025-03-05', 'prioridad': 'Alta', 'estado': 'Pendiente', 'asignado_a': 'Juan Pérez', 'lote': 1},
            {'id': 2, 'titulo': 'Limpieza de galpón', 'descripcion': 'Realizar limpieza y desinfección del galpón 2', 'fecha_creacion': '2025-03-02', 'fecha_vencimiento': '2025-03-03', 'prioridad': 'Media', 'estado': 'Completada', 'asignado_a': 'María Gómez', 'galpon': 2}
        ],
        'grupos': [
            {'id': 1, 'name': 'Administradores', 'permissions': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]},
            {'id': 2, 'name': 'Supervisores', 'permissions': [1, 2, 3, 4, 5, 6]},
            {'id': 3, 'name': 'Operadores', 'permissions': [1, 2, 3]}
        ],
        'razas': [
            {'id': 1, 'nombre': 'Cobb 500', 'descripcion': 'Raza de engorde de rápido crecimiento'},
            {'id': 2, 'nombre': 'Hy-Line Brown', 'descripcion': 'Raza ponedora de huevo marrón'}
        ],
        'alimentos': [
            {'id': 1, 'nombre': 'Iniciador Pollitas', 'tipo': 'Iniciador', 'proteina': 20.5, 'energia_metabolizable': 3000, 'presentacion': 'Sacos de 25 kg'},
            {'id': 2, 'nombre': 'Crecimiento Pollos', 'tipo': 'Crecimiento', 'proteina': 18.0, 'energia_metabolizable': 3100, 'presentacion': 'Sacos de 25 kg'}
        ],
        'vacunas': [
            {'id': 1, 'nombre': 'Newcastle', 'fabricante': 'Merial', 'presentacion': 'Dosis para 1000 aves'},
            {'id': 2, 'nombre': 'Gumboro', 'fabricante': 'Merial', 'presentacion': 'Dosis para 1000 aves'}
        ]
    }
    
    return examples.get(data_type, [])

def test_get_example_data():
    print("Testing get_example_data method...")
    
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
        'vacunas',
        'nonexistent_type'  # Test with a non-existent type
    ]
    
    for data_type in data_types:
        print(f"\nTesting data type: {data_type}")
        try:
            data = get_example_data(data_type)
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
