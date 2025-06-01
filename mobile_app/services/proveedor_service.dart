import '../models/proveedor_model.dart';
import 'api_service.dart';

class ProveedorService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'proveedores/';

  // Obtener todos los proveedores
  Future<List<Proveedor>> getProveedores() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Proveedor.fromJson(json)).toList();
  }

  // Obtener un proveedor por ID
  Future<Proveedor> getProveedor(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Proveedor.fromJson(response);
  }

  // Crear un nuevo proveedor
  Future<Proveedor> createProveedor(Proveedor proveedor) async {
    final response = await _apiService.post(endpoint, proveedor.toJson());
    return Proveedor.fromJson(response);
  }

  // Actualizar un proveedor existente
  Future<Proveedor> updateProveedor(Proveedor proveedor) async {
    final response = await _apiService.put('$endpoint${proveedor.id}/', proveedor.toJson());
    return Proveedor.fromJson(response);
  }

  // Eliminar un proveedor
  Future<void> deleteProveedor(int id) async {
    await _apiService.delete('$endpoint$id/');
  }

  // Buscar proveedores por nombre
  Future<List<Proveedor>> searchProveedores(String query) async {
    final response = await _apiService.get('${endpoint}?search=$query');
    final List<dynamic> results = response['results'];
    return results.map((json) => Proveedor.fromJson(json)).toList();
  }
}
