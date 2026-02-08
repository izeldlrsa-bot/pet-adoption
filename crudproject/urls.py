from django.contrib import admin
from django.urls import path, include
from adoption.views import LandingView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Landing page at root URL
    path('', LandingView.as_view(), name='landing'),
    
    # Adoption app URLs
    path('', include('adoption.urls')),
    
    # Pet adoption URLs
    path('pets/', include('pet_adoption.urls')),
    
    # User management
    path('management/', include('user_management.urls')),
    
    # ONLY use your custom auth URLs (NOT django.contrib.auth.urls)
    path('accounts/', include('security_management.urls')),
]