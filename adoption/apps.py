# adoption/apps.py
from django.apps import AppConfig

class AdoptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoption'
    verbose_name = 'Adoption Management'
    
    def ready(self):
        """Create superuser on app startup"""
        import os
        from django.contrib.auth.models import User
        
        try:
            username = os.environ.get('ADMIN_USERNAME', 'Admin')
            email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
            password = os.environ.get('ADMIN_PASSWORD', 'admin123')
            
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                print(f"✅ Superuser '{username}' created successfully")
            else:
                print(f"ℹ️ Superuser '{username}' already exists")
        except Exception as e:
            print(f"❌ Error creating admin: {str(e)}")