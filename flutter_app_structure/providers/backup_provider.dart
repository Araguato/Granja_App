import 'package:flutter/foundation.dart';
import '../models/backup_model.dart';
import '../services/backup_service.dart';

class BackupProvider with ChangeNotifier {
  final BackupService _backupService = BackupService();
  
  List<Backup> _backups = [];
  Backup? _selectedBackup;
  bool _isLoading = false;
  String? _error;
  Map<String, dynamic> _stats = {};
  Map<String, dynamic> _config = {};

  // Getters
  List<Backup> get backups => [..._backups];
  Backup? get selectedBackup => _selectedBackup;
  bool get isLoading => _isLoading;
  String? get error => _error;
  Map<String, dynamic> get stats => {..._stats};
  Map<String, dynamic> get config => {..._config};

  // Obtener todos los respaldos
  Future<void> fetchBackups() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _backups = await _backupService.getBackups();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
    }
  }

  // Obtener un respaldo específico
  Future<void> fetchBackup(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _selectedBackup = await _backupService.getBackup(id);
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
    }
  }

  // Crear un nuevo respaldo
  Future<bool> createBackup(String backupType, String? notes) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newBackup = await _backupService.createBackup(backupType, notes);
      _backups.add(newBackup);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  // Restaurar un respaldo
  Future<bool> restoreBackup(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final success = await _backupService.restoreBackup(id);
      _isLoading = false;
      notifyListeners();
      return success;
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  // Eliminar un respaldo
  Future<bool> deleteBackup(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final success = await _backupService.deleteBackup(id);
      if (success) {
        _backups.removeWhere((backup) => backup.id == id);
      }
      _isLoading = false;
      notifyListeners();
      return success;
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  // Obtener estadísticas de respaldos
  Future<void> fetchBackupStats() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _stats = await _backupService.getBackupStats();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
    }
  }

  // Obtener configuración de respaldos
  Future<void> fetchBackupConfig() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _config = await _backupService.getBackupConfig();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
    }
  }

  // Actualizar configuración de respaldos
  Future<bool> updateBackupConfig(Map<String, dynamic> config) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final success = await _backupService.updateBackupConfig(config);
      if (success) {
        _config = config;
      }
      _isLoading = false;
      notifyListeners();
      return success;
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  // Limpiar error
  void clearError() {
    _error = null;
    notifyListeners();
  }

  // Seleccionar un respaldo
  void selectBackup(Backup backup) {
    _selectedBackup = backup;
    notifyListeners();
  }
}
