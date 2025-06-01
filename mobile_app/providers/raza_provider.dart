import 'package:flutter/foundation.dart';
import '../models/raza_model.dart';
import '../services/raza_service.dart';

class RazaProvider with ChangeNotifier {
  List<Raza> _razas = [];
  bool _isLoading = false;
  String? _error;
  final RazaService _razaService = RazaService();

  List<Raza> get razas => [..._razas];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Obtener todas las razas
  Future<void> fetchRazas() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _razas = await _razaService.getRazas();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener razas por tipo
  Future<void> fetchRazasByTipo(String tipoRaza) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _razas = await _razaService.getRazasByTipo(tipoRaza);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener una raza por ID
  Future<Raza?> getRazaById(int id) async {
    try {
      // Primero buscar en la lista local
      final localRaza = _razas.firstWhere((raza) => raza.id == id);
      return localRaza;
    } catch (_) {
      // Si no está en la lista local, buscar en la API
      try {
        return await _razaService.getRaza(id);
      } catch (e) {
        _error = e.toString();
        notifyListeners();
        return null;
      }
    }
  }

  // Agregar una nueva raza
  Future<bool> addRaza(Raza raza) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newRaza = await _razaService.createRaza(raza);
      _razas.add(newRaza);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Actualizar una raza existente
  Future<bool> updateRaza(Raza raza) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final updatedRaza = await _razaService.updateRaza(raza);
      final index = _razas.indexWhere((r) => r.id == raza.id);
      if (index >= 0) {
        _razas[index] = updatedRaza;
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Eliminar una raza
  Future<bool> deleteRaza(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _razaService.deleteRaza(id);
      _razas.removeWhere((raza) => raza.id == id);
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // Limpiar errores
  void clearError() {
    _error = null;
    notifyListeners();
  }
}
