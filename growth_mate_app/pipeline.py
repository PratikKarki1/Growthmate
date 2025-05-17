from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from .models import UserProfile

def save_profile(backend, user, response, *args, **kwargs):
    """
    Custom pipeline to handle user profile creation after social auth.
    Redirects to role selection if the user is new.
    """
    # Check if this is a new user
    try:
        profile = UserProfile.objects.get(user=user)
        # Existing user - continue with normal login flow
        return
    except UserProfile.DoesNotExist:
        # Store user ID in session for role selection
        kwargs['request'].session['user_id'] = user.id
        # Store email from Google response
        kwargs['request'].session['social_email'] = response.get('email', '')
        # Store name from Google response
        name_data = response.get('name', '')
        first_name = response.get('given_name', name_data.split()[0] if name_data else '')
        last_name = response.get('family_name', ' '.join(name_data.split()[1:]) if name_data and len(name_data.split()) > 1 else '')
        
        kwargs['request'].session['social_first_name'] = first_name
        kwargs['request'].session['social_last_name'] = last_name
        
        # Redirect to role selection
        return redirect('select_role') 