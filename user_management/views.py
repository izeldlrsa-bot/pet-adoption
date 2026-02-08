from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserCreateForm, UserEditForm, AdminProfileForm
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden

# Helper function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_staff

# --- NEW: PROFILE VIEW ---
@login_required
def profile_view(request):
    """
    Renders the profile page for the currently logged-in user.
    """
    return render(request, 'user_management/profile.html', {
        'user': request.user
    })

# --- USER LIST VIEW ---
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all().order_by('-date_joined')
    
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            username__icontains=search_query
        ) | users.filter(
            email__icontains=search_query
        ) | users.filter(
            first_name__icontains=search_query
        ) | users.filter(
            last_name__icontains=search_query
        )
    
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'users': page_obj.object_list,
        'search_query': search_query,
    }
    # Path updated to reflect separate app structure
    return render(request, 'user_management/pages/user_list.html', context)

# --- USER CREATE VIEW ---
@login_required
@user_passes_test(is_admin)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('user_management:user_list')
    else:
        form = UserCreateForm()
    
    context = {'form': form}
    return render(request, 'user_management/pages/user_create.html', context)

# --- USER DETAIL VIEW ---
@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {'user': user}
    return render(request, 'user_management/pages/user_detail.html', context)

# --- ADMIN CREATE VIEW ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_create(request):
    if request.method == 'POST':
        form = AdminProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Admin {user.username} created successfully!')
            return redirect('user_management:user_list')
    else:
        form = AdminProfileForm()
    
    context = {'form': form}
    return render(request, 'user_management/pages/admin_create.html', context)

# --- USER EDIT VIEW ---
@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    
    if user_obj.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Only superusers can edit other superusers.')
        return redirect('user_management:user_list')
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_obj.username} updated successfully!')
            return redirect('user_management:user_detail', user_id=user_obj.id)
    else:
        form = UserEditForm(instance=user_obj)
    
    context = {
        'form': form,
        'user': user_obj,
    }
    return render(request, 'user_management/pages/user_edit.html', context)

# --- TOGGLE STATUS VIEWS ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_toggle_active(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj == request.user:
        messages.error(request, 'You cannot deactivate your own account.')
        return redirect('user_management:user_detail', user_id=user_obj.id)
    
    user_obj.is_active = not user_obj.is_active
    user_obj.save()
    status = "activated" if user_obj.is_active else "deactivated"
    messages.success(request, f'User {user_obj.username} has been {status}.')
    return redirect('user_management:user_detail', user_id=user_obj.id)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_toggle_staff(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj == request.user:
        messages.error(request, 'You cannot change your own staff status.')
        return redirect('user_management:user_detail', user_id=user_obj.id)
    
    user_obj.is_staff = not user_obj.is_staff
    user_obj.save()
    status = "granted staff privileges" if user_obj.is_staff else "removed staff privileges"
    messages.success(request, f'User {user_obj.username} has been {status}.')
    return redirect('user_management:user_detail', user_id=user_obj.id)

# --- USER DELETE VIEW ---
@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('user_management:user_detail', user_id=user_obj.id)
    
    if request.method == 'POST':
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f'User {username} has been deleted.')
        return redirect('user_management:user_list')
    
    context = {'user': user_obj}
    return render(request, 'user_management/pages/user_confirm_delete.html', context)