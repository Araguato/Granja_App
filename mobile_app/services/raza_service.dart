import '../models/raza_model.dart';
import 'api_service.dart';

class RazaService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'razas/';

  // Obtener todas las razas
  Future<List<Raza>> getRazas() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Raza.fromJson(json)).toList();
  }

  // Obtener razas por tipo
  Future<List<Raza>> getRazasByTipo(String tipoRaza) async {
    final response = await _apiService.get('${endpoint}?tipo_raza=$tipoRaza');
    final List<dynamic> results = response['results'];
    return results.map((json) => Raza.fromJson(json)).toList();
  }

  // Obtener una raza por ID
  Future<Raza> getRaza(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Raza.fromJson(response);
  }

  // Crear una nueva raza
  Future<Raza> createRaza(Raza raza) async {
    final response = await _apiService.post(endpoint, raza.toJson());
    return Raza.fromJson(response);
  }

  // Actualizar una raza existente
  Future<Raza> updateRaza(Raza raza) async {
    final response = await _apiService.put('$endpoint${raza.id}/', raza.toJson());
    return Raza.fromJson(response);
  }

  // Eliminar una raza
  Future<void> deleteRaza(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
