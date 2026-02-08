# pet_adoption/models.py
from django.db import models
from django.contrib.auth.models import User
# REMOVE these imports:
# from adoption.models import Pet, AdoptionApplication

class UserFavorite(models.Model):
    """Allow users to favorite pets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    
    # CHANGE: Use string reference
    pet = models.ForeignKey('adoption.Pet', on_delete=models.CASCADE, related_name='favorited_by')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'pet']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.pet.name}"


class AdoptionInquiry(models.Model):
    """For users who want more information before applying"""
    
    # CHANGE: Use string references
    pet = models.ForeignKey('adoption.Pet', on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pet_inquiries')
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    contacted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Adoption Inquiries"
    
    def __str__(self):
        return f"Inquiry about {self.pet.name} from {self.name}"