from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Customize the User admin if needed
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

# Unregister default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# You can also customize Group admin if needed
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)