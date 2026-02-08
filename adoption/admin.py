from django.contrib import admin
from django.utils import timezone
from .models import Pet, AdoptionApplication

# Custom admin action for approving applications
def approve_applications(modeladmin, request, queryset):
    queryset.update(
        status='approved',
        decision_date=timezone.now(),
        reviewed_date=timezone.now()  # Ensure reviewed_date is set
    )
    modeladmin.message_user(request, f"{queryset.count()} application(s) approved.")

approve_applications.short_description = "Mark selected as Approved"

# Custom admin action for rejecting applications
def reject_applications(modeladmin, request, queryset):
    queryset.update(
        status='rejected',
        decision_date=timezone.now(),
        reviewed_date=timezone.now()
    )
    modeladmin.message_user(request, f"{queryset.count()} application(s) rejected.")

reject_applications.short_description = "Mark selected as Rejected"

# Inline for viewing applications related to a pet
class ApplicationInline(admin.TabularInline):
    model = AdoptionApplication
    extra = 0
    fields = ['user', 'full_name', 'status', 'applied_date']
    readonly_fields = ['user', 'full_name', 'applied_date']
    can_delete = False
    
    # Limit inline display to prevent overcrowding
    max_num = 5
    show_change_link = True

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_type', 'age', 'gender', 'is_available', 'adopted', 'created_at']
    list_filter = ['is_dog', 'is_cat', 'gender', 'size', 'is_available', 'adopted', 'created_at']
    search_fields = ['name', 'breed', 'description']
    list_editable = ['is_available', 'adopted']
    readonly_fields = ['created_at', 'updated_at']
    
    # Add applications inline to pet admin
    inlines = [ApplicationInline]
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'breed', 'age', 'description']
        }),
        ('Type & Characteristics', {
            'fields': [('is_dog', 'is_cat'), 'gender', 'size', 'color']
        }),
        ('Health & Care', {
            'fields': ['special_needs', 'vaccination_status']
        }),
        ('Images', {
            'fields': ['main_image', 'additional_images']
        }),
        ('Status', {
            'fields': [('is_available', 'adopted'), 'intake_date']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
    
    def display_type(self, obj):
        """Display pet type in admin list"""
        if obj.is_dog:
            return "Dog"
        elif obj.is_cat:
            return "Cat"
        return "Unknown"
    display_type.short_description = "Type"

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    # ... keep all your existing configuration ...
    
    def save_model(self, request, obj, form, change):
        """Custom save to update dates when status changes"""
        print("\n" + "="*60)
        print("[ADMIN SAVE] Starting save for AdoptionApplication")
        print(f"[ADMIN SAVE] Application ID: {obj.id}")
        print(f"[ADMIN SAVE] Is this a change? {change}")
        print(f"[ADMIN SAVE] Changed fields: {form.changed_data}")
        print(f"[ADMIN SAVE] Old status (from form): {form.initial.get('status', 'N/A')}")
        print(f"[ADMIN SAVE] New status (from obj): {obj.status}")
        
        # Check if status is changing
        if 'status' in form.changed_data:
            print(f"[ADMIN SAVE] Status is changing!")
            if obj.status in ['approved', 'rejected'] and not obj.decision_date:
                obj.decision_date = timezone.now()
                print(f"[ADMIN SAVE] Setting decision_date: {obj.decision_date}")
            if obj.status != 'pending' and not obj.reviewed_date:
                obj.reviewed_date = timezone.now()
                print(f"[ADMIN SAVE] Setting reviewed_date: {obj.reviewed_date}")
        
        # Call parent save
        super().save_model(request, obj, form, change)
        
        print(f"[ADMIN SAVE] Save completed successfully")
        print("="*60 + "\n")
    
    
    def save_model(self, request, obj, form, change):
        """Custom save to update dates when status changes"""
        if 'status' in form.changed_data:
            if obj.status in ['approved', 'rejected'] and not obj.decision_date:
                obj.decision_date = timezone.now()
            if obj.status != 'pending' and not obj.reviewed_date:
                obj.reviewed_date = timezone.now()
        super().save_model(request, obj, form, change)