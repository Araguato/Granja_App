import 'package:flutter/foundation.dart';
import '../models/galpon_model.dart';
import '../services/galpon_service.dart';

class GalponProvider with ChangeNotifier {
  List<Galpon> _galpones = [];
  bool _isLoading = false;
  String? _error;
  final GalponService _galponService = GalponService();

  List<Galpon> get galpones => [..._galpones];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Obtener todos los galpones
  Future<void> fetchGalpones() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _galpones = await _galponService.getGalpones();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener galpones por granja
  Future<void> fetchGalponesByGranja(int granjaId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _galpones = await _galponService.getGalponesByGranja(granjaId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener un galpon por ID
  Future<Galpon?> getGalponById(int id) async {
    try {
      // Primero buscar en la lista local
      final localGalpon = _galpones.firstWhere((galpon) => galpon.id == id);
      return localGalpon;
    } catch (_) {
      // Si no está en la lista local, buscar en la API
      try {
        return await _galponService.getGalpon(id);
      } catch (e) {
        _error = e.toString();
        notifyListeners();
        return null;
      }
    }
  }

  // Agregar un nuevo galpon
  Future<bool> addGalpon(Galpon galpon) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newGalpon = await _galponService.createGalpon(galpon);
      _galpones.add(newGalpon);
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

  // Actualizar un galpon existente
  Future<bool> updateGalpon(Galpon galpon) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final updatedGalpon = await _galponService.updateGalpon(galpon);
      final index = _galpones.indexWhere((g) => g.id == galpon.id);
      if (index >= 0) {
        _galpones[index] = updatedGalpon;
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

  // Eliminar un galpon
  Future<bool> deleteGalpon(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _galponService.deleteGalpon(id);
      _galpones.removeWhere((galpon) => galpon.id == id);
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
