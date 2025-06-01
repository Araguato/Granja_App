import '../models/vacuna_model.dart';
import 'api_service.dart';

class VacunaService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'vacunas/';

  // Obtener todas las vacunas
  Future<List<Vacuna>> getVacunas() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Vacuna.fromJson(json)).toList();
  }

  // Obtener vacunas por proveedor
  Future<List<Vacuna>> getVacunasByProveedor(int proveedorId) async {
    final response = await _apiService.get('${endpoint}?proveedor=$proveedorId');
    final List<dynamic> results = response['results'];
    return results.map((json) => Vacuna.fromJson(json)).toList();
  }

  // Obtener vacunas por enfermedad
  Future<List<Vacuna>> getVacunasByEnfermedad(String enfermedad) async {
    final response = await _apiService.get('${endpoint}?enfermedad_objetivo=$enfermedad');
    final List<dynamic> results = response['results'];
    return results.map((json) => Vacuna.fromJson(json)).toList();
  }

  // Obtener una vacuna por ID
  Future<Vacuna> getVacuna(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Vacuna.fromJson(response);
  }

  // Crear una nueva vacuna
  Future<Vacuna> createVacuna(Vacuna vacuna) async {
    final response = await _apiService.post(endpoint, vacuna.toJson());
    return Vacuna.fromJson(response);
  }

  // Actualizar una vacuna existente
  Future<Vacuna> updateVacuna(Vacuna vacuna) async {
    final response = await _apiService.put('$endpoint${vacuna.id}/', vacuna.toJson());
    return Vacuna.fromJson(response);
  }

  // Eliminar una vacuna
  Future<void> deleteVacuna(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
