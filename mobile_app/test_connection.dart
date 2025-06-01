import 'dart:convert';
import 'package:http/http.dart' as http;

// Función para probar la conexión con el servidor Django
Future<Map<String, dynamic>> testConnection(String baseUrl) async {
  try {
    // Asegúrate de que la URL termine con '/'
    if (!baseUrl.endsWith('/')) {
      baseUrl = '$baseUrl/';
    }
    
    // Intenta acceder a la raíz de la API
    final response = await http.get(
      Uri.parse(baseUrl),
      headers: {'Content-Type': 'application/json'},
    ).timeout(const Duration(seconds: 10));
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      // Conexión exitosa
      return {
        'success': true,
        'message': 'Conexión exitosa al servidor',
        'status_code': response.statusCode,
        'data': _tryParseJson(response.body),
      };
    } else {
      // El servidor respondió, pero con un error
      return {
        'success': false,
        'message': 'El servidor respondió con un error',
        'status_code': response.statusCode,
        'data': _tryParseJson(response.body),
      };
    }
  } catch (e) {
    // Error de conexión
    return {
      'success': false,
      'message': 'Error de conexión: ${e.toString()}',
      'status_code': null,
      'data': null,
    };
  }
}

// Función para probar la autenticación con el servidor Django
Future<Map<String, dynamic>> testAuthentication(String baseUrl, String username, String password) async {
  try {
    // Asegúrate de que la URL termine con '/'
    if (!baseUrl.endsWith('/')) {
      baseUrl = '$baseUrl/';
    }
    
    // Intenta autenticarse con el servidor
    final response = await http.post(
      Uri.parse('${baseUrl}token/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'username': username,
        'password': password,
      }),
    ).timeout(const Duration(seconds: 10));
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      // Autenticación exitosa
      final data = jsonDecode(response.body);
      return {
        'success': true,
        'message': 'Autenticación exitosa',
        'status_code': response.statusCode,
        'data': data,
      };
    } else {
      // El servidor respondió, pero con un error de autenticación
      return {
        'success': false,
        'message': 'Error de autenticación',
        'status_code': response.statusCode,
        'data': _tryParseJson(response.body),
      };
    }
  } catch (e) {
    // Error de conexión
    return {
      'success': false,
      'message': 'Error de conexión: ${e.toString()}',
      'status_code': null,
      'data': null,
    };
  }
}

// Función auxiliar para intentar parsear JSON
dynamic _tryParseJson(String text) {
  try {
    return jsonDecode(text);
  } catch (e) {
    return text;
  }
}

// Función principal para ejecutar las pruebas
Future<void> main() async {
  // URL del servidor Django (cambia esto según tu configuración)
  const String baseUrl = 'http://10.0.2.2:8000/api/';
  const String username = 'admin';
  const String password = 'admin';
  
  print('Probando conexión con el servidor: $baseUrl');
  final connectionResult = await testConnection(baseUrl);
  print('Resultado de la conexión:');
  print('  Éxito: ${connectionResult['success']}');
  print('  Mensaje: ${connectionResult['message']}');
  print('  Código de estado: ${connectionResult['status_code']}');
  
  if (connectionResult['success']) {
    print('\nProbando autenticación con el servidor');
    final authResult = await testAuthentication(baseUrl, username, password);
    print('Resultado de la autenticación:');
    print('  Éxito: ${authResult['success']}');
    print('  Mensaje: ${authResult['message']}');
    print('  Código de estado: ${authResult['status_code']}');
    
    if (authResult['success']) {
      print('  Token de acceso: ${authResult['data']['access']}');
    } else {
      print('  Error: ${authResult['data']}');
    }
  }
}
