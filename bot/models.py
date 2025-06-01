from django.db import models
from django.conf import settings


class BotIntent(models.Model):
    """Intenciones que el bot puede reconocer"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    
    class Meta:
        verbose_name = "Intención del Bot"
        verbose_name_plural = "Intenciones del Bot"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class BotTrainingPhrase(models.Model):
    """Frases de entrenamiento para reconocer intenciones"""
    intent = models.ForeignKey(BotIntent, on_delete=models.CASCADE, related_name='training_phrases',
                              verbose_name="Intención")
    text = models.CharField(max_length=255, verbose_name="Texto")
    
    class Meta:
        verbose_name = "Frase de Entrenamiento"
        verbose_name_plural = "Frases de Entrenamiento"
    
    def __str__(self):
        return f"{self.text} ({self.intent.name})"


class BotResponse(models.Model):
    """Respuestas del bot para cada intención"""
    intent = models.ForeignKey(BotIntent, on_delete=models.CASCADE, related_name='responses',
                              verbose_name="Intención")
    text = models.TextField(verbose_name="Texto de Respuesta")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    
    class Meta:
        verbose_name = "Respuesta del Bot"
        verbose_name_plural = "Respuestas del Bot"
        ordering = ['intent', 'order']
    
    def __str__(self):
        return f"Respuesta para {self.intent.name}"


class BotConversation(models.Model):
    """Registro de conversaciones con el bot"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                            related_name='bot_conversations', verbose_name="Usuario")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Hora de Inicio")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Hora de Finalización")
    feedback_rating = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Calificación (1-5)")
    
    class Meta:
        verbose_name = "Conversación"
        verbose_name_plural = "Conversaciones"
        ordering = ['-start_time']
    
    def __str__(self):
        return f"Conversación {self.id} - {self.user or 'Usuario Anónimo'}"


class BotMessage(models.Model):
    """Mensajes individuales en una conversación"""
    SENDER_CHOICES = [
        ('USER', 'Usuario'),
        ('BOT', 'Bot'),
    ]
    
    conversation = models.ForeignKey(BotConversation, on_delete=models.CASCADE, related_name='messages',
                                    verbose_name="Conversación")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Remitente")
    text = models.TextField(verbose_name="Texto")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Marca de Tiempo")
    detected_intent = models.ForeignKey(BotIntent, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='messages', verbose_name="Intención Detectada")
    
    class Meta:
        verbose_name = "Mensaje"
        verbose_name_plural = "Mensajes"
        ordering = ['conversation', 'timestamp']
    
    def __str__(self):
        return f"{self.get_sender_display()}: {self.text[:50]}..."
