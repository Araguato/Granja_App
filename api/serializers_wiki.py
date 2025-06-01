from rest_framework import serializers
from wiki.models import Category, Article, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'name', 'description', 'file', 'uploaded_at']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'parent', 'order', 'subcategories']
    
    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        if subcategories:
            return CategorySerializer(subcategories, many=True, context=self.context).data
        return []


class ArticleListSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'category', 'category_name', 
                 'author', 'author_name', 'created_at', 'updated_at', 
                 'is_published', 'views']
    
    def get_author_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return "Sistema"


class ArticleDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    author_name = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'category', 'category_name',
                 'author', 'author_name', 'created_at', 'updated_at', 
                 'is_published', 'views', 'attachments']
    
    def get_author_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        return "Sistema"
