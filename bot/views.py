from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .models import BotIntent, BotTrainingPhrase, BotResponse, BotConversation, BotMessage

@login_required
def bot_chat_view(request):
    """
    Vista principal para la interfaz de chat del bot.
    """
    # Obtener o crear una conversación activa para el usuario
    active_conversation = BotConversation.objects.filter(
        user=request.user,
        end_time__isnull=True
    ).first()
    
    if not active_conversation:
        active_conversation = BotConversation.objects.create(
            user=request.user,
            start_time=timezone.now()
        )
    
    # Obtener mensajes de la conversación activa
    messages = BotMessage.objects.filter(conversation=active_conversation).order_by('timestamp')
    
    # Si no hay mensajes, crear un mensaje de bienvenida
    if not messages.exists():
        # Buscar una intención de saludo
        saludo_intent = BotIntent.objects.filter(name='saludo').first()
        
        if saludo_intent:
            # Obtener una respuesta de saludo
            saludo_response = BotResponse.objects.filter(intent=saludo_intent).first()
            
            if saludo_response:
                # Crear mensaje de bienvenida del bot
                BotMessage.objects.create(
                    conversation=active_conversation,
                    sender='BOT',
                    text=saludo_response.text,
                    timestamp=timezone.now(),
                    detected_intent=saludo_intent
                )
        
        # Recargar los mensajes
        messages = BotMessage.objects.filter(conversation=active_conversation).order_by('timestamp')
    
    context = {
        'conversation': active_conversation,
        'messages': messages,
        'title': 'Asistente Virtual'
    }
    
    return render(request, 'bot/chat.html', context)

@login_required
@csrf_exempt
def send_message_view(request):
    """
    Vista para enviar un mensaje al bot y recibir respuesta.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_text = data.get('message', '').strip()
            conversation_id = data.get('conversation_id')
            
            if not message_text or not conversation_id:
                return JsonResponse({'error': 'Mensaje o ID de conversación no proporcionados'}, status=400)
            
            # Obtener la conversación
            try:
                conversation = BotConversation.objects.get(id=conversation_id, user=request.user)
            except BotConversation.DoesNotExist:
                return JsonResponse({'error': 'Conversación no encontrada'}, status=404)
            
            # Crear mensaje del usuario
            user_message = BotMessage.objects.create(
                conversation=conversation,
                sender='USER',
                text=message_text,
                timestamp=timezone.now()
            )
            
            # Detectar intención (simulado - en producción usaríamos un modelo NLP)
            detected_intent = None
            best_match_score = 0
            
            # Búsqueda simple de coincidencia con frases de entrenamiento
            for intent in BotIntent.objects.all():
                for phrase in intent.training_phrases.all():
                    if phrase.text.lower() in message_text.lower():
                        # Si hay coincidencia exacta, asignar esta intención
                        detected_intent = intent
                        best_match_score = 1
                        break
                
                if best_match_score == 1:
                    break
            
            # Obtener una respuesta apropiada
            bot_response_text = "Lo siento, no entiendo esa pregunta."
            
            if detected_intent:
                # Actualizar la intención detectada en el mensaje del usuario
                user_message.detected_intent = detected_intent
                user_message.save()
                
                # Obtener una respuesta para la intención detectada
                bot_response = BotResponse.objects.filter(intent=detected_intent).order_by('?').first()
                
                if bot_response:
                    bot_response_text = bot_response.text
            
            # Crear mensaje de respuesta del bot
            bot_message = BotMessage.objects.create(
                conversation=conversation,
                sender='BOT',
                text=bot_response_text,
                timestamp=timezone.now(),
                detected_intent=detected_intent
            )
            
            # Devolver los mensajes
            return JsonResponse({
                'user_message': {
                    'id': user_message.id,
                    'text': user_message.text,
                    'timestamp': user_message.timestamp.isoformat(),
                    'sender': user_message.sender
                },
                'bot_message': {
                    'id': bot_message.id,
                    'text': bot_message.text,
                    'timestamp': bot_message.timestamp.isoformat(),
                    'sender': bot_message.sender,
                    'detected_intent': detected_intent.name if detected_intent else None
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def end_conversation_view(request, conversation_id):
    """
    Vista para finalizar una conversación.
    """
    try:
        conversation = BotConversation.objects.get(id=conversation_id, user=request.user)
        conversation.end_time = timezone.now()
        
        # Obtener calificación si se proporciona
        feedback = request.GET.get('feedback')
        if feedback and feedback.isdigit() and 1 <= int(feedback) <= 5:
            conversation.feedback_rating = int(feedback)
        
        conversation.save()
        
        return JsonResponse({'success': True})
    except BotConversation.DoesNotExist:
        return JsonResponse({'error': 'Conversación no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def conversation_history_view(request):
    """
    Vista para mostrar el historial de conversaciones del usuario.
    """
    conversations = BotConversation.objects.filter(user=request.user).order_by('-start_time')
    
    context = {
        'conversations': conversations,
        'title': 'Historial de Conversaciones'
    }
    
    return render(request, 'bot/history.html', context)
