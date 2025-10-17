from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
import os


class Command(BaseCommand):
    help = 'Initialize database and create superuser for production'

    def handle(self, *args, **options):
        self.stdout.write('Starting database initialization...')
        
        try:
            # Test database connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            self.stdout.write(self.style.SUCCESS('Database connection successful'))
            
            # Run migrations
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=0)
            self.stdout.write(self.style.SUCCESS('Migrations completed'))
            
            # Create superuser if it doesn't exist
            from django.contrib.auth.models import User
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@tradingjournal.com',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created: admin/admin123'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise
