from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView  # Add this import

urlpatterns = [
    path('login/', views.custom_login, name='login'),  # Add this line
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),  # Changed from views.logout
]