from rest_framework import serializers
from bot.models import BotIntent, BotTrainingPhrase, BotResponse, BotConversation, BotMessage


class BotResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotResponse
        fields = ['id', 'text', 'order']


class BotTrainingPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotTrainingPhrase
        fields = ['id', 'text']


class BotIntentSerializer(serializers.ModelSerializer):
    training_phrases = BotTrainingPhraseSerializer(many=True, read_only=True)
    responses = BotResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = BotIntent
        fields = ['id', 'name', 'description', 'training_phrases', 'responses']


class BotMessageSerializer(serializers.ModelSerializer):
    intent_name = serializers.ReadOnlyField(source='detected_intent.name', default=None)
    
    class Meta:
        model = BotMessage
        fields = ['id', 'sender', 'text', 'timestamp', 'detected_intent', 'intent_name']


class BotConversationSerializer(serializers.ModelSerializer):
    messages = BotMessageSerializer(many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BotConversation
        fields = ['id', 'user', 'user_name', 'start_time', 'end_time', 'feedback_rating', 'messages']
    
    def get_user_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
        return "Usuario Anónimo"


class BotMessageCreateSerializer(serializers.ModelSerializer):
    """Serializador para crear un nuevo mensaje de usuario y obtener respuesta del bot"""
    
    class Meta:
        model = BotMessage
        fields = ['conversation', 'text']
        
    def create(self, validated_data):
        # Crear el mensaje del usuario
        conversation = validated_data['conversation']
        user_message = BotMessage.objects.create(
            conversation=conversation,
            sender='USER',
            text=validated_data['text']
        )
        
        # Aquí iría la lógica para procesar el mensaje y determinar la intención
        # Por ahora, simplemente devolvemos una respuesta genérica
        
        # Crear respuesta del bot
        BotMessage.objects.create(
            conversation=conversation,
            sender='BOT',
            text="Gracias por tu mensaje. Estoy procesando tu solicitud."
        )
        
        return user_message
