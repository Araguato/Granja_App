from django.contrib import admin
from .models import BotIntent, BotTrainingPhrase, BotResponse, BotConversation, BotMessage


class BotTrainingPhraseInline(admin.TabularInline):
    model = BotTrainingPhrase
    extra = 3


class BotResponseInline(admin.TabularInline):
    model = BotResponse
    extra = 1


@admin.register(BotIntent)
class BotIntentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [BotTrainingPhraseInline, BotResponseInline]


class BotMessageInline(admin.TabularInline):
    model = BotMessage
    extra = 0
    readonly_fields = ('sender', 'text', 'timestamp', 'detected_intent')
    can_delete = False


@admin.register(BotConversation)
class BotConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'start_time', 'end_time', 'feedback_rating')
    list_filter = ('start_time', 'feedback_rating')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'start_time'
    inlines = [BotMessageInline]
    readonly_fields = ('start_time',)


@admin.register(BotMessage)
class BotMessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'text_preview', 'timestamp', 'detected_intent')
    list_filter = ('sender', 'detected_intent', 'timestamp')
    search_fields = ('text', 'conversation__user__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Texto'
