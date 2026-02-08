# pet_adoption/forms.py (FIXED)
from django import forms
from adoption.models import AdoptionApplication

class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = [
            'full_name', 'email', 'phone', 'address',
            'reason_for_adoption', 'previous_pet_experience', 'home_description'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'reason_for_adoption': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'previous_pet_experience': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'home_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        labels = {
            'full_name': 'Your Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'address': 'Home Address',
            'reason_for_adoption': 'Why do you want to adopt this pet?',
            'previous_pet_experience': 'Do you have previous experience with pets?',
            'home_description': 'Describe your home (size, yard, other pets, etc.)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to text inputs
        for field_name in ['full_name', 'email', 'phone']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove all non-digit characters
            digits = ''.join(filter(str.isdigit, phone))
            if len(digits) < 10:
                raise forms.ValidationError("Please enter a valid phone number with area code.")
        return phone