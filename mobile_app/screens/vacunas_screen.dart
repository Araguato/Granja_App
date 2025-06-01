import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/vacuna_model.dart';
import '../providers/vacuna_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class VacunasScreen extends StatefulWidget {
  @override
  _VacunasScreenState createState() => _VacunasScreenState();
}

class _VacunasScreenState extends State<VacunasScreen> {
  @override
  void initState() {
    super.initState();
    // Cargar vacunas al iniciar la pantalla
    Future.microtask(() => 
      Provider.of<VacunaProvider>(context, listen: false).loadVacunas()
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Vacunas'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () => _showVacunaForm(context),
          ),
        ],
      ),
      body: Consumer<VacunaProvider>(
        builder: (ctx, vacunaProvider, child) {
          if (vacunaProvider.isLoading) {
            return LoadingIndicator();
          }
          
          if (vacunaProvider.error.isNotEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Error: ${vacunaProvider.error}',
                    style: TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => vacunaProvider.loadVacunas(),
                    child: Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          if (vacunaProvider.vacunas.isEmpty) {
            return Center(
              child: Text('No hay vacunas registradas'),
            );
          }

          return ListView.builder(
            itemCount: vacunaProvider.vacunas.length,
            itemBuilder: (ctx, index) {
              final vacuna = vacunaProvider.vacunas[index];
              return Card(
                margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  title: Text(vacuna.nombreComercial),
                  subtitle: Text(vacuna.enfermedadObjetivo),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.edit),
                        onPressed: () => _showVacunaForm(context, vacuna),
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () => _confirmDelete(context, vacuna),
                      ),
                    ],
                  ),
                  onTap: () => _showVacunaDetails(context, vacuna),
                ),
              );
            },
          );
        },
      ),
    );
  }

  void _showVacunaDetails(BuildContext context, Vacuna vacuna) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(vacuna.nombreComercial),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Enfermedad: ${vacuna.enfermedadObjetivo}'),
              if (vacuna.descripcion != null && vacuna.descripcion!.isNotEmpty)
                Text('Descripción: ${vacuna.descripcion}'),
              if (vacuna.laboratorio != null && vacuna.laboratorio!.isNotEmpty)
                Text('Laboratorio: ${vacuna.laboratorio}'),
              if (vacuna.numeroLote != null && vacuna.numeroLote!.isNotEmpty)
                Text('Lote: ${vacuna.numeroLote}'),
              if (vacuna.fechaVencimiento != null && vacuna.fechaVencimiento!.isNotEmpty)
                Text('Vencimiento: ${vacuna.fechaVencimiento}'),
              Text('Proveedor: ${vacuna.proveedorNombre}'),
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

  void _showVacunaForm(BuildContext context, [Vacuna? vacuna]) {
    // Aquí iría la lógica para mostrar un formulario de creación/edición
    // Se implementaría como un StatefulWidget separado
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(vacuna == null ? 'Nueva Vacuna' : 'Editar Vacuna'),
        content: Text('Formulario de vacuna (implementar)'),
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

  void _confirmDelete(BuildContext context, Vacuna vacuna) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Confirmar eliminación'),
        content: Text('¿Está seguro que desea eliminar la vacuna ${vacuna.nombreComercial}?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              _deleteVacuna(context, vacuna.id);
            },
            child: Text('Eliminar'),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteVacuna(BuildContext context, int id) async {
    final success = await Provider.of<VacunaProvider>(context, listen: false)
        .deleteVacuna(id);
    
    if (!success) {
      if (!mounted) return;
      showDialog(
        context: context,
        builder: (ctx) => ErrorDialog(
          message: Provider.of<VacunaProvider>(context, listen: false).error,
        ),
      );
    }
  }
}
