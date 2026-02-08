from django.db import models
from django.utils import timezone
from django.conf import settings  # Add this import

class Pet(models.Model):
    # Basic info
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=50)
    age = models.IntegerField()
    description = models.TextField()
    
    # SIMPLE: Boolean fields for dog/cat (remove species)
    is_dog = models.BooleanField(default=False, verbose_name="Is a Dog")
    is_cat = models.BooleanField(default=False, verbose_name="Is a Cat")
    
    # Other fields (keep as is)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown')
    ], default='unknown')
    
    size = models.CharField(max_length=10, choices=[
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('xlarge', 'Extra Large')
    ], default='medium')
    
    color = models.CharField(max_length=50, blank=True)
    special_needs = models.TextField(blank=True, help_text="Any special care requirements")
    vaccination_status = models.CharField(max_length=20, choices=[
        ('up_to_date', 'Up to Date'),
        ('partial', 'Partial'),
        ('none', 'Not Vaccinated')
    ], default='up_to_date')
    
    # Images
    main_image = models.ImageField(upload_to='pets/main/', null=True, blank=True)
    additional_images = models.ImageField(upload_to='pets/additional/', null=True, blank=True, 
                                         help_text="Additional photos (optional)")
    
    # Status fields - UPDATED WITH BETTER DEFAULTS
    is_available = models.BooleanField(default=True, verbose_name="Available for adoption")
    adopted = models.BooleanField(default=False, verbose_name="Already adopted")
    
    # Timestamps - FIXED: removed default parameter
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intake_date = models.DateField(null=True, blank=True, help_text="Date when pet arrived at shelter")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
    
    def __str__(self):
        """Simple string representation"""
        pet_type = "Dog" if self.is_dog else "Cat" if self.is_cat else "Pet"
        return f"{self.name} - {pet_type} ({self.age}y)"
    
    # adoption/models.py - Fix the save method
# In adoption/models.py - UPDATE the save() method in AdoptionApplication class

def save(self, *args, **kwargs):
    """Update dates when status changes AND update pet availability"""
    
    # Get the old status if this is an update (not a new creation)
    old_status = None
    if self.pk:
        try:
            old_instance = AdoptionApplication.objects.get(pk=self.pk)
            old_status = old_instance.status
        except AdoptionApplication.DoesNotExist:
            pass
    
    # Update reviewed_date when status changes from pending
    if old_status == 'pending' and self.status != 'pending':
        self.reviewed_date = timezone.now()
        print(f"[APPLICATION] Status changed from pending, setting reviewed_date")
    
    # Update decision_date when status becomes approved or rejected
    if self.status in ['approved', 'rejected'] and not self.decision_date:
        self.decision_date = timezone.now()
        print(f"[APPLICATION] Status set to {self.status}, setting decision_date")
    
    # NEW LOGIC: Update pet availability when application is approved
    if old_status != 'approved' and self.status == 'approved':
        # Mark the pet as not available
        self.pet.is_available = False
        self.pet.adopted = True  # Also mark as adopted
        self.pet.save()
        print(f"[APPLICATION] Application approved! Marking {self.pet.name} as not available")
    
    # NEW LOGIC: If application status changes FROM approved to something else
    elif old_status == 'approved' and self.status != 'approved':
        # Check if there are no other approved applications for this pet
        other_approved_apps = AdoptionApplication.objects.filter(
            pet=self.pet,
            status='approved'
        ).exclude(pk=self.pk)
        
        if not other_approved_apps.exists():
            # No other approved applications, so pet becomes available again
            self.pet.is_available = True
            self.pet.adopted = False
            self.pet.save()
            print(f"[APPLICATION] Application no longer approved. Marking {self.pet.name} as available")
    
    super().save(*args, **kwargs)
    
    def get_status_display(self):
        """Get human-readable status"""
        if self.adopted:
            return "Adopted"
        elif self.is_available:
            return "Available"
        else:
            return "Not Available"


class AdoptionApplication(models.Model):
    """Adoption application model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    # FIX: Use string reference to avoid circular imports
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='applications')
    
    # FIX: Use settings.AUTH_USER_MODEL instead of get_user_model()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_applications')
    
    # Applicant Information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Application Details
    reason_for_adoption = models.TextField(verbose_name="Why do you want to adopt this pet?")
    previous_pet_experience = models.TextField(verbose_name="Previous experience with pets")
    home_description = models.TextField(
        verbose_name="Home environment description",
        help_text="Describe your home, yard, other pets, etc.",
        blank=True
    )
    household_members = models.TextField(
        blank=True,
        verbose_name="Household members",
        help_text="Who lives in your home? (ages if children)"
    )
    
    # References
    vet_reference = models.TextField(
        blank=True,
        verbose_name="Veterinary reference",
        help_text="Name and contact of your veterinarian (if any)"
    )
    personal_reference = models.TextField(
        blank=True,
        verbose_name="Personal reference",
        help_text="Name and contact of a personal reference"
    )
    
    # Status & Dates
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    reviewed_date = models.DateTimeField(null=True, blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin fields
    notes = models.TextField(blank=True, verbose_name="Admin notes")
    admin_comments = models.TextField(blank=True, verbose_name="Internal comments")
    
    # Follow-up
    follow_up_date = models.DateField(null=True, blank=True, verbose_name="Follow-up date")
    follow_up_notes = models.TextField(blank=True, verbose_name="Follow-up notes")
    
    class Meta:
        ordering = ['-applied_date']
        unique_together = ['pet', 'user']
        verbose_name = "Adoption Application"
        verbose_name_plural = "Adoption Applications"
    
    def __str__(self):
        return f"{self.full_name} - {self.pet.name} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        """Update dates when status changes"""
        
        # Update reviewed_date when status changes from pending
        if self.pk:
            try:
                old_instance = AdoptionApplication.objects.get(pk=self.pk)
                if old_instance.status == 'pending' and self.status != 'pending':
                    self.reviewed_date = timezone.now()
                    print(f"[APPLICATION] Status changed from pending, setting reviewed_date")
            except AdoptionApplication.DoesNotExist:
                pass
        
        # Update decision_date when status becomes approved or rejected
        if self.status in ['approved', 'rejected'] and not self.decision_date:
            self.decision_date = timezone.now()
            print(f"[APPLICATION] Status set to {self.status}, setting decision_date")
        
        super().save(*args, **kwargs)