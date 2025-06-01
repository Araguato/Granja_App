import 'package:flutter/foundation.dart';
import '../models/user_model.dart';
import '../services/api_service.dart';

class AuthProvider with ChangeNotifier {
  User? _currentUser;
  bool _isLoading = false;
  String? _error;
  final ApiService _apiService = ApiService();

  User? get currentUser => _currentUser;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _currentUser != null;
  String? get error => _error;

  // Método para iniciar sesión
  Future<bool> login(String username, String password) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.login(username, password);
      
      // Obtener información del usuario
      final userData = await _apiService.get('usuarios/me/');
      _currentUser = User.fromJson(userData);
      
      // Asignar tokens al usuario
      _currentUser!.token = response['access'];
      _currentUser!.refreshToken = response['refresh'];
      
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _isLoading = false;
      _error = e.toString();
      notifyListeners();
      return false;
    }
  }

  // Método para cerrar sesión
  Future<void> logout() async {
    _isLoading = true;
    notifyListeners();

    try {
      await _apiService.logout();
      _currentUser = null;
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Método para verificar si el usuario está autenticado
  Future<bool> checkAuth() async {
    try {
      // Intentar obtener información del usuario actual
      final userData = await _apiService.get('usuarios/me/');
      _currentUser = User.fromJson(userData);
      notifyListeners();
      return true;
    } catch (e) {
      // Si hay error, el usuario no está autenticado o el token expiró
      _currentUser = null;
      notifyListeners();
      return false;
    }
  }

  // Método para limpiar errores
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
