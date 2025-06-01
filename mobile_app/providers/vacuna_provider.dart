import 'package:flutter/foundation.dart';
import '../models/vacuna_model.dart';
import '../services/vacuna_service.dart';

class VacunaProvider with ChangeNotifier {
  final VacunaService _vacunaService = VacunaService();
  
  List<Vacuna> _vacunas = [];
  Vacuna? _selectedVacuna;
  bool _isLoading = false;
  String _error = '';

  // Getters
  List<Vacuna> get vacunas => _vacunas;
  Vacuna? get selectedVacuna => _selectedVacuna;
  bool get isLoading => _isLoading;
  String get error => _error;

  // Cargar todas las vacunas
  Future<void> loadVacunas() async {
    _setLoading(true);
    try {
      _vacunas = await _vacunaService.getVacunas();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar vacunas: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar vacunas por proveedor
  Future<void> loadVacunasByProveedor(int proveedorId) async {
    _setLoading(true);
    try {
      _vacunas = await _vacunaService.getVacunasByProveedor(proveedorId);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar vacunas por proveedor: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar vacunas por enfermedad
  Future<void> loadVacunasByEnfermedad(String enfermedad) async {
    _setLoading(true);
    try {
      _vacunas = await _vacunaService.getVacunasByEnfermedad(enfermedad);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar vacunas por enfermedad: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Seleccionar una vacuna
  void selectVacuna(int id) async {
    _setLoading(true);
    try {
      _selectedVacuna = await _vacunaService.getVacuna(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar vacuna: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Crear una nueva vacuna
  Future<bool> createVacuna(Vacuna vacuna) async {
    _setLoading(true);
    try {
      final newVacuna = await _vacunaService.createVacuna(vacuna);
      _vacunas.add(newVacuna);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear vacuna: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Actualizar una vacuna existente
  Future<bool> updateVacuna(Vacuna vacuna) async {
    _setLoading(true);
    try {
      final updatedVacuna = await _vacunaService.updateVacuna(vacuna);
      final index = _vacunas.indexWhere((v) => v.id == vacuna.id);
      if (index != -1) {
        _vacunas[index] = updatedVacuna;
      }
      if (_selectedVacuna?.id == vacuna.id) {
        _selectedVacuna = updatedVacuna;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar vacuna: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Eliminar una vacuna
  Future<bool> deleteVacuna(int id) async {
    _setLoading(true);
    try {
      await _vacunaService.deleteVacuna(id);
      _vacunas.removeWhere((v) => v.id == id);
      if (_selectedVacuna?.id == id) {
        _selectedVacuna = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar vacuna: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Método auxiliar para actualizar el estado de carga
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}
