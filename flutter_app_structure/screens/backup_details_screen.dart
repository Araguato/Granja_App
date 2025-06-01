import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/backup_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class BackupDetailsScreen extends StatefulWidget {
  static const routeName = '/backup-details';

  const BackupDetailsScreen({Key? key}) : super(key: key);

  @override
  _BackupDetailsScreenState createState() => _BackupDetailsScreenState();
}

class _BackupDetailsScreenState extends State<BackupDetailsScreen> {
  bool _isInit = true;
  final DateFormat _dateFormat = DateFormat('dd/MM/yyyy HH:mm');

  @override
  void didChangeDependencies() {
    if (_isInit) {
      final backupId = ModalRoute.of(context)!.settings.arguments as int;
      _loadBackupDetails(backupId);
      _isInit = false;
    }
    super.didChangeDependencies();
  }

  Future<void> _loadBackupDetails(int backupId) async {
    await Provider.of<BackupProvider>(context, listen: false).fetchBackup(backupId);
  }

  Color _getStatusColor(String status) {
    switch (status) {
      case 'PENDING':
        return Colors.amber;
      case 'IN_PROGRESS':
        return Colors.blue;
      case 'COMPLETED':
        return Colors.green;
      case 'FAILED':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  void _showRestoreConfirmDialog(BuildContext context, int backupId) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Confirmar Restauración'),
        content: const Text(
          '¿Está seguro de que desea restaurar este respaldo? '
          'Esta acción reemplazará los datos actuales del sistema y no se puede deshacer.',
        ),
        actions: [
          TextButton(
            child: const Text('Cancelar'),
            onPressed: () {
              Navigator.of(ctx).pop();
            },
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.amber,
            ),
            child: const Text('Restaurar'),
            onPressed: () async {
              Navigator.of(ctx).pop();
              
              final backupProvider = Provider.of<BackupProvider>(context, listen: false);
              final success = await backupProvider.restoreBackup(backupId);
              
              if (success && mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Restauración iniciada correctamente'),
                    backgroundColor: Colors.green,
                  ),
                );
                _loadBackupDetails(backupId);
              } else if (mounted) {
                showDialog(
                  context: context,
                  builder: (ctx) => ErrorDialog(
                    message: backupProvider.error ?? 'Error al restaurar respaldo',
                  ),
                );
              }
            },
          ),
        ],
      ),
    );
  }

  void _showDeleteConfirmDialog(BuildContext context, int backupId) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Confirmar Eliminación'),
        content: const Text(
          '¿Está seguro de que desea eliminar este respaldo? '
          'Esta acción no se puede deshacer.',
        ),
        actions: [
          TextButton(
            child: const Text('Cancelar'),
            onPressed: () {
              Navigator.of(ctx).pop();
            },
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.red,
            ),
            child: const Text('Eliminar'),
            onPressed: () async {
              Navigator.of(ctx).pop();
              
              final backupProvider = Provider.of<BackupProvider>(context, listen: false);
              final success = await backupProvider.deleteBackup(backupId);
              
              if (success && mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Respaldo eliminado correctamente'),
                    backgroundColor: Colors.green,
                  ),
                );
                Navigator.of(context).pop(); // Volver a la pantalla anterior
              } else if (mounted) {
                showDialog(
                  context: context,
                  builder: (ctx) => ErrorDialog(
                    message: backupProvider.error ?? 'Error al eliminar respaldo',
                  ),
                );
              }
            },
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detalles del Respaldo'),
        backgroundColor: Colors.green,
      ),
      body: Consumer<BackupProvider>(
        builder: (ctx, backupProvider, child) {
          if (backupProvider.isLoading) {
            return const LoadingIndicator();
          }

          if (backupProvider.error != null) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    'Error: ${backupProvider.error}',
                    textAlign: TextAlign.center,
                    style: const TextStyle(color: Colors.red),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    onPressed: () {
                      final backupId = ModalRoute.of(context)!.settings.arguments as int;
                      _loadBackupDetails(backupId);
                    },
                    child: const Text('Reintentar'),
                  ),
                ],
              ),
            );
          }

          final backup = backupProvider.selectedBackup;
          if (backup == null) {
            return const Center(
              child: Text('No se encontró el respaldo'),
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Tarjeta de información principal
                Card(
                  elevation: 4,
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              backgroundColor: _getStatusColor(backup.status).withOpacity(0.2),
                              radius: 24,
                              child: Icon(
                                Icons.backup,
                                color: _getStatusColor(backup.status),
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    backup.name,
                                    style: const TextStyle(
                                      fontSize: 20,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Chip(
                                    label: Text(
                                      backup.statusText,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontSize: 12,
                                      ),
                                    ),
                                    backgroundColor: _getStatusColor(backup.status),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                        const Divider(height: 32),
                        _buildInfoRow('ID', backup.id.toString()),
                        _buildInfoRow('Tipo', backup.backupTypeText),
                        _buildInfoRow('Tamaño', '${backup.sizeInMb.toStringAsFixed(2)} MB'),
                        _buildInfoRow('Creado', _dateFormat.format(backup.createdAt)),
                        if (backup.completedAt != null)
                          _buildInfoRow('Completado', _dateFormat.format(backup.completedAt!)),
                        _buildInfoRow('Automático', backup.isAuto ? 'Sí' : 'No'),
                        _buildInfoRow('Archivo', backup.fileExists ? 'Disponible' : 'No disponible'),
                        if (backup.createdBy != null)
                          _buildInfoRow('Creado por', backup.createdBy!),
                      ],
                    ),
                  ),
                ),

                // Notas
                if (backup.notes != null && backup.notes!.isNotEmpty)
                  Card(
                    elevation: 4,
                    margin: const EdgeInsets.only(top: 16),
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Notas',
                            style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(backup.notes!),
                        ],
                      ),
                    ),
                  ),

                // Botones de acción
                const SizedBox(height: 24),
                if (backup.status == 'COMPLETED' && backup.fileExists)
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      icon: const Icon(Icons.restore),
                      label: const Text('Restaurar Respaldo'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.amber,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                      onPressed: () => _showRestoreConfirmDialog(context, backup.id),
                    ),
                  ),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    icon: const Icon(Icons.delete),
                    label: const Text('Eliminar Respaldo'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                    onPressed: () => _showDeleteConfirmDialog(context, backup.id),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 100,
            child: Text(
              '$label:',
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.grey,
              ),
            ),
          ),
          Expanded(
            child: Text(
              value,
              style: const TextStyle(
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
