"""
Supabase Authentication Views
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .supabase_auth import supabase_auth
import json

def supabase_register_view(request):
    """Supabase registration view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            email = data.get('email')
            password = data.get('password')
            first_name = data.get('first_name', '')
            last_name = data.get('last_name', '')
            
            if not email or not password:
                return JsonResponse({
                    'success': False, 
                    'error': 'Email and password are required'
                })
            
            # Sign up with Supabase
            result = supabase_auth.sign_up(
                email=email,
                password=password,
                user_metadata={
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            
            if result['success']:
                # Debug: Print the result
                print(f"Supabase signup result: {result}")
                
                # Create Django user
                user_data = result['data'].get('user', result['data'])
                django_user = supabase_auth.create_django_user(user_data)
                
                if django_user:
                    # Check if email confirmation is required
                    user_metadata = user_data.get('user_metadata', {})
                    email_verified = user_metadata.get('email_verified', False)
                    
                    if email_verified:
                        # Log in the user immediately
                        login(request, django_user)
                        
                        if request.content_type == 'application/json':
                            return JsonResponse({
                                'success': True,
                                'message': 'Registration successful!',
                                'user': {
                                    'id': django_user.id,
                                    'username': django_user.username,
                                    'email': django_user.email
                                }
                            })
                        else:
                            messages.success(request, 'Registration successful! Welcome to your Trading Journal.')
                            return redirect('dashboard')
                    else:
                        # Email confirmation required
                        if request.content_type == 'application/json':
                            return JsonResponse({
                                'success': True,
                                'message': 'Registration successful! Please check your email and confirm your account before signing in.',
                                'email_confirmation_required': True
                            })
                        else:
                            messages.success(request, 'Registration successful! Please check your email and confirm your account before signing in.')
                            return redirect('login')
                else:
                    error_msg = 'Failed to create Django user account'
            else:
                error_msg = result.get('error', {}).get('message', 'Registration failed')
                # Log the full error for debugging
                print(f"Supabase registration error: {result}")
                
        except Exception as e:
            error_msg = f'Registration error: {str(e)}'
            # Log the full exception for debugging
            print(f"Registration exception: {str(e)}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
        
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': error_msg})
        else:
            messages.error(request, error_msg)
    
    return render(request, 'registration/supabase_register.html')

def supabase_login_view(request):
    """Supabase login view"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({
                    'success': False, 
                    'error': 'Email and password are required'
                })
            
            # Sign in with Supabase
            result = supabase_auth.sign_in(email=email, password=password)
            
            if result['success']:
                # Get user data
                user_data = result['data']['user']
                access_token = result['data']['access_token']
                
                # Create or get Django user
                django_user = supabase_auth.create_django_user(user_data)
                
                if django_user:
                    # Store Supabase token in session
                    request.session['supabase_access_token'] = access_token
                    request.session['supabase_user_id'] = user_data['id']
                    
                    # Log in the user
                    login(request, django_user)
                    
                    if request.content_type == 'application/json':
                        return JsonResponse({
                            'success': True,
                            'message': 'Login successful!',
                            'user': {
                                'id': django_user.id,
                                'username': django_user.username,
                                'email': django_user.email
                            }
                        })
                    else:
                        messages.success(request, 'Login successful!')
                        return redirect('dashboard')
                else:
                    error_msg = 'Failed to authenticate user'
            else:
                error_data = result.get('error', {})
                if isinstance(error_data, dict):
                    error_msg = error_data.get('message', 'Invalid credentials')
                else:
                    error_msg = str(error_data) if error_data else 'Invalid credentials'
                
        except Exception as e:
            error_msg = f'Login error: {str(e)}'
        
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': error_msg})
        else:
            messages.error(request, error_msg)
    
    return render(request, 'registration/supabase_login.html')

@login_required
def supabase_logout_view(request):
    """Supabase logout view"""
    try:
        # Get Supabase token from session
        access_token = request.session.get('supabase_access_token')
        
        if access_token:
            # Sign out from Supabase
            supabase_auth.sign_out(access_token)
            
            # Clear session data
            request.session.pop('supabase_access_token', None)
            request.session.pop('supabase_user_id', None)
        
        # Logout from Django
        logout(request)
        messages.success(request, 'Logged out successfully!')
        
    except Exception as e:
        messages.error(request, f'Logout error: {str(e)}')
    
    return redirect('login')

@login_required
def supabase_profile_view(request):
    """Get current user profile from Supabase"""
    try:
        access_token = request.session.get('supabase_access_token')
        
        if access_token:
            result = supabase_auth.get_user(access_token)
            
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'user': result['data']
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to get user profile'
                })
        else:
            return JsonResponse({
                'success': False,
                'error': 'No active session'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def supabase_webhook_view(request):
    """Handle Supabase webhooks for user events"""
    try:
        # Verify webhook signature (implement based on your needs)
        data = json.loads(request.body)
        event_type = data.get('type')
        
        if event_type == 'user.created':
            # Handle new user creation
            user_data = data.get('record', {})
            django_user = supabase_auth.create_django_user(user_data)
            
        elif event_type == 'user.updated':
            # Handle user updates
            user_data = data.get('record', {})
            # Update Django user if needed
            
        elif event_type == 'user.deleted':
            # Handle user deletion
            user_id = data.get('record', {}).get('id')
            # Handle user deletion if needed
            
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
