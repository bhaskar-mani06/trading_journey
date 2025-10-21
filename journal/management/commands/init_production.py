from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Initialize database for production deployment'

    def handle(self, *args, **options):
        self.stdout.write('Starting database initialization...')
        
        try:
            # Run migrations
            self.stdout.write('Running migrations...')
            call_command('migrate', verbosity=2)
            
            # Create superuser if it doesn't exist
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            if not User.objects.filter(username='admin').exists():
                self.stdout.write('Creating superuser...')
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'
                )
                self.stdout.write('Superuser created: admin/admin123')
            else:
                self.stdout.write('Superuser already exists')
                
            self.stdout.write(
                self.style.SUCCESS('Database initialization completed successfully!')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Database initialization failed: {str(e)}')
            )
            raise