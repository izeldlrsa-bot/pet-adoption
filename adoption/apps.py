# adoption/apps.py
from django.apps import AppConfig

class AdoptionConfig(AppConfig):  # Should be AdoptionConfig, NOT UserManagementConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoption'
    verbose_name = 'Adoption Management'