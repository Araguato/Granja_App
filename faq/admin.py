from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import FAQCategory, FAQ


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FAQ)
class FAQAdmin(SummernoteModelAdmin):
    summernote_fields = ('answer',)
    list_display = ('question', 'category', 'is_published', 'order', 'updated_at')
    list_filter = ('category', 'is_published')
    search_fields = ('question', 'answer')
    date_hierarchy = 'created_at'
