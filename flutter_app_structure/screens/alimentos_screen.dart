import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/alimento_model.dart';
import '../providers/alimento_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class AlimentosScreen extends StatefulWidget {
  @override
  _AlimentosScreenState createState() => _AlimentosScreenState();
}

class _AlimentosScreenState extends State<AlimentosScreen> {
  @override
  void initState() {
    super.initState();
    // Cargar alimentos al iniciar la pantalla
    Future.microtask(() => 
      Provider.of<AlimentoProvider>(context, listen: false).loadAlimentos()
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Alimentos'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () => _showAlimentoForm(context),
          ),
        ],
      ),
      body: Consumer<AlimentoProvider>(
        builder: (ctx, alimentoProvider, child) {
          if (alimentoProvider.isLoading) {
            return LoadingIndicator();
          }
          
          if (alimentoProvider.error.isNotEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Error: ${alimentoProvider.error}',
                    style: TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => alimentoProvider.loadAlimentos(),
                    child: Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          if (alimentoProvider.alimentos.isEmpty) {
            return Center(
              child: Text('No hay alimentos registrados'),
            );
          }

          return ListView.builder(
            itemCount: alimentoProvider.alimentos.length,
            itemBuilder: (ctx, index) {
              final alimento = alimentoProvider.alimentos[index];
              return Card(
                margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  title: Text(alimento.nombre),
                  subtitle: Text('${alimento.tipoAlimento} - ${alimento.etapa}'),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.edit),
                        onPressed: () => _showAlimentoForm(context, alimento),
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () => _confirmDelete(context, alimento),
                      ),
                    ],
                  ),
                  onTap: () => _showAlimentoDetails(context, alimento),
                ),
              );
            },
          );
        },
      ),
    );
  }

  void _showAlimentoDetails(BuildContext context, Alimento alimento) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(alimento.nombre),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Tipo: ${alimento.tipoAlimento}'),
              Text('Etapa: ${alimento.etapa}'),
              Text('Descripción: ${alimento.descripcion}'),
              if (alimento.contenidoProteina != null)
                Text('Proteína: ${alimento.contenidoProteina}%'),
              if (alimento.energiaMetabolizable != null)
                Text('Energía Metabolizable: ${alimento.energiaMetabolizable} kcal/kg'),
              if (alimento.grasaCruda != null)
                Text('Grasa Cruda: ${alimento.grasaCruda}%'),
              if (alimento.fibraCruda != null)
                Text('Fibra Cruda: ${alimento.fibraCruda}%'),
              if (alimento.calcio != null)
                Text('Calcio: ${alimento.calcio}%'),
              if (alimento.fosforo != null)
                Text('Fósforo: ${alimento.fosforo}%'),
              Text('Proveedor: ${alimento.proveedorNombre}'),
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

  void _showAlimentoForm(BuildContext context, [Alimento? alimento]) {
    // Aquí iría la lógica para mostrar un formulario de creación/edición
    // Se implementaría como un StatefulWidget separado
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(alimento == null ? 'Nuevo Alimento' : 'Editar Alimento'),
        content: Text('Formulario de alimento (implementar)'),
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

  void _confirmDelete(BuildContext context, Alimento alimento) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Confirmar eliminación'),
        content: Text('¿Está seguro que desea eliminar el alimento ${alimento.nombre}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              _deleteAlimento(context, alimento.id);
            },
            child: Text('Eliminar'),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteAlimento(BuildContext context, int id) async {
    final success = await Provider.of<AlimentoProvider>(context, listen: false)
        .deleteAlimento(id);
    
    if (!success) {
      if (!mounted) return;
      showDialog(
        context: context,
        builder: (ctx) => ErrorDialog(
          message: Provider.of<AlimentoProvider>(context, listen: false).error,
        ),
      );
    }
  }
}
