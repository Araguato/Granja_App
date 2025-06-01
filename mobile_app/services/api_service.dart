import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiService {
  // URL base de la API (configurable)
  String baseUrl;
  
  // Instancia para almacenamiento seguro de tokens
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  
  // Constructor
  ApiService({String? apiUrl}) : 
    baseUrl = apiUrl ?? 'http://10.0.2.2:8000/api/'; // Por defecto usa la dirección para emulador Android
  
  // Método para cambiar la URL base (útil para conectar con diferentes servidores)
  Future<void> setBaseUrl(String url) async {
    baseUrl = url;
    await _secureStorage.write(key: 'api_url', value: url);
  }
  
  // Método para obtener la URL base guardada
  Future<String> getBaseUrl() async {
    final savedUrl = await _secureStorage.read(key: 'api_url');
    return savedUrl ?? baseUrl;
  }
  
  // Headers comunes para todas las peticiones
  Future<Map<String, String>> _getHeaders() async {
    final token = await _secureStorage.read(key: 'access_token');
    return {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
  
  // Método para login
  Future<Map<String, dynamic>> login(String username, String password) async {
    final url = await getBaseUrl();
    final response = await http.post(
      Uri.parse('${url}token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      // Guardar tokens
      await _secureStorage.write(key: 'access_token', value: data['access']);
      await _secureStorage.write(key: 'refresh_token', value: data['refresh']);
      return data;
    } else {
      throw Exception('Error en la autenticación: ${response.body}');
    }
  }
  
  // Método para refrescar token
  Future<void> refreshToken() async {
    final refreshToken = await _secureStorage.read(key: 'refresh_token');
    if (refreshToken == null) {
      throw Exception('No hay token de refresco disponible');
    }
    
    final url = await getBaseUrl();
    final response = await http.post(
      Uri.parse('${url}token/refresh/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'refresh': refreshToken,
      }),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      await _secureStorage.write(key: 'access_token', value: data['access']);
    } else {
      // Si no se puede refrescar, cerrar sesión
      await logout();
      throw Exception('No se pudo refrescar el token: ${response.body}');
    }
  }
  
  // Método para logout
  Future<void> logout() async {
    await _secureStorage.delete(key: 'access_token');
    await _secureStorage.delete(key: 'refresh_token');
  }
  
  // Método genérico para GET
  Future<dynamic> get(String endpoint) async {
    try {
      final url = await getBaseUrl();
      final response = await http.get(
        Uri.parse('$url$endpoint'),
        headers: await _getHeaders(),
      );
      
      return _handleResponse(response);
    } on SocketException {
      throw Exception('No hay conexión a internet');
    } catch (e) {
      throw Exception('Error en la petición GET: $e');
    }
  }
  
  // Método genérico para POST
  Future<dynamic> post(String endpoint, Map<String, dynamic> data) async {
    try {
      final url = await getBaseUrl();
      final response = await http.post(
        Uri.parse('$url$endpoint'),
        headers: await _getHeaders(),
        body: jsonEncode(data),
      );
      
      return _handleResponse(response);
    } on SocketException {
      throw Exception('No hay conexión a internet');
    } catch (e) {
      throw Exception('Error en la petición POST: $e');
    }
  }
  
  // Método genérico para PUT
  Future<dynamic> put(String endpoint, Map<String, dynamic> data) async {
    try {
      final url = await getBaseUrl();
      final response = await http.put(
        Uri.parse('$url$endpoint'),
        headers: await _getHeaders(),
        body: jsonEncode(data),
      );
      
      return _handleResponse(response);
    } on SocketException {
      throw Exception('No hay conexión a internet');
    } catch (e) {
      throw Exception('Error en la petición PUT: $e');
    }
  }
  
  // Método genérico para DELETE
  Future<dynamic> delete(String endpoint) async {
    try {
      final url = await getBaseUrl();
      final response = await http.delete(
        Uri.parse('$url$endpoint'),
        headers: await _getHeaders(),
      );
      
      return _handleResponse(response);
    } on SocketException {
      throw Exception('No hay conexión a internet');
    } catch (e) {
      throw Exception('Error en la petición DELETE: $e');
    }
  }
  
  // Manejo de respuestas
  dynamic _handleResponse(http.Response response) async {
    if (response.statusCode >= 200 && response.statusCode < 300) {
      // Éxito
      if (response.body.isNotEmpty) {
        return jsonDecode(response.body);
      }
      return null;
    } else if (response.statusCode == 401) {
      // Token expirado, intentar refrescar
      try {
        await refreshToken();
        // Reintentar la petición original
        // Aquí deberíamos implementar la lógica para reintentar la petición original
        throw Exception('Token expirado, por favor reintente la operación');
      } catch (e) {
        throw Exception('Sesión expirada, por favor inicie sesión nuevamente');
      }
    } else {
      // Otros errores
      throw Exception('Error ${response.statusCode}: ${response.body}');
    }
  }
}
