"""
Supabase Authentication Helper for Django
"""
import requests
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

class SupabaseAuth:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.anon_key = settings.SUPABASE_ANON_KEY
        self.service_key = settings.SUPABASE_SERVICE_ROLE_KEY
        
    def sign_up(self, email, password, user_metadata=None):
        """Sign up a new user with Supabase"""
        try:
            url = f"{self.url}/auth/v1/signup"
            headers = {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
            data = {
                "email": email,
                "password": password,
                "data": user_metadata or {}
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"User signed up successfully: {email}")
                logger.info(f"Supabase response: {result}")
                return {"success": True, "data": result}
            else:
                error_data = response.json() if response.content else {"error": "Unknown error"}
                logger.error(f"Sign up failed: {error_data}")
                return {"success": False, "error": error_data}
                
        except Exception as e:
            logger.error(f"Sign up exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def sign_in(self, email, password):
        """Sign in user with Supabase"""
        try:
            url = f"{self.url}/auth/v1/token?grant_type=password"
            headers = {
                "apikey": self.anon_key,
                "Content-Type": "application/json"
            }
            data = {
                "email": email,
                "password": password
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"User signed in successfully: {email}")
                return {"success": True, "data": result}
            else:
                error_data = response.json() if response.content else {"error": "Invalid credentials"}
                logger.error(f"Sign in failed: {error_data}")
                
                # Provide more specific error messages
                if error_data.get('error_code') == 'invalid_credentials':
                    error_msg = "Invalid email or password. If you just registered, please check your email and confirm your account first."
                elif error_data.get('error_code') == 'email_not_confirmed':
                    error_msg = "Please check your email and confirm your account before signing in."
                else:
                    error_msg = error_data.get('msg', 'Invalid credentials')
                
                return {"success": False, "error": {"message": error_msg, "code": error_data.get('error_code')}}
                
        except Exception as e:
            logger.error(f"Sign in exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_user(self, access_token):
        """Get user info from Supabase"""
        try:
            url = f"{self.url}/auth/v1/user"
            headers = {
                "apikey": self.anon_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                return {"success": True, "data": result}
            else:
                return {"success": False, "error": "Invalid token"}
                
        except Exception as e:
            logger.error(f"Get user exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def sign_out(self, access_token):
        """Sign out user from Supabase"""
        try:
            url = f"{self.url}/auth/v1/logout"
            headers = {
                "apikey": self.anon_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers)
            return {"success": True}
            
        except Exception as e:
            logger.error(f"Sign out exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def create_django_user(self, supabase_user_data):
        """Create or update Django user from Supabase data"""
        try:
            logger.info(f"Creating Django user from data: {supabase_user_data}")
            
            email = supabase_user_data.get('email')
            user_id = supabase_user_data.get('id')
            
            if not email:
                logger.error("No email found in Supabase user data")
                return None
                
            # Get user metadata
            user_metadata = supabase_user_data.get('user_metadata', {})
            first_name = user_metadata.get('first_name', '')
            last_name = user_metadata.get('last_name', '')
            
            # Create username from email
            username = email.split('@')[0]
            
            # Create or get Django user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            
            if created:
                logger.info(f"Created Django user: {user.username}")
            else:
                logger.info(f"Found existing Django user: {user.username}")
                
            return user
            
        except Exception as e:
            logger.error(f"Create Django user exception: {str(e)}")
            return None

# Global instance
supabase_auth = SupabaseAuth()
