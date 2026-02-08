from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from security_management.decorators import admin_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Pet, AdoptionApplication
from .forms import PetForm, AdminApplicationForm
from django.shortcuts import render
from django.views.generic import TemplateView

@admin_required
def pet_list(request):
    """Admin-only view to manage all pets"""
    pets = Pet.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by availability
    status_filter = request.GET.get('status', '')
    if status_filter == 'available':
        pets = pets.filter(is_available=True, adopted=False)
    elif status_filter == 'adopted':
        pets = pets.filter(adopted=True)
    elif status_filter == 'unavailable':
        pets = pets.filter(is_available=False)
    
    # Get counts for stats
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(is_available=True, adopted=False).count()
    adopted_pets = Pet.objects.filter(adopted=True).count()
    pending_applications = AdoptionApplication.objects.filter(status='pending').count()
    
    context = {
        'pets': pets,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_pets': total_pets,
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
        'pending_applications': pending_applications,
    }
    return render(request, 'adoption/pages/pet_list.html', context)

@admin_required
def pet_create(request):
    """Admin-only view to create new pets"""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Pet "{pet.name}" has been created successfully!')
            return redirect('adoption:pet_list')
    else:
        form = PetForm()
    
    context = {
        'form': form,
        'title': 'Add New Pet',
        'action': 'Create',
    }
    return render(request, 'adoption/pages/adoption_form.html', context)

@admin_required
def pet_update(request, pk):
    """Admin-only view to update pets"""
    pet = get_object_or_404(Pet, pk=pk)
    
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Pet "{pet.name}" has been updated successfully!')
            return redirect('adoption:pet_list')
    else:
        form = PetForm(instance=pet)
    
    context = {
        'form': form,
        'pet': pet,
        'title': f'Update {pet.name}',
        'action': 'Update',
    }
    return render(request, 'adoption/pages/adoption_form.html', context)

@admin_required
def pet_delete(request, pk):
    """Admin-only view to delete pets"""
    pet = get_object_or_404(Pet, pk=pk)
    
    if request.method == 'POST':
        pet_name = pet.name
        pet.delete()
        messages.success(request, f'Pet "{pet_name}" has been deleted successfully!')
        return redirect('adoption:pet_list')
    
    context = {'pet': pet}
    return render(request, 'adoption/pages/adopt_confirm_delete.html', context)

@admin_required
def pet_detail(request, pk):
    """Admin-only detailed view of a pet"""
    pet = get_object_or_404(Pet, pk=pk)
    applications = pet.applications.all().order_by('-applied_date')
    
    # Get application counts by status
    status_counts = applications.values('status').annotate(count=Count('status'))
    
    context = {
        'pet': pet,
        'applications': applications,
        'status_counts': status_counts,
    }
    return render(request, 'adoption/pages/pet_detail.html', context)

@admin_required
def application_review(request, pk):
    """Admin review of an adoption application"""
    application = get_object_or_404(AdoptionApplication, pk=pk)
    
    if request.method == 'POST':
        form = AdminApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application has been updated!')
            return redirect('adoption:pet_detail', pk=application.pet.pk)
    else:
        form = AdminApplicationForm(instance=application)
    
    context = {
        'application': application,
        'form': form,
    }
    return render(request, 'adoption/pages/application_review.html', context)

@admin_required
def admin_dashboard(request):
    """Admin dashboard showing overview of system"""
    total_pets = Pet.objects.count()
    available_pets = Pet.objects.filter(is_available=True, adopted=False).count()
    adopted_pets = Pet.objects.filter(adopted=True).count()
    pending_applications = AdoptionApplication.objects.filter(status='pending').count()
    
    # Get recent applications
    recent_applications = AdoptionApplication.objects.all().order_by('-applied_date')[:5]
    
    context = {
        'total_pets': total_pets,
        'available_pets': available_pets,
        'adopted_pets': adopted_pets,
        'pending_applications': pending_applications,
        'recent_applications': recent_applications,
    }
    return render(request, 'adoption/pages/admin_dashboard.html', context)

@admin_required
def application_list(request):
    """Admin-only view to see all adoption applications"""
    applications = AdoptionApplication.objects.all().order_by('-applied_date')
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(full_name__icontains=search_query) |
            Q(pet__name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Get counts for each status
    all_applications = AdoptionApplication.objects.all()
    total_count = all_applications.count()
    pending_count = all_applications.filter(status='pending').count()
    under_review_count = all_applications.filter(status='under_review').count()
    approved_count = all_applications.filter(status='approved').count()
    rejected_count = all_applications.filter(status='rejected').count()
    cancelled_count = all_applications.filter(status='cancelled').count()
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_count': total_count,
        'pending_count': pending_count,
        'under_review_count': under_review_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'cancelled_count': cancelled_count,
    }
    return render(request, 'adoption/pages/application_list.html', context)

class LandingView(TemplateView):
    template_name = 'landing.html'