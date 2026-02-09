# adoption/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Pet, AdoptionApplication

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            'name', 
            'is_dog',
            'is_cat',
            'breed', 
            'age', 
            'gender', 
            'size',
            'color', 
            'description', 
            'special_needs', 
            'vaccination_status',
            'main_image', 
            'additional_images', 
            'is_available', 
            'adopted',
            'intake_date'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'special_needs': forms.Textarea(attrs={'rows': 3}),
            'intake_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'size': forms.Select(attrs={'class': 'form-control'}),
            'vaccination_status': forms.Select(attrs={'class': 'form-control'}),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*',
                'style': 'cursor: pointer;'
            }),
            'additional_images': forms.FileInput(attrs={
                'class': 'form-control form-control-lg',
                'accept': 'image/*',
                'style': 'cursor: pointer;'
            }),
        }
        labels = {
            'is_dog': 'Is a Dog',
            'is_cat': 'Is a Cat',
            'main_image': 'Main Pet Photo',
            'additional_images': 'Additional Photos',
        }
        help_texts = {
            'is_dog': 'Check if this pet is a dog',
            'is_cat': 'Check if this pet is a cat',
            'main_image': 'Upload a clear, front-facing photo of the pet (JPG, PNG)',
            'additional_images': 'Upload additional photos showing different angles (JPG, PNG)',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        is_dog = cleaned_data.get('is_dog')
        is_cat = cleaned_data.get('is_cat')
        
        if not is_dog and not is_cat:
            raise ValidationError("Please select either 'Is a Dog' or 'Is a Cat'.")
        
        if is_dog and is_cat:
            raise ValidationError("A pet cannot be both a dog and a cat.")
        
        return cleaned_data
    
    def clean_main_image(self):
        main_image = self.cleaned_data.get('main_image')
        if main_image:
            # Check file size (max 5MB)
            if main_image.size > 5 * 1024 * 1024:
                raise ValidationError("Main image file size must be less than 5MB.")
            # Validate it's an image
            try:
                from PIL import Image
                img = Image.open(main_image)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return main_image
    
    def clean_additional_images(self):
        additional_images = self.cleaned_data.get('additional_images')
        if additional_images:
            # Check file size (max 5MB)
            if additional_images.size > 5 * 1024 * 1024:
                raise ValidationError("Additional image file size must be less than 5MB.")
            # Validate it's an image
            try:
                from PIL import Image
                img = Image.open(additional_images)
                img.verify()
            except Exception:
                raise ValidationError("Please upload a valid image file.")
        return additional_images
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None:
            if age < 0:
                raise ValidationError("Age cannot be negative.")
            if age > 30:
                raise ValidationError("Please enter a valid age (0-30).")
        return age


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = [
            'full_name', 'email', 'phone', 'address',
            'reason_for_adoption', 'previous_pet_experience', 'home_description',
            'household_members', 'vet_reference', 'personal_reference'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'reason_for_adoption': forms.Textarea(attrs={'rows': 4}),
            'previous_pet_experience': forms.Textarea(attrs={'rows': 4}),
            'home_description': forms.Textarea(attrs={'rows': 4}),
            'household_members': forms.Textarea(attrs={'rows': 3}),
            'vet_reference': forms.Textarea(attrs={'rows': 3}),
            'personal_reference': forms.Textarea(attrs={'rows': 3}),
        }


class ApplicationReviewForm(forms.ModelForm):
    """Form for staff to review applications - FIXED VERSION"""
    
    # Add these fields if they don't exist in your model
    SEND_EMAIL_CHOICES = [
        ('no', "Don't send email"),
        ('status_update', "Send status update email"),
        ('custom', "Send custom email"),
    ]
    
    send_email = forms.ChoiceField(
        choices=SEND_EMAIL_CHOICES,
        initial='no',
        required=False,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    custom_email_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Enter custom email message...',
            'class': 'form-control'
        }),
        help_text="Only used if 'Send custom email' is selected"
    )
    
    class Meta:
        model = AdoptionApplication
        fields = [
            'status',
            'notes',
            'admin_comments',
            'follow_up_date',
            'follow_up_notes'
        ]
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select form-select-lg',
                'style': 'font-weight: 600;'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Notes visible to the applicant...'
            }),
            'admin_comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Internal comments for staff only...'
            }),
            'follow_up_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'min': timezone.now().date().isoformat()
            }),
            'follow_up_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Follow-up notes...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make follow_up_date optional
        self.fields['follow_up_date'].required = False
        
        # Add Bootstrap classes to form fields
        for field_name, field in self.fields.items():
            if field_name != 'send_email':  # Don't add to radio select
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs['class'] = field.widget.attrs.get('class', '') + ' form-control'
        
        # Style status field differently based on current value
        if self.instance and self.instance.status:
            status_classes = {
                'pending': 'form-select-warning',
                'under_review': 'form-select-info',
                'approved': 'form-select-success',
                'rejected': 'form-select-danger',
                'cancelled': 'form-select-secondary',
            }
            css_class = status_classes.get(self.instance.status, '')
            self.fields['status'].widget.attrs['class'] += f' {css_class}'
    
    def clean(self):
        cleaned_data = super().clean()
        send_email = cleaned_data.get('send_email')
        custom_email_message = cleaned_data.get('custom_email_message')
        
        if send_email == 'custom' and not custom_email_message:
            self.add_error('custom_email_message', 'Please enter a custom email message.')
        
        return cleaned_data


# Keep your existing AdminAdoptionApplicationForm but rename to avoid conflict
class AdminApplicationForm(forms.ModelForm):
    """Form for Django admin panel"""
    class Meta:
        model = AdoptionApplication
        fields = ['status', 'notes', 'admin_comments', 'follow_up_date', 'follow_up_notes']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }