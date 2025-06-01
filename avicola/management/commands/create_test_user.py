from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a test user and assigns them to the Operarios group'

    def handle(self, *args, **options):
        with transaction.atomic():
            # Create test user if not exists
            username = 'operario_test'
            email = 'operario@example.com'
            password = 'testpass123'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_active': True
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Created test user: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Test user {username} already exists'))
            
            # Add user to Operarios group
            try:
                group = Group.objects.get(name='Operarios')
                user.groups.add(group)
                self.stdout.write(self.style.SUCCESS(f'Added {username} to Operarios group'))
                self.stdout.write(self.style.SUCCESS('Test user credentials:'))
                self.stdout.write(self.style.SUCCESS(f'Username: {username}'))
                self.stdout.write(self.style.SUCCESS(f'Password: {password}'))
            except Group.DoesNotExist:
                self.stdout.write(self.style.ERROR('Operarios group does not exist. Run setup_groups first.'))
