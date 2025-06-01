import 'package:http/http.dart' as http;
import '../models/granja_model.dart';
import 'api_service.dart';

class GranjaService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'granjas/';

  // Obtener todas las granjas
  Future<List<Granja>> getGranjas() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Granja.fromJson(json)).toList();
  }

  // Obtener una granja por ID
  Future<Granja> getGranja(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Granja.fromJson(response);
  }

  // Crear una nueva granja
  Future<Granja> createGranja(Granja granja) async {
    final response = await _apiService.post(endpoint, granja.toJson());
    return Granja.fromJson(response);
  }

  // Actualizar una granja existente
  Future<Granja> updateGranja(Granja granja) async {
    final response = await _apiService.put('$endpoint${granja.id}/', granja.toJson());
    return Granja.fromJson(response);
  }

  // Eliminar una granja
  Future<void> deleteGranja(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
