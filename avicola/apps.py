from django.apps import AppConfig
from django.conf import settings
from django.contrib import admin

class AvicolaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'avicola'
    
    def ready(self):
        """
        Configure admin site when the application is ready.
        This runs after all apps are loaded.
        """
        try:
            from django.apps import apps
            from avicola.auth_admin import register_auth_models
            
            # Register auth models with our custom admin site
            register_auth_models(admin.site)
            
            # Import and register admin modules for each app
            try:
                # Wiki app
                from wiki import admin as wiki_admin
                admin.site.register(wiki_admin.Category, wiki_admin.CategoryAdmin)
                admin.site.register(wiki_admin.Article, wiki_admin.ArticleAdmin)
                admin.site.register(wiki_admin.Attachment, wiki_admin.AttachmentAdmin)
                print("Registered wiki admin")
            except Exception as e:
                print(f"Could not register wiki admin: {str(e)}")
                
            try:
                # FAQ app
                from faq import admin as faq_admin
                admin.site.register(faq_admin.FAQCategory, faq_admin.FAQCategoryAdmin)
                admin.site.register(faq_admin.FAQ, faq_admin.FAQAdmin)
                print("Registered faq admin")
            except Exception as e:
                print(f"Could not register faq admin: {str(e)}")
                
            try:
                # Bot app
                from bot import admin as bot_admin
                admin.site.register(bot_admin.BotIntent, bot_admin.BotIntentAdmin)
                admin.site.register(bot_admin.BotConversation, bot_admin.BotConversationAdmin)
                admin.site.register(bot_admin.BotMessage, bot_admin.BotMessageAdmin)
                print("Registered bot admin")
            except Exception as e:
                print(f"Could not register bot admin: {str(e)}")
                
            try:
                # Respaldos app
                from respaldos import admin as respaldos_admin
                admin.site.register(respaldos_admin.Backup, respaldos_admin.BackupAdmin)
                admin.site.register(respaldos_admin.BackupConfiguration, respaldos_admin.BackupConfigurationAdmin)
                admin.site.register(respaldos_admin.RestoreLog, respaldos_admin.RestoreLogAdmin)
                print("Registered respaldos admin")
            except Exception as e:
                print(f"Could not register respaldos admin: {str(e)}")
                
            # Register Django Summernote if installed
            try:
                from django_summernote.admin import SummernoteModelAdmin
                from django_summernote.models import Attachment as SummernoteAttachment
                admin.site.register(SummernoteAttachment)
                print("Registered django-summernote admin")
            except Exception as e:
                print(f"Could not register django-summernote admin: {str(e)}")
                    
        except Exception as e:
            print(f"Error in AvicolaConfig.ready(): {str(e)}")
            import traceback
            traceback.print_exc()
