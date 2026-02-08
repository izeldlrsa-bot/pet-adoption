# crudproject/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from security_management.decorators import admin_required, role_required

def landing_page(request):
    """
    Show landing page to non-logged in users.
    If user is logged in, redirect to appropriate pet list.
    """
    if request.user.is_authenticated:
        # User is logged in, redirect to appropriate pet list
        if request.user.is_staff:
            # Admin users go to admin pet management
            return redirect('adoption:pet_list')
        else:
            # Regular users go to public pet adoption page
            return redirect('pet_adoption:pet_list')
    else:
        # User is not logged in, show landing page
        return render(request, 'landing.html')