from django.urls import path
from . import views

app_name = 'adoption'

urlpatterns = [
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Make /adoption/ show pet list
    path('', views.pet_list, name='pet_list'),  # Changed from 'pets/' to ''
    
    # Update other URLs
    path('create/', views.pet_create, name='pet_create'),
    path('<int:pk>/', views.pet_detail, name='pet_detail'),
    path('<int:pk>/update/', views.pet_update, name='pet_update'),
    path('<int:pk>/delete/', views.pet_delete, name='pet_delete'),
    
    # Applications
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/review/', views.application_review, name='application_review'),
]