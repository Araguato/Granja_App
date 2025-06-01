import 'package:flutter/foundation.dart';
import '../models/lote_model.dart';
import '../services/lote_service.dart';

class LoteProvider with ChangeNotifier {
  List<Lote> _lotes = [];
  bool _isLoading = false;
  String? _error;
  final LoteService _loteService = LoteService();

  List<Lote> get lotes => [..._lotes];
  bool get isLoading => _isLoading;
  String? get error => _error;

  // Obtener todos los lotes
  Future<void> fetchLotes() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lotes = await _loteService.getLotes();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener lotes por galpon
  Future<void> fetchLotesByGalpon(int galponId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lotes = await _loteService.getLotesByGalpon(galponId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener lotes por raza
  Future<void> fetchLotesByRaza(int razaId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lotes = await _loteService.getLotesByRaza(razaId);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener lotes por estado
  Future<void> fetchLotesByEstado(String estado) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _lotes = await _loteService.getLotesByEstado(estado);
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Obtener un lote por ID
  Future<Lote?> getLoteById(int id) async {
    try {
      // Primero buscar en la lista local
      final localLote = _lotes.firstWhere((lote) => lote.id == id);
      return localLote;
    } catch (_) {
      // Si no está en la lista local, buscar en la API
      try {
        return await _loteService.getLote(id);
      } catch (e) {
        _error = e.toString();
        notifyListeners();
        return null;
      }
    }
  }

  // Agregar un nuevo lote
  Future<bool> addLote(Lote lote) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final newLote = await _loteService.createLote(lote);
      _lotes.add(newLote);
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

  // Actualizar un lote existente
  Future<bool> updateLote(Lote lote) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final updatedLote = await _loteService.updateLote(lote);
      final index = _lotes.indexWhere((l) => l.id == lote.id);
      if (index >= 0) {
        _lotes[index] = updatedLote;
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

  // Eliminar un lote
  Future<bool> deleteLote(int id) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await _loteService.deleteLote(id);
      _lotes.removeWhere((lote) => lote.id == id);
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
