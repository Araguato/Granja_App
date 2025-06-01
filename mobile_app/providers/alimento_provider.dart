import 'package:flutter/foundation.dart';
import '../models/alimento_model.dart';
import '../services/alimento_service.dart';

class AlimentoProvider with ChangeNotifier {
  final AlimentoService _alimentoService = AlimentoService();
  
  List<Alimento> _alimentos = [];
  Alimento? _selectedAlimento;
  bool _isLoading = false;
  String _error = '';

  // Getters
  List<Alimento> get alimentos => _alimentos;
  Alimento? get selectedAlimento => _selectedAlimento;
  bool get isLoading => _isLoading;
  String get error => _error;

  // Cargar todos los alimentos
  Future<void> loadAlimentos() async {
    _setLoading(true);
    try {
      _alimentos = await _alimentoService.getAlimentos();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar alimentos: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar alimentos por etapa
  Future<void> loadAlimentosByEtapa(String etapa) async {
    _setLoading(true);
    try {
      _alimentos = await _alimentoService.getAlimentosByEtapa(etapa);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar alimentos por etapa: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Cargar alimentos por proveedor
  Future<void> loadAlimentosByProveedor(int proveedorId) async {
    _setLoading(true);
    try {
      _alimentos = await _alimentoService.getAlimentosByProveedor(proveedorId);
      _error = '';
    } catch (e) {
      _error = 'Error al cargar alimentos por proveedor: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Seleccionar un alimento
  void selectAlimento(int id) async {
    _setLoading(true);
    try {
      _selectedAlimento = await _alimentoService.getAlimento(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar alimento: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Crear un nuevo alimento
  Future<bool> createAlimento(Alimento alimento) async {
    _setLoading(true);
    try {
      final newAlimento = await _alimentoService.createAlimento(alimento);
      _alimentos.add(newAlimento);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear alimento: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Actualizar un alimento existente
  Future<bool> updateAlimento(Alimento alimento) async {
    _setLoading(true);
    try {
      final updatedAlimento = await _alimentoService.updateAlimento(alimento);
      final index = _alimentos.indexWhere((a) => a.id == alimento.id);
      if (index != -1) {
        _alimentos[index] = updatedAlimento;
      }
      if (_selectedAlimento?.id == alimento.id) {
        _selectedAlimento = updatedAlimento;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar alimento: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Eliminar un alimento
  Future<bool> deleteAlimento(int id) async {
    _setLoading(true);
    try {
      await _alimentoService.deleteAlimento(id);
      _alimentos.removeWhere((a) => a.id == id);
      if (_selectedAlimento?.id == id) {
        _selectedAlimento = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar alimento: ${e.toString()}';
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
