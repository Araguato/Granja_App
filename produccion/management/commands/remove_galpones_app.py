from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Safely remove the galpones app and its database tables'

    def handle(self, *args, **options):
        # Check if the table exists
        with connection.cursor() as cursor:
            # Drop the galpones_galpon table if it exists
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'galpones_galpon';
            """)
            if cursor.fetchone():
                self.stdout.write(self.style.WARNING('Dropping table galpones_galpon...'))
                cursor.execute('DROP TABLE IF EXISTS galpones_galpon CASCADE')
                self.stdout.write(self.style.SUCCESS('Successfully dropped table galpones_galpon'))
            else:
                self.stdout.write(self.style.SUCCESS('Table galpones_galpon does not exist'))

        self.stdout.write(self.style.SUCCESS('Galpones app cleanup completed'))
