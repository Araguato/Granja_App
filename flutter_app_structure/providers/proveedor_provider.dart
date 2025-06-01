import 'package:flutter/foundation.dart';
import '../models/proveedor_model.dart';
import '../services/proveedor_service.dart';

class ProveedorProvider with ChangeNotifier {
  final ProveedorService _proveedorService = ProveedorService();
  
  List<Proveedor> _proveedores = [];
  Proveedor? _selectedProveedor;
  bool _isLoading = false;
  String _error = '';

  // Getters
  List<Proveedor> get proveedores => _proveedores;
  Proveedor? get selectedProveedor => _selectedProveedor;
  bool get isLoading => _isLoading;
  String get error => _error;

  // Cargar todos los proveedores
  Future<void> loadProveedores() async {
    _setLoading(true);
    try {
      _proveedores = await _proveedorService.getProveedores();
      _error = '';
    } catch (e) {
      _error = 'Error al cargar proveedores: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Buscar proveedores por nombre
  Future<void> searchProveedores(String query) async {
    _setLoading(true);
    try {
      _proveedores = await _proveedorService.searchProveedores(query);
      _error = '';
    } catch (e) {
      _error = 'Error al buscar proveedores: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Seleccionar un proveedor
  void selectProveedor(int id) async {
    _setLoading(true);
    try {
      _selectedProveedor = await _proveedorService.getProveedor(id);
      _error = '';
    } catch (e) {
      _error = 'Error al seleccionar proveedor: ${e.toString()}';
      print(_error);
    } finally {
      _setLoading(false);
    }
  }

  // Crear un nuevo proveedor
  Future<bool> createProveedor(Proveedor proveedor) async {
    _setLoading(true);
    try {
      final newProveedor = await _proveedorService.createProveedor(proveedor);
      _proveedores.add(newProveedor);
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al crear proveedor: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Actualizar un proveedor existente
  Future<bool> updateProveedor(Proveedor proveedor) async {
    _setLoading(true);
    try {
      final updatedProveedor = await _proveedorService.updateProveedor(proveedor);
      final index = _proveedores.indexWhere((p) => p.id == proveedor.id);
      if (index != -1) {
        _proveedores[index] = updatedProveedor;
      }
      if (_selectedProveedor?.id == proveedor.id) {
        _selectedProveedor = updatedProveedor;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al actualizar proveedor: ${e.toString()}';
      print(_error);
      return false;
    } finally {
      _setLoading(false);
    }
  }

  // Eliminar un proveedor
  Future<bool> deleteProveedor(int id) async {
    _setLoading(true);
    try {
      await _proveedorService.deleteProveedor(id);
      _proveedores.removeWhere((p) => p.id == id);
      if (_selectedProveedor?.id == id) {
        _selectedProveedor = null;
      }
      _error = '';
      return true;
    } catch (e) {
      _error = 'Error al eliminar proveedor: ${e.toString()}';
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
