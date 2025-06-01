import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/proveedor_model.dart';
import '../providers/proveedor_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class ProveedoresScreen extends StatefulWidget {
  @override
  _ProveedoresScreenState createState() => _ProveedoresScreenState();
}

class _ProveedoresScreenState extends State<ProveedoresScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    // Cargar proveedores al iniciar la pantalla
    Future.microtask(() => 
      Provider.of<ProveedorProvider>(context, listen: false).loadProveedores()
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Proveedores'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () => _showProveedorForm(context),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                labelText: 'Buscar proveedores',
                suffixIcon: IconButton(
                  icon: Icon(Icons.search),
                  onPressed: () {
                    if (_searchController.text.isNotEmpty) {
                      Provider.of<ProveedorProvider>(context, listen: false)
                          .searchProveedores(_searchController.text);
                    } else {
                      Provider.of<ProveedorProvider>(context, listen: false)
                          .loadProveedores();
                    }
                  },
                ),
                border: OutlineInputBorder(),
              ),
              onSubmitted: (value) {
                if (value.isNotEmpty) {
                  Provider.of<ProveedorProvider>(context, listen: false)
                      .searchProveedores(value);
                } else {
                  Provider.of<ProveedorProvider>(context, listen: false)
                      .loadProveedores();
                }
              },
            ),
          ),
          Expanded(
            child: Consumer<ProveedorProvider>(
              builder: (ctx, proveedorProvider, child) {
                if (proveedorProvider.isLoading) {
                  return LoadingIndicator();
                }
                
                if (proveedorProvider.error.isNotEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Error: ${proveedorProvider.error}',
                          style: TextStyle(color: Colors.red),
                          textAlign: TextAlign.center,
                        ),
                        SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () => proveedorProvider.loadProveedores(),
                          child: Text('Reintentar'),
                        ),
                      ],
                    ),
                  );
                }

                if (proveedorProvider.proveedores.isEmpty) {
                  return Center(
                    child: Text('No hay proveedores registrados'),
                  );
                }

                return ListView.builder(
                  itemCount: proveedorProvider.proveedores.length,
                  itemBuilder: (ctx, index) {
                    final proveedor = proveedorProvider.proveedores[index];
                    return Card(
                      margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      child: ListTile(
                        title: Text(proveedor.nombre),
                        subtitle: Text('RIF: ${proveedor.rif}'),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(
                              icon: Icon(Icons.edit),
                              onPressed: () => _showProveedorForm(context, proveedor),
                            ),
                            IconButton(
                              icon: Icon(Icons.delete),
                              onPressed: () => _confirmDelete(context, proveedor),
                            ),
                          ],
                        ),
                        onTap: () => _showProveedorDetails(context, proveedor),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  void _showProveedorDetails(BuildContext context, Proveedor proveedor) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(proveedor.nombre),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('RIF: ${proveedor.rif}'),
              Text('Contacto: ${proveedor.contactoPrincipal}'),
              Text('Teléfono: ${proveedor.telefono}'),
              Text('Email: ${proveedor.email}'),
              Text('Dirección: ${proveedor.direccion}'),
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cerrar'),
          ),
        ],
      ),
    );
  }

  void _showProveedorForm(BuildContext context, [Proveedor? proveedor]) {
    // Aquí iría la lógica para mostrar un formulario de creación/edición
    // Se implementaría como un StatefulWidget separado
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(proveedor == null ? 'Nuevo Proveedor' : 'Editar Proveedor'),
        content: Text('Formulario de proveedor (implementar)'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              // Aquí iría la lógica para guardar
              Navigator.of(ctx).pop();
            },
            child: Text('Guardar'),
          ),
        ],
      ),
    );
  }

  void _confirmDelete(BuildContext context, Proveedor proveedor) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Confirmar eliminación'),
        content: Text('¿Está seguro que desea eliminar el proveedor ${proveedor.nombre}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              _deleteProveedor(context, proveedor.id);
            },
            child: Text('Eliminar'),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteProveedor(BuildContext context, int id) async {
    final success = await Provider.of<ProveedorProvider>(context, listen: false)
        .deleteProveedor(id);
    
    if (!success) {
      if (!mounted) return;
      showDialog(
        context: context,
        builder: (ctx) => ErrorDialog(
          message: Provider.of<ProveedorProvider>(context, listen: false).error,
        ),
      );
    }
  }
}
