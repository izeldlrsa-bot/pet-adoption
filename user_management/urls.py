from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('create-admin/', views.admin_create, name='admin_create'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('<int:user_id>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('<int:user_id>/toggle-staff/', views.user_toggle_staff, name='user_toggle_staff'),
    path('<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('profile/', views.profile_view, name='profile'),
]