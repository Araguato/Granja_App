from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wiki.models import Category, Article
from faq.models import FAQCategory, FAQ
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Load sample data for WIKI and FAQ sections'

    def handle(self, *args, **options):
        # Create a superuser if it doesn't exist
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
            admin = User.objects.get(username='admin')

        # Create WIKI categories and articles
        if Category.objects.count() == 0:
            # Create categories
            cat1 = Category.objects.create(
                name='Manejo de Aves',
                description='Guías para el manejo adecuado de aves',
                order=1
            )
            cat2 = Category.objects.create(
                name='Alimentación',
                description='Información sobre alimentación de aves',
                order=2
            )
            
            # Create articles
            Article.objects.create(
                title='Manejo de pollitos en la primera semana',
                content='Contenido detallado sobre el manejo de pollitos...',
                category=cat1,
                is_published=True
            )
            Article.objects.create(
                title='Programa de alimentación para pollos de engorde',
                content='Contenido detallado sobre el programa de alimentación...',
                category=cat2,
                is_published=True
            )
            self.stdout.write(self.style.SUCCESS('Created WIKI sample data'))

        # Create FAQ categories and questions
        if FAQCategory.objects.count() == 0:
            # Create categories
            faq_cat1 = FAQCategory.objects.create(
                name='Manejo General',
                description='Preguntas generales sobre el manejo de la granja',
                order=1
            )
            faq_cat2 = FAQCategory.objects.create(
                name='Salud y Bienestar',
                description='Preguntas sobre la salud de las aves',
                order=2
            )
            
            # Create FAQs
            FAQ.objects.create(
                question='¿Con qué frecuencia debo limpiar los galpones?',
                answer='Se recomienda limpiar los galpones al menos una vez por semana...',
                category=faq_cat1,
                is_published=True,
                order=1
            )
            FAQ.objects.create(
                question='¿Cuáles son los signos de enfermedad en las aves?',
                answer='Algunos signos comunes incluyen pérdida de apetito...',
                category=faq_cat2,
                is_published=True,
                order=1
            )
            self.stdout.write(self.style.SUCCESS('Created FAQ sample data'))

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))
