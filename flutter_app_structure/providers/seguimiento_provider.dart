import 'package:flutter/foundation.dart';
import '../models/seguimiento_diario_model.dart';
import '../services/seguimiento_service.dart';

class SeguimientoProvider with ChangeNotifier {
  final SeguimientoService _seguimientoService = SeguimientoService();
  
  List<SeguimientoDiario> _seguimientos = [];
  SeguimientoDiario? _selectedSeguimiento;
  bool _isLoading = false;
  String _error = '';

  // Getters
  List<SeguimientoDiario> get seguimientos => _seguimientos;
  SeguimientoDiario? get selectedSeguimiento => _selectedSeguimiento;
  bool get isLoading => _isLoading;
  String get error => _error;

  // Cargar todos los seguimientos
  Future<void> loadSeguimientos() async {
    _setLoading(true);
    try {
      _seguimientos = await _seguimientoService.getSeguimientos();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar seguimientos: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar seguimientos por lote
  Future<void> loadSeguimientosByLote(int loteId) async {
    _setLoading(true);
    try {
      _seguimientos = await _seguimientoService.getSeguimientosByLote(loteId);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar seguimientos por lote: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar seguimientos por fecha
  Future<void> loadSeguimientosByFecha(String fecha) async {
    _setLoading(true);
    try {
      _seguimientos = await _seguimientoService.getSeguimientosByFecha(fecha);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar seguimientos por fecha: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar seguimientos por tipo
  Future<void> loadSeguimientosByTipo(String tipo) async {
    _setLoading(true);
    try {
      _seguimientos = await _seguimientoService.getSeguimientosByTipo(tipo);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar seguimientos por tipo: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Seleccionar un seguimiento
  void selectSeguimiento(int id) async {
    _setLoading(true);
    try {
      _selectedSeguimiento = await _seguimientoService.getSeguimiento(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar seguimiento: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Crear un nuevo seguimiento
  Future<bool> createSeguimiento(SeguimientoDiario seguimiento) async {
    _setLoading(true);
    try {
      final newSeguimiento = await _seguimientoService.createSeguimiento(seguimiento);
      _seguimientos.add(newSeguimiento);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear seguimiento: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Actualizar un seguimiento existente
  Future<bool> updateSeguimiento(SeguimientoDiario seguimiento) async {
    _setLoading(true);
    try {
      final updatedSeguimiento = await _seguimientoService.updateSeguimiento(seguimiento);
      final index = _seguimientos.indexWhere((s) => s.id == seguimiento.id);
      if (index != -1) {
        _seguimientos[index] = updatedSeguimiento;
      }
      if (_selectedSeguimiento?.id == seguimiento.id) {
        _selectedSeguimiento = updatedSeguimiento;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar seguimiento: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Eliminar un seguimiento
  Future<bool> deleteSeguimiento(int id) async {
    _setLoading(true);
    try {
      await _seguimientoService.deleteSeguimiento(id);
      _seguimientos.removeWhere((s) => s.id == id);
      if (_selectedSeguimiento?.id == id) {
        _selectedSeguimiento = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar seguimiento: ${e.toString()}';
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
