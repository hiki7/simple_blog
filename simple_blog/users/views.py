from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Follow
from .forms import ProfileForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST

@require_POST
def custom_logout(request):
    logout(request)
    return redirect('post_list')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/registration.html', {'form': form})


@login_required
def profile_view(request, id):
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.filter(user=user).first()

    if not profile:
        return render(request, 'users/profile_not_found.html')  # Render a template showing profile not found

    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'users/profile.html', {
        'profile': profile,
        'is_following': is_following,
        'profile_user': user  # Add this line
    })


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', id=request.user.id)  # Redirect by 'id'
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def follow_user(request, id):
    user = get_object_or_404(User, id=id)
    if not Follow.objects.filter(follower=request.user, following=user).exists():
        Follow.objects.create(follower=request.user, following=user)
    return redirect('profile_view', id=id)

@login_required
def unfollow_user(request, id):
    user = get_object_or_404(User, id=id)
    Follow.objects.filter(follower=request.user, following=user).delete()
    return redirect('profile_view', id=id)
