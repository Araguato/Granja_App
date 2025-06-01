from rest_framework import serializers
from faq.models import FAQCategory, FAQ


class FAQSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'category_name', 'order', 'is_published']


class FAQCategorySerializer(serializers.ModelSerializer):
    faqs = serializers.SerializerMethodField()
    
    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'slug', 'description', 'order', 'faqs']
    
    def get_faqs(self, obj):
        # Solo incluir FAQs publicadas para usuarios no administradores
        request = self.context.get('request')
        if request and request.user.is_staff:
            faqs = obj.faqs.all()
        else:
            faqs = obj.faqs.filter(is_published=True)
        
        return FAQSerializer(faqs, many=True, context=self.context).data
