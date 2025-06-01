import '../models/lote_model.dart';
import 'api_service.dart';

class LoteService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'lotes/';

  // Obtener todos los lotes
  Future<List<Lote>> getLotes() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Lote.fromJson(json)).toList();
  }

  // Obtener lotes por galpon
  Future<List<Lote>> getLotesByGalpon(int galponId) async {
    final response = await _apiService.get('${endpoint}?galpon=$galponId');
    final List<dynamic> results = response['results'];
    return results.map((json) => Lote.fromJson(json)).toList();
  }

  // Obtener lotes por raza
  Future<List<Lote>> getLotesByRaza(int razaId) async {
    final response = await _apiService.get('${endpoint}?raza=$razaId');
    final List<dynamic> results = response['results'];
    return results.map((json) => Lote.fromJson(json)).toList();
  }

  // Obtener lotes por estado
  Future<List<Lote>> getLotesByEstado(String estado) async {
    final response = await _apiService.get('${endpoint}?estado=$estado');
    final List<dynamic> results = response['results'];
    return results.map((json) => Lote.fromJson(json)).toList();
  }

  // Obtener un lote por ID
  Future<Lote> getLote(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Lote.fromJson(response);
  }

  // Crear un nuevo lote
  Future<Lote> createLote(Lote lote) async {
    final response = await _apiService.post(endpoint, lote.toJson());
    return Lote.fromJson(response);
  }

  // Actualizar un lote existente
  Future<Lote> updateLote(Lote lote) async {
    final response = await _apiService.put('$endpoint${lote.id}/', lote.toJson());
    return Lote.fromJson(response);
  }

  // Eliminar un lote
  Future<void> deleteLote(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
