from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    Decorator that checks if the user has admin role in their profile.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check if user has a profile and is admin
            if hasattr(request.user, 'profile'):
                if request.user.profile.role == 'admin':
                    return view_func(request, *args, **kwargs)
        
        # If not admin, show error message and redirect or show 403
        messages.error(request, "Access denied. Admin privileges required.")
        return HttpResponseForbidden("""
            <h1>403 Forbidden</h1>
            <p>You don't have permission to access this page.</p>
            <p><a href="/">Return to homepage</a></p>
        """)
    return _wrapped_view


def role_required(allowed_roles):
    """
    Decorator that checks if user has one of the allowed roles.
    Usage: @role_required(['admin', 'staff'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if hasattr(request.user, 'profile'):
                    if request.user.profile.role in allowed_roles:
                        return view_func(request, *args, **kwargs)
            
            messages.error(request, f"Access denied. Required roles: {', '.join(allowed_roles)}")
            return HttpResponseForbidden("""
                <h1>403 Forbidden</h1>
                <p>You don't have permission to access this page.</p>
                <p><a href="/">Return to homepage</a></p>
            """)
        return _wrapped_view
    return decorator


def user_required(view_func):
    """
    Decorator that checks if user is authenticated (any role).
    Basically the same as @login_required but uses your role system.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        
        # Redirect to login if not authenticated
        messages.warning(request, "Please login to access this page.")
        return redirect('login')  # Change 'login' to your actual login URL name
    return _wrapped_view