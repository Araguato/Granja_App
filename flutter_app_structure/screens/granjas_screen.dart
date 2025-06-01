import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/granja_model.dart';
import '../providers/granja_provider.dart';
import '../widgets/error_dialog.dart';
import '../widgets/loading_indicator.dart';

class GranjasScreen extends StatefulWidget {
  static const routeName = '/granjas';

  const GranjasScreen({Key? key}) : super(key: key);

  @override
  _GranjasScreenState createState() => _GranjasScreenState();
}

class _GranjasScreenState extends State<GranjasScreen> {
  bool _isInit = true;

  @override
  void didChangeDependencies() {
    if (_isInit) {
      _fetchGranjas();
      _isInit = false;
    }
    super.didChangeDependencies();
  }

  Future<void> _fetchGranjas() async {
    try {
      await Provider.of<GranjaProvider>(context, listen: false).fetchGranjas();
    } catch (error) {
      if (mounted) {
        showDialog(
          context: context,
          builder: (ctx) => ErrorDialog(
            message: 'Error al cargar las granjas: $error',
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Granjas'),
        backgroundColor: Colors.green,
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showAddEditGranjaDialog(context),
        backgroundColor: Colors.green,
        child: const Icon(Icons.add),
      ),
      body: RefreshIndicator(
        onRefresh: _fetchGranjas,
        child: Consumer<GranjaProvider>(
          builder: (ctx, granjaProvider, child) {
            if (granjaProvider.isLoading) {
              return const LoadingIndicator();
            }

            if (granjaProvider.error != null) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Error: ${granjaProvider.error}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.red),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      onPressed: _fetchGranjas,
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              );
            }

            final granjas = granjaProvider.granjas;

            if (granjas.isEmpty) {
              return const Center(
                child: Text('No hay granjas registradas'),
              );
            }

            return ListView.builder(
              padding: const EdgeInsets.all(8),
              itemCount: granjas.length,
              itemBuilder: (ctx, index) {
                final granja = granjas[index];
                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 8, horizontal: 4),
                  elevation: 3,
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: Colors.green,
                      child: Text(
                        granja.nombre.substring(0, 1).toUpperCase(),
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    title: Text(
                      granja.nombre,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text('Código: ${granja.codigoGranja}'),
                        Text('Capacidad: ${granja.capacidadTotalAves} aves'),
                      ],
                    ),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        IconButton(
                          icon: const Icon(Icons.edit, color: Colors.blue),
                          onPressed: () => _showAddEditGranjaDialog(context, granja),
                        ),
                        IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => _confirmDelete(context, granja),
                        ),
                      ],
                    ),
                    onTap: () {
                      // Navegar a la pantalla de detalle de granja
                      // Navigator.of(context).pushNamed('/granja-detalle', arguments: granja.id);
                    },
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }

  void _showAddEditGranjaDialog(BuildContext context, [Granja? granja]) {
    final _formKey = GlobalKey<FormState>();
    final _codigoController = TextEditingController(text: granja?.codigoGranja ?? '');
    final _nombreController = TextEditingController(text: granja?.nombre ?? '');
    final _direccionController = TextEditingController(text: granja?.direccion ?? '');
    final _ubicacionController = TextEditingController(text: granja?.ubicacionGeografica ?? '');
    final _telefonoController = TextEditingController(text: granja?.telefono ?? '');
    final _capacidadController = TextEditingController(
        text: granja?.capacidadTotalAves.toString() ?? '0');
    
    // En una aplicación real, estos valores vendrían de la API
    final _estados = ['ACTIVA', 'INACTIVA', 'MANTENIMIENTO'];
    String _estadoSeleccionado = granja?.estado ?? _estados[0];

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(granja == null ? 'Agregar Granja' : 'Editar Granja'),
        content: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: _codigoController,
                  decoration: const InputDecoration(labelText: 'Código'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingrese el código';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _nombreController,
                  decoration: const InputDecoration(labelText: 'Nombre'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingrese el nombre';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _direccionController,
                  decoration: const InputDecoration(labelText: 'Dirección'),
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingrese la dirección';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  controller: _ubicacionController,
                  decoration: const InputDecoration(labelText: 'Ubicación Geográfica'),
                ),
                TextFormField(
                  controller: _telefonoController,
                  decoration: const InputDecoration(labelText: 'Teléfono'),
                ),
                TextFormField(
                  controller: _capacidadController,
                  decoration: const InputDecoration(labelText: 'Capacidad Total (aves)'),
                  keyboardType: TextInputType.number,
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return 'Por favor ingrese la capacidad';
                    }
                    if (int.tryParse(value) == null) {
                      return 'Por favor ingrese un número válido';
                    }
                    return null;
                  },
                ),
                DropdownButtonFormField<String>(
                  value: _estadoSeleccionado,
                  decoration: const InputDecoration(labelText: 'Estado'),
                  items: _estados.map((estado) {
                    return DropdownMenuItem(
                      value: estado,
                      child: Text(estado),
                    );
                  }).toList(),
                  onChanged: (value) {
                    if (value != null) {
                      _estadoSeleccionado = value;
                    }
                  },
                ),
              ],
            ),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () async {
              if (_formKey.currentState!.validate()) {
                // En una aplicación real, estos valores vendrían de la API o del usuario logueado
                final empresaId = 1; // Ejemplo
                final encargadoId = null; // Ejemplo

                final granjaData = Granja(
                  id: granja?.id ?? 0, // El ID será ignorado en creación
                  codigoGranja: _codigoController.text,
                  nombre: _nombreController.text,
                  direccion: _direccionController.text,
                  ubicacionGeografica: _ubicacionController.text,
                  telefono: _telefonoController.text,
                  capacidadTotalAves: int.parse(_capacidadController.text),
                  estado: _estadoSeleccionado,
                  empresaId: empresaId,
                  encargadoId: encargadoId,
                );

                final granjaProvider = Provider.of<GranjaProvider>(context, listen: false);
                bool success;

                if (granja == null) {
                  // Crear nueva granja
                  success = await granjaProvider.addGranja(granjaData);
                } else {
                  // Actualizar granja existente
                  success = await granjaProvider.updateGranja(granjaData);
                }

                if (mounted) {
                  Navigator.of(context).pop();
                  
                  if (!success && granjaProvider.error != null) {
                    showDialog(
                      context: context,
                      builder: (ctx) => ErrorDialog(
                        message: granjaProvider.error!,
                      ),
                    );
                  }
                }
              }
            },
            child: Text(granja == null ? 'Agregar' : 'Actualizar'),
          ),
        ],
      ),
    );
  }

  void _confirmDelete(BuildContext context, Granja granja) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Confirmar Eliminación'),
        content: Text('¿Está seguro que desea eliminar la granja ${granja.nombre}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.of(context).pop();
              
              final success = await Provider.of<GranjaProvider>(context, listen: false)
                  .deleteGranja(granja.id);
              
              if (!success && mounted) {
                final error = Provider.of<GranjaProvider>(context, listen: false).error;
                showDialog(
                  context: context,
                  builder: (ctx) => ErrorDialog(
                    message: error ?? 'Error al eliminar la granja',
                  ),
                );
              }
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );
  }
}
