import '../models/alimento_model.dart';
import 'api_service.dart';

class AlimentoService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'alimentos/';

  // Obtener todos los alimentos
  Future<List<Alimento>> getAlimentos() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Alimento.fromJson(json)).toList();
  }

  // Obtener alimentos por etapa
  Future<List<Alimento>> getAlimentosByEtapa(String etapa) async {
    final response = await _apiService.get('${endpoint}?etapa=$etapa');
    final List<dynamic> results = response['results'];
    return results.map((json) => Alimento.fromJson(json)).toList();
  }

  // Obtener alimentos por proveedor
  Future<List<Alimento>> getAlimentosByProveedor(int proveedorId) async {
    final response = await _apiService.get('${endpoint}?proveedor=$proveedorId');
    final List<dynamic> results = response['results'];
    return results.map((json) => Alimento.fromJson(json)).toList();
  }

  // Obtener un alimento por ID
  Future<Alimento> getAlimento(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Alimento.fromJson(response);
  }

  // Crear un nuevo alimento
  Future<Alimento> createAlimento(Alimento alimento) async {
    final response = await _apiService.post(endpoint, alimento.toJson());
    return Alimento.fromJson(response);
  }

  // Actualizar un alimento existente
  Future<Alimento> updateAlimento(Alimento alimento) async {
    final response = await _apiService.put('$endpoint${alimento.id}/', alimento.toJson());
    return Alimento.fromJson(response);
  }

  // Eliminar un alimento
  Future<void> deleteAlimento(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
