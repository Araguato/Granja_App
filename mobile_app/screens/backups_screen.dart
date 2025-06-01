import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/backup_provider.dart';
import '../models/backup_model.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class BackupsScreen extends StatefulWidget {
  static const routeName = '/backups';

  const BackupsScreen({Key? key}) : super(key: key);

  @override
  _BackupsScreenState createState() => _BackupsScreenState();
}

class _BackupsScreenState extends State<BackupsScreen> {
  bool _isInit = true;
  final DateFormat _dateFormat = DateFormat('dd/MM/yyyy HH:mm');

  @override
  void didChangeDependencies() {
    if (_isInit) {
      _refreshBackups();
      _isInit = false;
    }
    super.didChangeDependencies();
  }

  Future<void> _refreshBackups() async {
    await Provider.of<BackupProvider>(context, listen: false).fetchBackups();
    await Provider.of<BackupProvider>(context, listen: false).fetchBackupStats();
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

  void _showBackupDetails(BuildContext context, Backup backup) {
    Navigator.of(context).pushNamed(
      '/backup-details',
      arguments: backup.id,
    );
  }

  void _showCreateBackupDialog(BuildContext context) {
    String backupType = 'FULL';
    String? notes;

    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Crear Nuevo Respaldo'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Tipo de Respaldo:'),
              DropdownButton<String>(
                value: backupType,
                isExpanded: true,
                items: const [
                  DropdownMenuItem(
                    value: 'FULL',
                    child: Text('Completo (Base de datos y archivos)'),
                  ),
                  DropdownMenuItem(
                    value: 'DB',
                    child: Text('Solo Base de Datos'),
                  ),
                  DropdownMenuItem(
                    value: 'MEDIA',
                    child: Text('Solo Archivos de Medios'),
                  ),
                ],
                onChanged: (value) {
                  setState(() {
                    backupType = value!;
                  });
                },
              ),
              const SizedBox(height: 16),
              TextField(
                decoration: const InputDecoration(
                  labelText: 'Notas (opcional)',
                  border: OutlineInputBorder(),
                ),
                maxLines: 3,
                onChanged: (value) {
                  notes = value;
                },
              ),
            ],
          ),
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
              backgroundColor: Colors.green,
            ),
            child: const Text('Crear'),
            onPressed: () async {
              Navigator.of(ctx).pop();
              
              final backupProvider = Provider.of<BackupProvider>(context, listen: false);
              final success = await backupProvider.createBackup(backupType, notes);
              
              if (success && mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text('Respaldo creado correctamente'),
                    backgroundColor: Colors.green,
                  ),
                );
                _refreshBackups();
              } else if (mounted) {
                showDialog(
                  context: context,
                  builder: (ctx) => ErrorDialog(
                    message: backupProvider.error ?? 'Error al crear respaldo',
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
        title: const Text('Respaldos'),
        backgroundColor: Colors.green,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshBackups,
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _refreshBackups,
        child: Consumer<BackupProvider>(
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
                      onPressed: _refreshBackups,
                      child: const Text('Reintentar'),
                    ),
                  ],
                ),
              );
            }

            final backups = backupProvider.backups;
            final stats = backupProvider.stats;

            if (backups.isEmpty) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.backup,
                      size: 80,
                      color: Colors.grey,
                    ),
                    const SizedBox(height: 16),
                    const Text(
                      'No hay respaldos disponibles',
                      style: TextStyle(fontSize: 18),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.add),
                      label: const Text('Crear Respaldo'),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                      ),
                      onPressed: () => _showCreateBackupDialog(context),
                    ),
                  ],
                ),
              );
            }

            return Column(
              children: [
                // Estadísticas
                if (stats.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Card(
                      elevation: 4,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            _buildStatItem(
                              'Total',
                              stats['total_backups']?.toString() ?? '0',
                              Icons.backup,
                              Colors.blue,
                            ),
                            _buildStatItem(
                              'Exitosos',
                              stats['successful_backups']?.toString() ?? '0',
                              Icons.check_circle,
                              Colors.green,
                            ),
                            _buildStatItem(
                              'Fallidos',
                              stats['failed_backups']?.toString() ?? '0',
                              Icons.error,
                              Colors.red,
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),

                // Lista de respaldos
                Expanded(
                  child: ListView.builder(
                    itemCount: backups.length,
                    itemBuilder: (ctx, i) {
                      final backup = backups[i];
                      return Card(
                        margin: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        child: ListTile(
                          leading: CircleAvatar(
                            backgroundColor: _getStatusColor(backup.status).withOpacity(0.2),
                            child: Icon(
                              Icons.backup,
                              color: _getStatusColor(backup.status),
                            ),
                          ),
                          title: Text(backup.name),
                          subtitle: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Tipo: ${backup.backupTypeText}'),
                              Text('Fecha: ${_dateFormat.format(backup.createdAt)}'),
                            ],
                          ),
                          trailing: Chip(
                            label: Text(
                              backup.statusText,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 12,
                              ),
                            ),
                            backgroundColor: _getStatusColor(backup.status),
                          ),
                          onTap: () => _showBackupDetails(context, backup),
                        ),
                      );
                    },
                  ),
                ),
              ],
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        backgroundColor: Colors.green,
        child: const Icon(Icons.add),
        onPressed: () => _showCreateBackupDialog(context),
      ),
    );
  }

  Widget _buildStatItem(String label, String value, IconData icon, Color color) {
    return Column(
      children: [
        Icon(
          icon,
          color: color,
          size: 30,
        ),
        const SizedBox(height: 8),
        Text(
          value,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
}
