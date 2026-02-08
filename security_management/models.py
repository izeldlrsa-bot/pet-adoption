from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    User = get_user_model()
    
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'
    ROLE_CHOICES = [
        (ROLE_USER, 'User'),
        (ROLE_ADMIN, 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_USER)

    def __str__(self) -> str:
        return f"Profile: {self.user.get_username()} ({self.role})"

# Signal to create profile automatically when a user is created
@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create profile with default 'user' role
        Profile.objects.create(user=instance, role='user')
        print(f"Signal: Created profile for {instance.username} with role='user'")

@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()