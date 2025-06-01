import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/bot_message_model.dart';
import 'api_service.dart';

class BotService {
  final ApiService _apiService;
  final String _baseUrl = '/api/bot/conversaciones';

  BotService(this._apiService);

  /// Inicia una nueva conversación con el bot
  Future<BotConversationModel> startConversation() async {
    try {
      final response = await _apiService.post(
        '$_baseUrl/',
        body: json.encode({}),
      );

      if (response.statusCode == 201) {
        return BotConversationModel.fromJson(json.decode(response.body));
      } else {
        throw Exception('Error al iniciar conversación: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Envía un mensaje al bot en una conversación existente
  Future<BotMessageModel> sendMessage(int conversationId, String text) async {
    try {
      final response = await _apiService.post(
        '$_baseUrl/$conversationId/mensajes/',
        body: json.encode({
          'text': text,
          'sender': 'USER',
        }),
      );

      if (response.statusCode == 201) {
        // La API debería devolver tanto el mensaje del usuario como la respuesta del bot
        return BotMessageModel.fromJson(json.decode(response.body));
      } else {
        throw Exception('Error al enviar mensaje: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Obtiene los mensajes de una conversación
  Future<List<BotMessageModel>> getMessages(int conversationId) async {
    try {
      final response = await _apiService.get('$_baseUrl/$conversationId/mensajes/');

      if (response.statusCode == 200) {
        final List<dynamic> messagesJson = json.decode(response.body);
        return messagesJson
            .map((json) => BotMessageModel.fromJson(json))
            .toList();
      } else {
        throw Exception('Error al obtener mensajes: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Finaliza una conversación existente
  Future<void> endConversation(int conversationId, {int? feedbackRating}) async {
    try {
      final Map<String, dynamic> data = {
        'end_time': DateTime.now().toIso8601String(),
      };
      
      if (feedbackRating != null) {
        data['feedback_rating'] = feedbackRating;
      }

      final response = await _apiService.patch(
        '$_baseUrl/$conversationId/',
        body: json.encode(data),
      );

      if (response.statusCode != 200) {
        throw Exception('Error al finalizar conversación: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  /// Obtiene el historial de conversaciones
  Future<List<BotConversationModel>> getConversationHistory() async {
    try {
      final response = await _apiService.get('$_baseUrl/');

      if (response.statusCode == 200) {
        final List<dynamic> conversationsJson = json.decode(response.body);
        return conversationsJson
            .map((json) => BotConversationModel.fromJson(json))
            .toList();
      } else {
        throw Exception('Error al obtener historial: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }
}
