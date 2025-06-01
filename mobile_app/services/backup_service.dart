import '../models/backup_model.dart';
import 'api_service.dart';

class BackupService {
  final ApiService _apiService = ApiService();

  // Obtener todos los respaldos
  Future<List<Backup>> getBackups() async {
    try {
      final response = await _apiService.get('respaldos/');
      final List<dynamic> backupsJson = response;
      return backupsJson.map((json) => Backup.fromJson(json)).toList();
    } catch (e) {
      throw Exception('Error al obtener respaldos: $e');
    }
  }

  // Obtener un respaldo específico
  Future<Backup> getBackup(int id) async {
    try {
      final response = await _apiService.get('respaldos/$id/');
      return Backup.fromJson(response);
    } catch (e) {
      throw Exception('Error al obtener respaldo: $e');
    }
  }

  // Crear un nuevo respaldo
  Future<Backup> createBackup(String backupType, String? notes) async {
    try {
      final response = await _apiService.post('respaldos/crear/', {
        'backup_type': backupType,
        'notes': notes,
      });
      return Backup.fromJson(response);
    } catch (e) {
      throw Exception('Error al crear respaldo: $e');
    }
  }

  // Restaurar un respaldo
  Future<bool> restoreBackup(int id) async {
    try {
      await _apiService.post('respaldos/$id/restaurar/', {});
      return true;
    } catch (e) {
      throw Exception('Error al restaurar respaldo: $e');
    }
  }

  // Eliminar un respaldo
  Future<bool> deleteBackup(int id) async {
    try {
      await _apiService.delete('respaldos/$id/');
      return true;
    } catch (e) {
      throw Exception('Error al eliminar respaldo: $e');
    }
  }

  // Obtener estadísticas de respaldos
  Future<Map<String, dynamic>> getBackupStats() async {
    try {
      final response = await _apiService.get('respaldos/estadisticas/');
      return response;
    } catch (e) {
      throw Exception('Error al obtener estadísticas de respaldos: $e');
    }
  }

  // Obtener configuración de respaldos
  Future<Map<String, dynamic>> getBackupConfig() async {
    try {
      final response = await _apiService.get('respaldos/configuracion/');
      return response;
    } catch (e) {
      throw Exception('Error al obtener configuración de respaldos: $e');
    }
  }

  // Actualizar configuración de respaldos
  Future<bool> updateBackupConfig(Map<String, dynamic> config) async {
    try {
      await _apiService.put('respaldos/configuracion/', config);
      return true;
    } catch (e) {
      throw Exception('Error al actualizar configuración de respaldos: $e');
    }
  }
}
