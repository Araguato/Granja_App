import '../models/seguimiento_diario_model.dart';
import 'api_service.dart';

class SeguimientoService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'seguimientos/';

  // Obtener todos los seguimientos
  Future<List<SeguimientoDiario>> getSeguimientos() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => SeguimientoDiario.fromJson(json)).toList();
  }

  // Obtener seguimientos por lote
  Future<List<SeguimientoDiario>> getSeguimientosByLote(int loteId) async {
    final response = await _apiService.get('${endpoint}?lote=$loteId');
    final List<dynamic> results = response['results'];
    return results.map((json) => SeguimientoDiario.fromJson(json)).toList();
  }

  // Obtener seguimientos por fecha
  Future<List<SeguimientoDiario>> getSeguimientosByFecha(String fecha) async {
    final response = await _apiService.get('${endpoint}?fecha_seguimiento=$fecha');
    final List<dynamic> results = response['results'];
    return results.map((json) => SeguimientoDiario.fromJson(json)).toList();
  }

  // Obtener seguimientos por tipo
  Future<List<SeguimientoDiario>> getSeguimientosByTipo(String tipo) async {
    final response = await _apiService.get('${endpoint}?tipo_seguimiento=$tipo');
    final List<dynamic> results = response['results'];
    return results.map((json) => SeguimientoDiario.fromJson(json)).toList();
  }

  // Obtener un seguimiento por ID
  Future<SeguimientoDiario> getSeguimiento(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return SeguimientoDiario.fromJson(response);
  }

  // Crear un nuevo seguimiento
  Future<SeguimientoDiario> createSeguimiento(SeguimientoDiario seguimiento) async {
    final response = await _apiService.post(endpoint, seguimiento.toJson());
    return SeguimientoDiario.fromJson(response);
  }

  // Actualizar un seguimiento existente
  Future<SeguimientoDiario> updateSeguimiento(SeguimientoDiario seguimiento) async {
    final response = await _apiService.put('$endpoint${seguimiento.id}/', seguimiento.toJson());
    return SeguimientoDiario.fromJson(response);
  }

  // Eliminar un seguimiento
  Future<void> deleteSeguimiento(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
