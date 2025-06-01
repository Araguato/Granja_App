import 'package:flutter/foundation.dart';
import '../models/granja_model.dart';
import '../services/granja_service.dart';

class GranjaProvider with ChangeNotifier {
  List<Granja> _granjas = [];
  bool _isLoading = false;
  String? _error;
  final GranjaService _granjaService = GranjaService();

  List<Granja> get granjas => [..._granjas];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Obtener todas las granjas
  Future<void> fetchGranjas() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _granjas = await _granjaService.getGranjas();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener una granja por ID
  Future<Granja?> getGranjaById(int id) async {
    try {
      // Primero buscar en la lista local
      final localGranja = _granjas.firstWhere((granja) => granja.id == id);
      return localGranja;
    } catch (_) {
      // Si no está en la lista local, buscar en la API
      try {
        return await _granjaService.getGranja(id);
      } catch (e) {
        _error = e.toString();
        notifyListeners();
        return null;
      }
    }
  }

  // Agregar una nueva granja
  Future<bool> addGranja(Granja granja) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newGranja = await _granjaService.createGranja(granja);
      _granjas.add(newGranja);
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

  // Actualizar una granja existente
  Future<bool> updateGranja(Granja granja) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final updatedGranja = await _granjaService.updateGranja(granja);
      final index = _granjas.indexWhere((g) => g.id == granja.id);
      if (index >= 0) {
        _granjas[index] = updatedGranja;
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

  // Eliminar una granja
  Future<bool> deleteGranja(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _granjaService.deleteGranja(id);
      _granjas.removeWhere((granja) => granja.id == id);
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
