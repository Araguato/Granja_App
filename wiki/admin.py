from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Article, Attachment


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'order')
    list_filter = ('parent',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'category', 'author', 'updated_at', 'is_published', 'views')
    list_filter = ('category', 'is_published', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    inlines = [AttachmentInline]


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'uploaded_at')
    list_filter = ('article__category',)
    search_fields = ('name', 'description', 'article__title')
