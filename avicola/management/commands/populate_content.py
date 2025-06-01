from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faq.models import FAQCategory, FAQ
from wiki.models import Category, Article
from bot.models import BotIntent, BotTrainingPhrase, BotResponse

class Command(BaseCommand):
    help = 'Populates the database with initial FAQ, Wiki, and Bot content'

    def handle(self, *args, **options):
        # Get or create admin user
        User = get_user_model()
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        
        self.create_faq_content(admin_user)
        self.create_wiki_content(admin_user)
        self.create_bot_content(admin_user)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated content for FAQ, Wiki, and Bot'))
    
    def create_faq_content(self, user):
        # Create FAQ Categories
        system_cat, _ = FAQCategory.objects.get_or_create(
            name='System Help',
            defaults={'description': 'Frequently asked questions about using the system', 'order': 1}
        )
        
        farm_cat, _ = FAQCategory.objects.get_or_create(
            name='Farm Management',
            defaults={'description': 'Questions about managing your poultry farm', 'order': 2}
        )
        
        # System FAQs
        faqs = [
            {
                'question': 'How do I reset my password?',
                'answer': 'Click on "Forgot password" on the login page and follow the instructions sent to your email.',
                'category': system_cat
            },
            {
                'question': 'How do I generate reports?',
                'answer': 'Navigate to the Reports section and select the type of report you need. Choose your date range and click Generate.',
                'category': system_cat
            },
            {
                'question': 'What is the ideal temperature for broilers?',
                'answer': 'The ideal temperature varies by age: 32-35°C (90-95°F) for day-old chicks, decreasing by about 2.5°C per week until reaching 21-24°C (70-75°F).',
                'category': farm_cat
            },
            {
                'question': 'How often should I clean the chicken coop?',
                'answer': 'Daily spot cleaning is recommended, with a thorough cleaning and disinfection between flocks.',
                'category': farm_cat
            },
        ]
        
        for faq in faqs:
            FAQ.objects.get_or_create(
                question=faq['question'],
                defaults={
                    'answer': faq['answer'],
                    'category': faq['category'],
                    'is_published': True,
                    'order': 1
                }
            )
    
    def create_wiki_content(self, user):
        # Create Wiki Categories
        system_cat, _ = Category.objects.get_or_create(
            name='System Documentation',
            defaults={'description': 'Documentation about using the system', 'order': 1}
        )
        
        farm_cat, _ = Category.objects.get_or_create(
            name='Poultry Farming Guide',
            defaults={'description': 'Comprehensive guides for poultry farming', 'order': 2}
        )
        
        # System Documentation Articles
        system_articles = [
            {
                'title': 'Getting Started',
                'content': '## Welcome to Farm Management System\n\nThis guide will help you get started with the system.\n\n### Key Features:\n- Inventory Management\n- Production Tracking\n- Sales Management\n- Reporting\n\n### First Steps:\n1. Complete your farm profile\n2. Set up your inventory\n3. Add your first batch of birds',
                'category': system_cat
            },
            {
                'title': 'User Roles and Permissions',
                'content': '## Understanding User Roles\n\n### Administrator\n- Full system access\n- Can manage all farm data\n- User management\n\n### Manager\n- Can view and manage production\n- Access to reports\n- Limited user management\n\n### Worker\n- Basic data entry\n- View assigned tasks\n- Limited access to reports',
                'category': system_cat
            }
        ]
        
        # Farm Guide Articles
        farm_articles = [
            {
                'title': 'Broiler Management Guide',
                'content': '## Broiler Management Best Practices\n\n### Housing:\n- Provide 1 sq.ft per bird\n- Ensure proper ventilation\n- Maintain clean bedding\n\n### Feeding:\n- Provide starter feed (0-10 days)\n- Grower feed (11-24 days)\n- Finisher feed (25 days to market)',
                'category': farm_cat
            },
            {
                'title': 'Biosecurity Measures',
                'content': '## Farm Biosecurity\n\n### Key Measures:\n- Restrict farm access\n- Provide foot baths\n- Regular disinfection\n- Rodent and pest control\n\n### Visitor Policy:\n- Minimum 48-hour bird-free period\n- Use of protective clothing\n- Hand sanitization required',
                'category': farm_cat
            }
        ]
        
        for article in system_articles + farm_articles:
            Article.objects.get_or_create(
                title=article['title'],
                defaults={
                    'content': article['content'],
                    'category': article['category'],
                    'author': user,
                    'is_published': True
                }
            )
    
    def create_bot_content(self, user):
        # Create Bot Intents
        greeting_intent, _ = BotIntent.objects.get_or_create(
            name='greeting',
            defaults={'description': 'Greet the user'}
        )
        
        farm_help_intent, _ = BotIntent.objects.get_or_create(
            name='farm_help',
            defaults={'description': 'Provide help with farm management'}
        )
        
        # Greeting Intent
        greeting_phrases = [
            'Hi',
            'Hello',
            'Good morning',
            'Good afternoon',
            'Hey there'
        ]
        
        for phrase in greeting_phrases:
            BotTrainingPhrase.objects.get_or_create(
                intent=greeting_intent,
                text=phrase
            )
        
        BotResponse.objects.get_or_create(
            intent=greeting_intent,
            text='Hello! How can I assist you with your farm management today?'
        )
        
        # Farm Help Intent
        farm_phrases = [
            'How do I manage my farm?',
            'Farm management tips',
            'Help with poultry farming',
            'Best practices for chicken farming'
        ]
        
        for phrase in farm_phrases:
            BotTrainingPhrase.objects.get_or_create(
                intent=farm_help_intent,
                text=phrase
            )
        
        BotResponse.objects.get_or_create(
            intent=farm_help_intent,
            text='''Here are some key farm management tips:
1. Maintain proper ventilation in chicken houses
2. Ensure clean water is always available
3. Follow a strict vaccination schedule
4. Monitor feed quality and quantity
5. Keep detailed production records

Would you like more specific information about any of these areas?'''
        )
