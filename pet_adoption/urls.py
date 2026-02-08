# pet_adoption/urls.py (USER-FACING)
from django.urls import path
from . import views

app_name = 'pet_adoption'

urlpatterns = [
    # User-facing adoption routes
    path('', views.pet_list, name='pet_list'),  # This is the gallery
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('apply/<int:pet_id>/', views.adoption_application, name='adoption_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    
    # Staff review routes (only accessible to staff users)
    path('staff/applications/', views.application_list_staff, name='application_list_staff'),
    path('staff/applications/<int:application_id>/review/', views.review_application, name='review_application'),
    
    # Debug routes (temporary - remove in production)
    path('debug/', views.debug_pets, name='debug_pets'),
    path('debug/add-test-pet/', views.test_add_pet, name='test_add_pet'),
    path('debug/json/', views.json_debug, name='json_debug'),
    path('debug-applications/', views.debug_applications, name='debug_applications'),
    
    # Test routes
    path('test-admin-update/', views.test_admin_update, name='test_admin_update'),
    path('status-test/', views.status_test, name='status_test'),
]