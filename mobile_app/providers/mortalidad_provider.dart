import 'package:flutter/foundation.dart';
import '../models/mortalidad_model.dart';
import '../services/mortalidad_service.dart';

class MortalidadProvider with ChangeNotifier {
  final MortalidadService _mortalidadService = MortalidadService();
  
  // Estado para Mortalidad Diaria
  List<MortalidadDiaria> _mortalidadDiaria = [];
  MortalidadDiaria? _selectedMortalidadDiaria;
  
  // Estado para Mortalidad Semanal
  List<MortalidadSemanal> _mortalidadSemanal = [];
  MortalidadSemanal? _selectedMortalidadSemanal;
  
  // Estado general
  bool _isLoading = false;
  String _error = '';

  // Getters para Mortalidad Diaria
  List<MortalidadDiaria> get mortalidadDiaria => _mortalidadDiaria;
  MortalidadDiaria? get selectedMortalidadDiaria => _selectedMortalidadDiaria;
  
  // Getters para Mortalidad Semanal
  List<MortalidadSemanal> get mortalidadSemanal => _mortalidadSemanal;
  MortalidadSemanal? get selectedMortalidadSemanal => _selectedMortalidadSemanal;
  
  // Getters generales
  bool get isLoading => _isLoading;
  String get error => _error;

  // Métodos para Mortalidad Diaria
  Future<void> loadMortalidadDiaria() async {
    _setLoading(true);
    try {
      _mortalidadDiaria = await _mortalidadService.getMortalidadDiaria();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar mortalidad diaria: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> loadMortalidadDiariaByLote(int loteId) async {
    _setLoading(true);
    try {
      _mortalidadDiaria = await _mortalidadService.getMortalidadDiariaByLote(loteId);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar mortalidad diaria por lote: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> loadMortalidadDiariaByFecha(String fecha) async {
    _setLoading(true);
    try {
      _mortalidadDiaria = await _mortalidadService.getMortalidadDiariaByFecha(fecha);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar mortalidad diaria por fecha: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  void selectMortalidadDiaria(int id) async {
    _setLoading(true);
    try {
      _selectedMortalidadDiaria = await _mortalidadService.getMortalidadDiariaById(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar mortalidad diaria: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> createMortalidadDiaria(MortalidadDiaria mortalidad) async {
    _setLoading(true);
    try {
      final newMortalidad = await _mortalidadService.createMortalidadDiaria(mortalidad);
      _mortalidadDiaria.add(newMortalidad);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear registro de mortalidad diaria: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> updateMortalidadDiaria(MortalidadDiaria mortalidad) async {
    _setLoading(true);
    try {
      final updatedMortalidad = await _mortalidadService.updateMortalidadDiaria(mortalidad);
      final index = _mortalidadDiaria.indexWhere((m) => m.id == mortalidad.id);
      if (index != -1) {
        _mortalidadDiaria[index] = updatedMortalidad;
      }
      if (_selectedMortalidadDiaria?.id == mortalidad.id) {
        _selectedMortalidadDiaria = updatedMortalidad;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar registro de mortalidad diaria: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> deleteMortalidadDiaria(int id) async {
    _setLoading(true);
    try {
      await _mortalidadService.deleteMortalidadDiaria(id);
      _mortalidadDiaria.removeWhere((m) => m.id == id);
      if (_selectedMortalidadDiaria?.id == id) {
        _selectedMortalidadDiaria = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar registro de mortalidad diaria: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Métodos para Mortalidad Semanal
  Future<void> loadMortalidadSemanal() async {
    _setLoading(true);
    try {
      _mortalidadSemanal = await _mortalidadService.getMortalidadSemanal();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar mortalidad semanal: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  Future<void> loadMortalidadSemanalByLote(int loteId) async {
    _setLoading(true);
    try {
      _mortalidadSemanal = await _mortalidadService.getMortalidadSemanalByLote(loteId);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar mortalidad semanal por lote: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  void selectMortalidadSemanal(int id) async {
    _setLoading(true);
    try {
      _selectedMortalidadSemanal = await _mortalidadService.getMortalidadSemanalById(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar mortalidad semanal: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> createMortalidadSemanal(MortalidadSemanal mortalidad) async {
    _setLoading(true);
    try {
      final newMortalidad = await _mortalidadService.createMortalidadSemanal(mortalidad);
      _mortalidadSemanal.add(newMortalidad);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear registro de mortalidad semanal: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> updateMortalidadSemanal(MortalidadSemanal mortalidad) async {
    _setLoading(true);
    try {
      final updatedMortalidad = await _mortalidadService.updateMortalidadSemanal(mortalidad);
      final index = _mortalidadSemanal.indexWhere((m) => m.id == mortalidad.id);
      if (index != -1) {
        _mortalidadSemanal[index] = updatedMortalidad;
      }
      if (_selectedMortalidadSemanal?.id == mortalidad.id) {
        _selectedMortalidadSemanal = updatedMortalidad;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar registro de mortalidad semanal: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  Future<bool> deleteMortalidadSemanal(int id) async {
    _setLoading(true);
    try {
      await _mortalidadService.deleteMortalidadSemanal(id);
      _mortalidadSemanal.removeWhere((m) => m.id == id);
      if (_selectedMortalidadSemanal?.id == id) {
        _selectedMortalidadSemanal = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar registro de mortalidad semanal: ${e.toString()}';
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
