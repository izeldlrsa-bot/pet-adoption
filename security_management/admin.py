from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'user_email')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'