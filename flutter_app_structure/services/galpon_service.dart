import '../models/galpon_model.dart';
import 'api_service.dart';

class GalponService {
  final ApiService _apiService = ApiService();
  final String endpoint = 'galpones/';

  // Obtener todos los galpones
  Future<List<Galpon>> getGalpones() async {
    final response = await _apiService.get(endpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => Galpon.fromJson(json)).toList();
  }

  // Obtener galpones por granja
  Future<List<Galpon>> getGalponesByGranja(int granjaId) async {
    final response = await _apiService.get('${endpoint}?granja=$granjaId');
    final List<dynamic> results = response['results'];
    return results.map((json) => Galpon.fromJson(json)).toList();
  }

  // Obtener un galpon por ID
  Future<Galpon> getGalpon(int id) async {
    final response = await _apiService.get('$endpoint$id/');
    return Galpon.fromJson(response);
  }

  // Crear un nuevo galpon
  Future<Galpon> createGalpon(Galpon galpon) async {
    final response = await _apiService.post(endpoint, galpon.toJson());
    return Galpon.fromJson(response);
  }

  // Actualizar un galpon existente
  Future<Galpon> updateGalpon(Galpon galpon) async {
    final response = await _apiService.put('$endpoint${galpon.id}/', galpon.toJson());
    return Galpon.fromJson(response);
  }

  // Eliminar un galpon
  Future<void> deleteGalpon(int id) async {
    await _apiService.delete('$endpoint$id/');
  }
}
