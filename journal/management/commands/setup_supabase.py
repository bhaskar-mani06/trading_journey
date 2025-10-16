"""
Django management command to set up Supabase storage buckets and configurations
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from journal.supabase_client import get_supabase_client
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Set up Supabase storage buckets and configurations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up Supabase storage...'))
        
        client = get_supabase_client()
        if not client:
            self.stdout.write(
                self.style.ERROR('Supabase client not configured. Please check your environment variables.')
            )
            return
        
        try:
            # Create storage bucket for trade screenshots
            bucket_name = "trade-screenshots"
            
            # Check if bucket exists
            try:
                buckets = client.storage.list_buckets()
                bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
                
                if not bucket_exists:
                    # Create bucket
                    response = client.storage.create_bucket(
                        bucket_name,
                        options={"public": True}  # Make bucket public for easy access
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f'Created storage bucket: {bucket_name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Storage bucket already exists: {bucket_name}')
                    )
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating storage bucket: {e}')
                )
                return
            
            # Set up RLS policies (if needed)
            self.stdout.write(
                self.style.SUCCESS('Supabase storage setup completed successfully!')
            )
            
            # Display configuration info
            self.stdout.write('\n' + '='*50)
            self.stdout.write(self.style.SUCCESS('SUPABASE CONFIGURATION'))
            self.stdout.write('='*50)
            self.stdout.write(f'URL: {settings.SUPABASE_URL}')
            self.stdout.write(f'Storage Bucket: {bucket_name}')
            self.stdout.write('='*50)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up Supabase: {e}')
            )
