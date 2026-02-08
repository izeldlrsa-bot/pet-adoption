from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm
from .models import Profile
from django.contrib import messages

def custom_login(request):
    """Custom login that redirects all users to homepage first"""
    # If already logged in, redirect to homepage
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Get next URL from query parameter if exists
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # All users go to homepage first
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'security_management/pages/login.html', {
        'form': form,
        'title': 'Login',
        'next': request.GET.get('next', '')  # Pass next parameter to template
    })

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()  # This triggers the signal to create Profile automatically
            
            print(f"User created: {user.username}")  
            
            # Auto-login after registration
            auth_login(request, user)
            messages.success(request, f'Account created successfully! Welcome {user.username}!')
            
            # Redirect based on user role
            if user.is_staff or user.is_superuser:
                return redirect('adoption:pet_list')
            else:
                return redirect('pet_adoption:pet_list')
        else:
            print("Form errors:", form.errors) 
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    return render(
        request,
        'security_management/pages/register.html',
        {
            'form': form, 
            'title': 'Register',
            'next': request.GET.get('next', '')
        }
    )

@login_required
def profile(request):
    # Try to get or create profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile updates here if needed
        pass
    
    return render(request, 'security_management/pages/profile.html', {
        'title': 'Profile',
        'profile': profile,
        'user': request.user
    })

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """Logs the user out - accepts both GET and POST"""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')