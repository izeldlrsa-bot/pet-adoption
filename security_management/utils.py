def is_admin(user):
    """Check if user is admin"""
    if user.is_authenticated:
        if hasattr(user, 'profile'):
            return user.profile.role == 'admin'
    return False

def get_user_role(user):
    """Get user's role"""
    if user.is_authenticated and hasattr(user, 'profile'):
        return user.profile.role
    return None