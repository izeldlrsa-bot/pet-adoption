def user_roles(request):
    """
    Add user role information to all templates.
    """
    context = {}
    if request.user.is_authenticated:
        if hasattr(request.user, 'profile'):
            context['user_role'] = request.user.profile.role
            context['is_admin'] = request.user.profile.role == 'admin'
        else:
            context['user_role'] = None
            context['is_admin'] = False
    else:
        context['user_role'] = None
        context['is_admin'] = False
    
    return context