# pet_adoption/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils import timezone
from adoption.models import Pet, AdoptionApplication
from adoption.forms import AdoptionApplicationForm, ApplicationReviewForm

# Staff required decorator
def staff_required(view_func):
    """Decorator to require staff status"""
    decorated_view_func = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url='/admin/login/'
    )(view_func)
    return decorated_view_func

def debug_pets(request):
    """Debug view to check pet data"""
    all_pets = Pet.objects.all().order_by('-created_at')
    available_pets = Pet.objects.filter(is_available=True, adopted=False)
    
    # Print to console for debugging
    print("\n=== PET DATABASE DEBUG ===")
    print(f"Total pets in database: {all_pets.count()}")
    print(f"Available pets (is_available=True, adopted=False): {available_pets.count()}")
    
    print("\nAll pets with status:")
    for pet in all_pets:
        print(f"  {pet.id}: '{pet.name}' - is_available={pet.is_available}, adopted={pet.adopted}, created={pet.created_at}")
    
    print("\nAvailable pets:")
    for pet in available_pets:
        print(f"  {pet.id}: '{pet.name}'")
    print("====================\n")
    
    context = {
        'all_pets': all_pets,
        'available_pets': available_pets,
        'total_count': all_pets.count(),
        'available_count': available_pets.count(),
    }
    return render(request, 'pet_adoption/debug.html', context)

def test_add_pet(request):
    """Test adding a pet programmatically (admin only)"""
    if request.user.is_superuser:
        try:
            pet = Pet.objects.create(
                name="DEBUG Test Pet",
                breed="Mixed",
                age=3,
                description="This is a test pet added via debug view",
                is_dog=True,
                is_cat=False,
                is_available=True,
                adopted=False,
                gender='male',
                size='medium',
                color='Brown',
                vaccination_status='up_to_date',
                intake_date=timezone.now().date()
            )
            messages.success(request, f'Test pet "{pet.name}" created successfully! ID: {pet.id}')
            return redirect('pet_adoption:debug_pets')
        except Exception as e:
            messages.error(request, f'Error creating test pet: {str(e)}')
            return redirect('pet_adoption:debug_pets')
    messages.error(request, 'Only superusers can access this function')
    return redirect('pet_adoption:pet_list')

@login_required(login_url='login')
def pet_list(request):
    """User-facing gallery of available pets"""
    # DEBUG: Print current filter
    print(f"\n[PET_LIST] Filtering: is_available=True, adopted=False")
    
    pets = Pet.objects.filter(
        is_available=True,
        adopted=False
    ).order_by('-created_at')
    
    # DEBUG: Print results
    print(f"[PET_LIST] Found {pets.count()} available pets")
    for pet in pets:
        print(f"  [PET_LIST] Showing: {pet.id} - {pet.name}")
    
    search_query = request.GET.get('search', '')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        print(f"[PET_LIST] After search '{search_query}': {pets.count()} pets")
    
    paginator = Paginator(pets, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'total_pets': pets.count(),
    }
    return render(request, 'pet_adoption/pages/pet_list.html', context)

@login_required(login_url='login')
def pet_detail(request, pet_id):
    """User-facing pet detail view"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    # DEBUG
    print(f"\n[PET_DETAIL] Viewing pet {pet.id}: {pet.name}")
    print(f"  [PET_DETAIL] Status: is_available={pet.is_available}, adopted={pet.adopted}")
    
    # Check if pet should be visible
    if not pet.is_available or pet.adopted:
        messages.warning(request, f"{pet.name} is not currently available for adoption.")
    
    # Check if user has already applied
    user_has_applied = False
    if request.user.is_authenticated:
        user_has_applied = AdoptionApplication.objects.filter(
            pet=pet, user=request.user
        ).exists()
    
    context = {
        'pet': pet,
        'user_has_applied': user_has_applied,
        'can_adopt': pet.is_available and not pet.adopted,
        'is_visible': pet.is_available and not pet.adopted,
    }
    return render(request, 'pet_adoption/pages/pet_detail.html', context)

@login_required
def adoption_application(request, pet_id):
    """User adoption application"""
    pet = get_object_or_404(Pet, id=pet_id)
    
    # Check if pet is adoptable
    if not pet.is_available or pet.adopted:
        messages.error(request, f"Sorry, {pet.name} is not available for adoption.")
        return redirect('pet_adoption:pet_detail', pet_id=pet_id)
    
    # Check if already applied
    if AdoptionApplication.objects.filter(pet=pet, user=request.user).exists():
        messages.warning(request, 'You have already applied to adopt this pet.')
        return redirect('pet_adoption:pet_detail', pet_id=pet_id)
    
    if request.method == 'POST':
        form = AdoptionApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.pet = pet
            application.user = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('pet_adoption:my_applications')
    else:
        form = AdoptionApplicationForm()
    
    context = {
        'form': form,
        'pet': pet,
    }
    return render(request, 'pet_adoption/pages/adoption_application.html', context)

@login_required
def my_applications(request):
    """User's adoption applications with filtering"""
    print(f"\n=== MY_APPLICATIONS DEBUG ===")
    print(f"User: {request.user}")
    
    # Get all applications for the user
    all_applications = AdoptionApplication.objects.filter(user=request.user).order_by('-applied_date')
    
    # Debug: Print all applications and their statuses
    print(f"Total applications found: {all_applications.count()}")
    for app in all_applications:
        print(f"  App {app.id}: Pet='{app.pet.name}', Status='{app.status}'")
    
    # Calculate counts for each status
    status_counts = {
        'all': all_applications.count(),
        'pending': all_applications.filter(status='pending').count(),
        'under_review': all_applications.filter(status='under_review').count(),
        'approved': all_applications.filter(status='approved').count(),
        'rejected': all_applications.filter(status='rejected').count(),
        'cancelled': all_applications.filter(status='cancelled').count(),
    }
    
    print(f"Status counts: {status_counts}")
    print("====================\n")
    
    # Apply status filter if provided
    status_filter = request.GET.get('status', '')
    applications = all_applications
    if status_filter and status_filter != 'all':
        applications = applications.filter(status=status_filter)
        print(f"Filtered by status '{status_filter}': {applications.count()} apps")
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'status_counts': status_counts,
    }
    
    # Disable caching for this page
    response = render(request, 'pet_adoption/pages/my_applications.html', context)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

def json_debug(request):
    """JSON endpoint for debugging"""
    all_pets = Pet.objects.all().values('id', 'name', 'is_available', 'adopted', 'created_at')
    available_pets = Pet.objects.filter(is_available=True, adopted=False).values('id', 'name')
    
    return JsonResponse({
        'total_pets': len(all_pets),
        'available_pets': len(available_pets),
        'all_pets': list(all_pets),
        'available_pets_list': list(available_pets),
        'filter_query': str(Pet.objects.filter(is_available=True, adopted=False).query),
    })

@login_required
def debug_applications(request):
    """Debug view to check application status directly"""
    print("\n=== DEBUG APPLICATIONS ===")
    
    # 1. Check all applications in database
    all_apps = AdoptionApplication.objects.all()
    print(f"Total applications in database: {all_apps.count()}")
    
    for app in all_apps:
        print(f"  ID: {app.id}, User: {app.user.username}, Pet: {app.pet.name}, Status: {app.status}")
    
    # 2. Check current user's applications
    user_apps = AdoptionApplication.objects.filter(user=request.user)
    print(f"\nYour applications: {user_apps.count()}")
    for app in user_apps:
        print(f"  ID: {app.id}, Pet: {app.pet.name}, Status: '{app.status}'")
    
    # 3. Check raw SQL query
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, status, user_id FROM adoption_adoptionapplication")
        rows = cursor.fetchall()
        print(f"\nRaw SQL data from adoption_adoptionapplication table:")
        for row in rows:
            print(f"  ID: {row[0]}, Status: '{row[1]}', User ID: {row[2]}")
    
    print("==========================\n")
    
    return render(request, 'pet_adoption/debug_applications.html', {
        'all_apps': all_apps,
        'user_apps': user_apps,
    })

@staff_required
def review_application(request, application_id):
    """Staff review page for adoption applications"""
    application = get_object_or_404(AdoptionApplication, id=application_id)
    
    print(f"\n[REVIEW PAGE] Loading application {application_id} for review")
    print(f"[REVIEW PAGE] Current status: {application.status}")
    print(f"[REVIEW PAGE] User: {request.user.username} (Staff: {request.user.is_staff})")
    
    if request.method == 'POST':
        form = ApplicationReviewForm(request.POST, instance=application)
        if form.is_valid():
            # Get old status before saving
            old_status = application.status
            new_status = form.cleaned_data['status']
            
            print(f"[REVIEW PAGE] Status changing from '{old_status}' to '{new_status}'")
            
            # Save the form
            application = form.save(commit=False)
            
            # Auto-update dates based on status changes
            if old_status == 'pending' and new_status != 'pending' and not application.reviewed_date:
                application.reviewed_date = timezone.now()
                print(f"[REVIEW PAGE] Setting reviewed_date: {application.reviewed_date}")
            
            if new_status in ['approved', 'rejected'] and not application.decision_date:
                application.decision_date = timezone.now()
                print(f"[REVIEW PAGE] Setting decision_date: {application.decision_date}")
            
            # Auto-update pet status if approved
            if new_status == 'approved' and not application.pet.adopted:
                application.pet.adopted = True
                application.pet.is_available = False
                application.pet.save()
                print(f"[REVIEW PAGE] Marked pet '{application.pet.name}' as adopted")
            
            # Handle email notifications
            send_email = form.cleaned_data.get('send_email', 'no')
            if send_email != 'no' and new_status != old_status:
                # Here you would implement email sending
                # For now, just log it
                print(f"[REVIEW PAGE] Would send email notification (type: {send_email})")
                if send_email == 'custom':
                    custom_message = form.cleaned_data.get('custom_email_message')
                    print(f"[REVIEW PAGE] Custom message: {custom_message[:50]}...")
            
            # Save the application
            application.save()
            
            # Show success message
            status_display = dict(AdoptionApplication.STATUS_CHOICES).get(new_status, new_status)
            messages.success(
                request, 
                f"✓ Application #{application.id} updated to '{status_display}'."
            )
            
            # Redirect to stay on the same page
            return redirect('pet_adoption:review_application', application_id=application.id)
        else:
            messages.error(request, "Please correct the errors below.")
            print(f"[REVIEW PAGE] Form errors: {form.errors}")
    else:
        form = ApplicationReviewForm(instance=application)
    
    # Calculate days since application
    days_since = (timezone.now() - application.applied_date).days
    
    context = {
        'application': application,
        'form': form,
        'days_since': days_since,
        'status_choices': dict(AdoptionApplication.STATUS_CHOICES),
    }
    
    return render(request, 'adoption/pages/application_review.html', context)

@staff_required
def application_list_staff(request):
    """Staff view of all adoption applications"""
    applications = AdoptionApplication.objects.all().order_by('-applied_date')
    
    # Filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Counts for stats
    status_counts = {
        'all': AdoptionApplication.objects.count(),
        'pending': AdoptionApplication.objects.filter(status='pending').count(),
        'under_review': AdoptionApplication.objects.filter(status='under_review').count(),
        'approved': AdoptionApplication.objects.filter(status='approved').count(),
        'rejected': AdoptionApplication.objects.filter(status='rejected').count(),
        'cancelled': AdoptionApplication.objects.filter(status='cancelled').count(),
    }
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'status_counts': status_counts,
        'status_choices': dict(AdoptionApplication.STATUS_CHOICES),
    }
    
    return render(request, 'pet_adoption/pages/application_list_staff.html', context)

@login_required
def test_admin_update(request):
    """Test if admin updates work"""
    print("\n=== TEST ADMIN UPDATE ===")
    
    # Get first application
    if AdoptionApplication.objects.exists():
        app = AdoptionApplication.objects.first()
        print(f"Testing Application ID: {app.id}")
        print(f"Current status in database: '{app.status}'")
        print(f"Pet: {app.pet.name}")
        print(f"User: {app.user.username}")
        
        # Try to update it
        old_status = app.status
        new_status = 'approved' if old_status != 'approved' else 'under_review'
        
        print(f"\nAttempting to change status from '{old_status}' to '{new_status}'...")
        app.status = new_status
        app.save()
        
        # Refresh from database
        app.refresh_from_db()
        print(f"After save: status = '{app.status}'")
        
        if app.status == new_status:
            print("✓ SUCCESS: Database updated!")
        else:
            print("✗ FAILED: Database not updated!")
    else:
        print("No applications found in database")
    
    print("=======================\n")
    
    from django.http import HttpResponse
    return HttpResponse("Check console for test results")

    # pet_adoption/views.py - Add this function at the end

@login_required
def status_test(request):
    """Test if status updates are working"""
    from adoption.models import AdoptionApplication
    from django.http import HttpResponse
    import json
    
    print("\n" + "="*80)
    print("STATUS TEST - COMPLETE DEBUG")
    print("="*80)
    
    results = []
    
    # Test 1: Check current user
    results.append(f"User: {request.user.username} (ID: {request.user.id})")
    print(f"[TEST] User: {request.user.username}")
    
    # Test 2: Check all applications in database
    all_apps = AdoptionApplication.objects.all()
    results.append(f"Total applications in DB: {all_apps.count()}")
    print(f"[TEST] Total applications: {all_apps.count()}")
    
    for app in all_apps:
        info = f"App {app.id}: User='{app.user.username}', Pet='{app.pet.name}', Status='{app.status}'"
        results.append(info)
        print(f"[TEST] {info}")
    
    # Test 3: Check current user's applications
    user_apps = AdoptionApplication.objects.filter(user=request.user)
    results.append(f"\nYour applications: {user_apps.count()}")
    print(f"[TEST] Your applications: {user_apps.count()}")
    
    for app in user_apps:
        info = f"Your App {app.id}: Pet='{app.pet.name}', Status='{app.status}'"
        results.append(info)
        print(f"[TEST] {info}")
        
        # Try a direct update
        print(f"[TEST] Testing direct update for app {app.id}...")
        old_status = app.status
        new_status = 'approved' if old_status != 'approved' else 'under_review'
        
        app.status = new_status
        app.save()
        
        # Refresh from database
        app.refresh_from_db()
        
        if app.status == new_status:
            results.append(f"✓ Direct update SUCCESS: {old_status} → {new_status}")
            print(f"[TEST] ✓ Direct update SUCCESS: {old_status} → {new_status}")
        else:
            results.append(f"✗ Direct update FAILED: still {app.status}")
            print(f"[TEST] ✗ Direct update FAILED: still {app.status}")
    
    print("="*80 + "\n")
    
    # Return results as HTML
    html = f"""
    <html>
    <head>
        <title>Status Test</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            .success {{ color: green; font-weight: bold; }}
            .error {{ color: red; font-weight: bold; }}
            .info {{ color: blue; }}
            pre {{ background: #f5f5f5; padding: 20px; border-radius: 10px; }}
        </style>
    </head>
    <body>
        <h1>Status Update Test</h1>
        <p>Check the console/terminal for detailed debug output.</p>
        
        <h2>Test Results:</h2>
        <pre>{chr(10).join(results)}</pre>
        
        <h2>Next Steps:</h2>
        <ol>
            <li>Open this page in a new tab: <a href="/pet_adoption/my-applications/" target="_blank">My Applications</a></li>
            <li>Note the status shown</li>
            <li>Go to admin: <a href="/admin/adoption/adoptionapplication/" target="_blank">Admin Panel</a></li>
            <li>Change status and SAVE</li>
            <li>Refresh the "My Applications" page</li>
            <li>Status should update immediately</li>
        </ol>
        
        <h2>Debug Links:</h2>
        <ul>
            <li><a href="/pet_adoption/debug-applications/">Debug Applications</a></li>
            <li><a href="/pet_adoption/test-admin-update/">Test Admin Update</a></li>
            <li><a href="/admin/">Django Admin</a></li>
        </ul>
    </body>
    </html>
    """
    
    return HttpResponse(html)