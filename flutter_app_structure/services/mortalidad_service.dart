import '../models/mortalidad_model.dart';
import 'api_service.dart';

class MortalidadService {
  final ApiService _apiService = ApiService();
  
  // Endpoints
  final String mortalidadDiariaEndpoint = 'mortalidad-diaria/';
  final String mortalidadSemanalEndpoint = 'mortalidad-semanal/';

  // Métodos para Mortalidad Diaria
  Future<List<MortalidadDiaria>> getMortalidadDiaria() async {
    final response = await _apiService.get(mortalidadDiariaEndpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => MortalidadDiaria.fromJson(json)).toList();
  }

  Future<List<MortalidadDiaria>> getMortalidadDiariaByLote(int loteId) async {
    final response = await _apiService.get('${mortalidadDiariaEndpoint}?lote=$loteId');
    final List<dynamic> results = response['results'];
    return results.map((json) => MortalidadDiaria.fromJson(json)).toList();
  }

  Future<List<MortalidadDiaria>> getMortalidadDiariaByFecha(String fecha) async {
    final response = await _apiService.get('${mortalidadDiariaEndpoint}?fecha=$fecha');
    final List<dynamic> results = response['results'];
    return results.map((json) => MortalidadDiaria.fromJson(json)).toList();
  }

  Future<MortalidadDiaria> getMortalidadDiariaById(int id) async {
    final response = await _apiService.get('$mortalidadDiariaEndpoint$id/');
    return MortalidadDiaria.fromJson(response);
  }

  Future<MortalidadDiaria> createMortalidadDiaria(MortalidadDiaria mortalidad) async {
    final response = await _apiService.post(mortalidadDiariaEndpoint, mortalidad.toJson());
    return MortalidadDiaria.fromJson(response);
  }

  Future<MortalidadDiaria> updateMortalidadDiaria(MortalidadDiaria mortalidad) async {
    final response = await _apiService.put('$mortalidadDiariaEndpoint${mortalidad.id}/', mortalidad.toJson());
    return MortalidadDiaria.fromJson(response);
  }

  Future<void> deleteMortalidadDiaria(int id) async {
    await _apiService.delete('$mortalidadDiariaEndpoint$id/');
  }

  // Métodos para Mortalidad Semanal
  Future<List<MortalidadSemanal>> getMortalidadSemanal() async {
    final response = await _apiService.get(mortalidadSemanalEndpoint);
    final List<dynamic> results = response['results'];
    return results.map((json) => MortalidadSemanal.fromJson(json)).toList();
  }

  Future<List<MortalidadSemanal>> getMortalidadSemanalByLote(int loteId) async {
    final response = await _apiService.get('${mortalidadSemanalEndpoint}?lote=$loteId');
    final List<dynamic> results = response['results'];
    return results.map((json) => MortalidadSemanal.fromJson(json)).toList();
  }

  Future<MortalidadSemanal> getMortalidadSemanalById(int id) async {
    final response = await _apiService.get('$mortalidadSemanalEndpoint$id/');
    return MortalidadSemanal.fromJson(response);
  }

  Future<MortalidadSemanal> createMortalidadSemanal(MortalidadSemanal mortalidad) async {
    final response = await _apiService.post(mortalidadSemanalEndpoint, mortalidad.toJson());
    return MortalidadSemanal.fromJson(response);
  }

  Future<MortalidadSemanal> updateMortalidadSemanal(MortalidadSemanal mortalidad) async {
    final response = await _apiService.put('$mortalidadSemanalEndpoint${mortalidad.id}/', mortalidad.toJson());
    return MortalidadSemanal.fromJson(response);
  }

  Future<void> deleteMortalidadSemanal(int id) async {
    await _apiService.delete('$mortalidadSemanalEndpoint$id/');
  }
}
