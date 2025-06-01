import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/backup_provider.dart';
import '../widgets/loading_indicator.dart';
import '../widgets/error_dialog.dart';

class BackupConfigScreen extends StatefulWidget {
  static const routeName = '/backup-config';

  const BackupConfigScreen({Key? key}) : super(key: key);

  @override
  _BackupConfigScreenState createState() => _BackupConfigScreenState();
}

class _BackupConfigScreenState extends State<BackupConfigScreen> {
  bool _isInit = true;
  final _formKey = GlobalKey<FormState>();
  
  // Controladores para los campos del formulario
  final _backupDirectoryController = TextEditingController();
  final _maxBackupsController = TextEditingController();
  final _autoBackupFrequencyController = TextEditingController();
  final _notificationEmailController = TextEditingController();
  
  // Variables para los campos de tipo checkbox
  bool _autoBackupEnabled = false;
  bool _includeDatabase = true;
  bool _includeMedia = true;
  bool _compressBackup = true;
  bool _encryptBackup = false;

  @override
  void dispose() {
    _backupDirectoryController.dispose();
    _maxBackupsController.dispose();
    _autoBackupFrequencyController.dispose();
    _notificationEmailController.dispose();
    super.dispose();
  }

  @override
  void didChangeDependencies() {
    if (_isInit) {
      _loadBackupConfig();
      _isInit = false;
    }
    super.didChangeDependencies();
  }

  Future<void> _loadBackupConfig() async {
    try {
      await Provider.of<BackupProvider>(context, listen: false).fetchBackupConfig();
      
      // Llenar los campos del formulario con los valores de la configuración
      final config = Provider.of<BackupProvider>(context, listen: false).config;
      
      setState(() {
        _backupDirectoryController.text = config['backup_directory'] ?? '';
        _maxBackupsController.text = (config['max_backups'] ?? 10).toString();
        _autoBackupEnabled = config['auto_backup_enabled'] ?? false;
        _autoBackupFrequencyController.text = (config['auto_backup_frequency'] ?? 24).toString();
        _includeDatabase = config['include_database'] ?? true;
        _includeMedia = config['include_media'] ?? true;
        _compressBackup = config['compress_backup'] ?? true;
        _encryptBackup = config['encrypt_backup'] ?? false;
        _notificationEmailController.text = config['notification_email'] ?? '';
      });
    } catch (e) {
      if (mounted) {
        showDialog(
          context: context,
          builder: (ctx) => ErrorDialog(
            message: 'Error al cargar la configuración: $e',
          ),
        );
      }
    }
  }

  Future<void> _saveConfig() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    // Crear objeto de configuración
    final config = {
      'backup_directory': _backupDirectoryController.text,
      'max_backups': int.parse(_maxBackupsController.text),
      'auto_backup_enabled': _autoBackupEnabled,
      'auto_backup_frequency': int.parse(_autoBackupFrequencyController.text),
      'include_database': _includeDatabase,
      'include_media': _includeMedia,
      'compress_backup': _compressBackup,
      'encrypt_backup': _encryptBackup,
      'notification_email': _notificationEmailController.text,
    };

    try {
      final success = await Provider.of<BackupProvider>(context, listen: false)
          .updateBackupConfig(config);

      if (success && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Configuración guardada correctamente'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        showDialog(
          context: context,
          builder: (ctx) => ErrorDialog(
            message: 'Error al guardar la configuración: $e',
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Configuración de Respaldos'),
        backgroundColor: Colors.green,
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: _saveConfig,
          ),
        ],
      ),
      body: Consumer<BackupProvider>(
        builder: (ctx, backupProvider, child) {
          if (backupProvider.isLoading) {
            return const LoadingIndicator();
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Configuración General
                  _buildSectionTitle('Configuración General'),
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          TextFormField(
                            controller: _backupDirectoryController,
                            decoration: const InputDecoration(
                              labelText: 'Directorio de Respaldos',
                              border: OutlineInputBorder(),
                              helperText: 'Ruta donde se guardarán los archivos de respaldo',
                            ),
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Por favor ingrese un directorio';
                              }
                              return null;
                            },
                          ),
                          const SizedBox(height: 16),
                          TextFormField(
                            controller: _maxBackupsController,
                            decoration: const InputDecoration(
                              labelText: 'Máximo de Respaldos',
                              border: OutlineInputBorder(),
                              helperText: 'Número máximo de respaldos a mantener',
                            ),
                            keyboardType: TextInputType.number,
                            validator: (value) {
                              if (value == null || value.isEmpty) {
                                return 'Por favor ingrese un número';
                              }
                              if (int.tryParse(value) == null) {
                                return 'Por favor ingrese un número válido';
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Respaldo Automático
                  _buildSectionTitle('Respaldo Automático'),
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          SwitchListTile(
                            title: const Text('Habilitar Respaldo Automático'),
                            subtitle: const Text('Realizar respaldos automáticos programados'),
                            value: _autoBackupEnabled,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              setState(() {
                                _autoBackupEnabled = value;
                              });
                            },
                          ),
                          const SizedBox(height: 16),
                          TextFormField(
                            controller: _autoBackupFrequencyController,
                            decoration: const InputDecoration(
                              labelText: 'Frecuencia (horas)',
                              border: OutlineInputBorder(),
                              helperText: 'Cada cuántas horas se realizará el respaldo automático',
                            ),
                            keyboardType: TextInputType.number,
                            enabled: _autoBackupEnabled,
                            validator: (value) {
                              if (_autoBackupEnabled) {
                                if (value == null || value.isEmpty) {
                                  return 'Por favor ingrese un número';
                                }
                                if (int.tryParse(value) == null) {
                                  return 'Por favor ingrese un número válido';
                                }
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Contenido del Respaldo
                  _buildSectionTitle('Contenido del Respaldo'),
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          CheckboxListTile(
                            title: const Text('Incluir Base de Datos'),
                            subtitle: const Text('Incluir la base de datos en los respaldos'),
                            value: _includeDatabase,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              setState(() {
                                _includeDatabase = value ?? true;
                              });
                            },
                          ),
                          CheckboxListTile(
                            title: const Text('Incluir Archivos de Medios'),
                            subtitle: const Text('Incluir imágenes y otros archivos'),
                            value: _includeMedia,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              setState(() {
                                _includeMedia = value ?? true;
                              });
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Opciones Avanzadas
                  _buildSectionTitle('Opciones Avanzadas'),
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          CheckboxListTile(
                            title: const Text('Comprimir Respaldo'),
                            subtitle: const Text('Reducir el tamaño del archivo de respaldo'),
                            value: _compressBackup,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              setState(() {
                                _compressBackup = value ?? true;
                              });
                            },
                          ),
                          CheckboxListTile(
                            title: const Text('Cifrar Respaldo'),
                            subtitle: const Text('Proteger el respaldo con cifrado'),
                            value: _encryptBackup,
                            activeColor: Colors.green,
                            onChanged: (value) {
                              setState(() {
                                _encryptBackup = value ?? false;
                              });
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 24),
                  
                  // Notificaciones
                  _buildSectionTitle('Notificaciones'),
                  Card(
                    elevation: 2,
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        children: [
                          TextFormField(
                            controller: _notificationEmailController,
                            decoration: const InputDecoration(
                              labelText: 'Correo Electrónico',
                              border: OutlineInputBorder(),
                              helperText: 'Correo para recibir notificaciones (opcional)',
                            ),
                            keyboardType: TextInputType.emailAddress,
                            validator: (value) {
                              if (value != null && value.isNotEmpty) {
                                // Validación simple de correo electrónico
                                if (!value.contains('@') || !value.contains('.')) {
                                  return 'Por favor ingrese un correo válido';
                                }
                              }
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  
                  // Botón de guardar
                  SizedBox(
                    width: double.infinity,
                    height: 50,
                    child: ElevatedButton(
                      onPressed: _saveConfig,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                      ),
                      child: const Text(
                        'Guardar Configuración',
                        style: TextStyle(fontSize: 16),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8.0),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
          color: Colors.green,
        ),
      ),
    );
  }
}
