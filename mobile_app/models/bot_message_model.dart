class BotMessageModel {
  final int? id;
  final int conversationId;
  final String sender;
  final String text;
  final DateTime timestamp;
  final String? detectedIntent;

  BotMessageModel({
    this.id,
    required this.conversationId,
    required this.sender,
    required this.text,
    required this.timestamp,
    this.detectedIntent,
  });

  factory BotMessageModel.fromJson(Map<String, dynamic> json) {
    return BotMessageModel(
      id: json['id'],
      conversationId: json['conversation'],
      sender: json['sender'],
      text: json['text'],
      timestamp: DateTime.parse(json['timestamp']),
      detectedIntent: json['detected_intent'] != null 
          ? json['detected_intent']['name'] 
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'conversation': conversationId,
      'sender': sender,
      'text': text,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}

class BotConversationModel {
  final int? id;
  final int? userId;
  final DateTime startTime;
  final DateTime? endTime;
  final int? feedbackRating;
  final List<BotMessageModel> messages;

  BotConversationModel({
    this.id,
    this.userId,
    required this.startTime,
    this.endTime,
    this.feedbackRating,
    this.messages = const [],
  });

  factory BotConversationModel.fromJson(Map<String, dynamic> json) {
    List<BotMessageModel> messagesList = [];
    if (json['messages'] != null) {
      messagesList = (json['messages'] as List)
          .map((message) => BotMessageModel.fromJson(message))
          .toList();
    }

    return BotConversationModel(
      id: json['id'],
      userId: json['user'],
      startTime: DateTime.parse(json['start_time']),
      endTime: json['end_time'] != null ? DateTime.parse(json['end_time']) : null,
      feedbackRating: json['feedback_rating'],
      messages: messagesList,
    );
  }
}
