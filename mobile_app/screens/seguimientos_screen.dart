import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/seguimiento_diario_model.dart';
import '../providers/seguimiento_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class SeguimientosScreen extends StatefulWidget {
  final int? loteId;

  const SeguimientosScreen({Key? key, this.loteId}) : super(key: key);

  @override
  _SeguimientosScreenState createState() => _SeguimientosScreenState();
}

class _SeguimientosScreenState extends State<SeguimientosScreen> {
  @override
  void initState() {
    super.initState();
    // Cargar seguimientos al iniciar la pantalla
    Future.microtask(() {
      if (widget.loteId != null) {
        Provider.of<SeguimientoProvider>(context, listen: false)
            .loadSeguimientosByLote(widget.loteId!);
      } else {
        Provider.of<SeguimientoProvider>(context, listen: false)
            .loadSeguimientos();
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.loteId != null 
            ? 'Seguimiento del Lote' 
            : 'Seguimientos Diarios'),
        actions: [
          IconButton(
            icon: Icon(Icons.add),
            onPressed: () => _showSeguimientoForm(context),
          ),
        ],
      ),
      body: Consumer<SeguimientoProvider>(
        builder: (ctx, seguimientoProvider, child) {
          if (seguimientoProvider.isLoading) {
            return LoadingIndicator();
          }
          
          if (seguimientoProvider.error.isNotEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Error: ${seguimientoProvider.error}',
                    style: TextStyle(color: Colors.red),
                    textAlign: TextAlign.center,
                  ),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      if (widget.loteId != null) {
                        seguimientoProvider.loadSeguimientosByLote(widget.loteId!);
                      } else {
                        seguimientoProvider.loadSeguimientos();
                      }
                    },
                    child: Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          if (seguimientoProvider.seguimientos.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text('No hay registros de seguimiento'),
                  SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () => _showSeguimientoForm(context),
                    child: Text('Agregar Seguimiento'),
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            itemCount: seguimientoProvider.seguimientos.length,
            itemBuilder: (ctx, index) {
              final seguimiento = seguimientoProvider.seguimientos[index];
              return Card(
                margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                child: ListTile(
                  title: Text('Lote: ${seguimiento.loteCode}'),
                  subtitle: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Fecha: ${seguimiento.fechaSeguimiento}'),
                      Text('Tipo: ${seguimiento.tipoSeguimientoDisplay}'),
                    ],
                  ),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: Icon(Icons.edit),
                        onPressed: () => _showSeguimientoForm(context, seguimiento),
                      ),
                      IconButton(
                        icon: Icon(Icons.delete),
                        onPressed: () => _confirmDelete(context, seguimiento),
                      ),
                    ],
                  ),
                  onTap: () => _showSeguimientoDetails(context, seguimiento),
                ),
              );
            },
          );
        },
      ),
    );
  }

  void _showSeguimientoDetails(BuildContext context, SeguimientoDiario seguimiento) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Detalles del Seguimiento'),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Lote: ${seguimiento.loteCode}'),
              Text('Fecha: ${seguimiento.fechaSeguimiento}'),
              Text('Tipo: ${seguimiento.tipoSeguimientoDisplay}'),
              Divider(),
              Text('Aves Presentes: ${seguimiento.avesPresentes}'),
              Text('Mortalidad del día: ${seguimiento.mortalidadDia}'),
              if (seguimiento.pesoPromedioAve != null)
                Text('Peso Promedio: ${seguimiento.pesoPromedioAve} g'),
              if (seguimiento.consumoAlimentoKg != null)
                Text('Consumo de Alimento: ${seguimiento.consumoAlimentoKg} kg'),
              Divider(),
              Text('Producción de Huevos:'),
              if (seguimiento.huevosA != null)
                Text('Tipo A: ${seguimiento.huevosA}'),
              if (seguimiento.huevosB != null)
                Text('Tipo B: ${seguimiento.huevosB}'),
              if (seguimiento.huevosC != null)
                Text('Tipo C: ${seguimiento.huevosC}'),
              if (seguimiento.huevosSucios != null)
                Text('Sucios: ${seguimiento.huevosSucios}'),
              if (seguimiento.huevosRotos != null)
                Text('Rotos: ${seguimiento.huevosRotos}'),
              Text('Total: ${seguimiento.huevosTotal}'),
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

  void _showSeguimientoForm(BuildContext context, [SeguimientoDiario? seguimiento]) {
    // Aquí iría la lógica para mostrar un formulario de creación/edición
    // Se implementaría como un StatefulWidget separado
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text(seguimiento == null ? 'Nuevo Seguimiento' : 'Editar Seguimiento'),
        content: Text('Formulario de seguimiento (implementar)'),
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

  void _confirmDelete(BuildContext context, SeguimientoDiario seguimiento) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Confirmar eliminación'),
        content: Text('¿Está seguro que desea eliminar este registro de seguimiento?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(ctx).pop(),
            child: Text('Cancelar'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(ctx).pop();
              _deleteSeguimiento(context, seguimiento.id);
            },
            child: Text('Eliminar'),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
          ),
        ],
      ),
    );
  }

  Future<void> _deleteSeguimiento(BuildContext context, int id) async {
    final success = await Provider.of<SeguimientoProvider>(context, listen: false)
        .deleteSeguimiento(id);
    
    if (!success) {
      if (!mounted) return;
      showDialog(
        context: context,
        builder: (ctx) => ErrorDialog(
          message: Provider.of<SeguimientoProvider>(context, listen: false).error,
        ),
      );
    }
  }
}
