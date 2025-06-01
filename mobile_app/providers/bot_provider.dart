import 'package:flutter/foundation.dart';
import '../models/bot_message_model.dart';
import '../services/bot_service.dart';

class BotProvider with ChangeNotifier {
  final BotService _botService;
  
  BotConversationModel? _currentConversation;
  List<BotMessageModel> _messages = [];
  bool _isLoading = false;
  String? _error;

  BotProvider(this._botService);

  // Getters
  BotConversationModel? get currentConversation => _currentConversation;
  List<BotMessageModel> get currentMessages => _messages;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get hasActiveConversation => _currentConversation != null;

  // Iniciar una nueva conversación
  Future<void> startNewConversation() async {
    _setLoading(true);
    _clearError();
    
    try {
      _currentConversation = await _botService.startConversation();
      _messages = [];
      notifyListeners();
    } catch (e) {
      _setError('Error al iniciar conversación: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Enviar un mensaje al bot
  Future<void> sendMessage(String text) async {
    if (_currentConversation == null) {
      await startNewConversation();
      if (_currentConversation == null) {
        return; // No se pudo iniciar la conversación
      }
    }

    _setLoading(true);
    _clearError();
    
    try {
      // Añadir el mensaje del usuario inmediatamente para mejor UX
      final userMessage = BotMessageModel(
        conversationId: _currentConversation!.id!,
        sender: 'USER',
        text: text,
        timestamp: DateTime.now(),
      );
      
      _messages.add(userMessage);
      notifyListeners();
      
      // Enviar el mensaje al servidor
      final botResponse = await _botService.sendMessage(_currentConversation!.id!, text);
      
      // Obtener los mensajes actualizados
      _messages = await _botService.getMessages(_currentConversation!.id!);
      notifyListeners();
    } catch (e) {
      _setError('Error al enviar mensaje: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Finalizar la conversación actual
  Future<void> endCurrentConversation({int? feedbackRating}) async {
    if (_currentConversation == null) return;
    
    _setLoading(true);
    _clearError();
    
    try {
      await _botService.endConversation(
        _currentConversation!.id!,
        feedbackRating: feedbackRating,
      );
      
      // Actualizar el estado local
      _currentConversation = null;
      _messages = [];
      notifyListeners();
    } catch (e) {
      _setError('Error al finalizar conversación: $e');
    } finally {
      _setLoading(false);
    }
  }

  // Obtener el historial de conversaciones
  Future<List<BotConversationModel>> getConversationHistory() async {
    _setLoading(true);
    _clearError();
    
    try {
      final history = await _botService.getConversationHistory();
      return history;
    } catch (e) {
      _setError('Error al obtener historial: $e');
      return [];
    } finally {
      _setLoading(false);
    }
  }

  // Helpers
  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }

  void _setError(String errorMessage) {
    _error = errorMessage;
    notifyListeners();
  }

  void _clearError() {
    _error = null;
  }
}
