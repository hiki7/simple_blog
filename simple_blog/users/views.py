from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Follow


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
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()
    return render(request, 'users/profile.html', {'profile': profile, 'is_following': is_following})

@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile_edit.html', {'form': form})

@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    if not Follow.objects.filter(follower=request.user, following=user).exists():
        Follow.objects.create(follower=request.user, following=user)
    return redirect('profile_view', username=username)

@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(follower=request.user, following=user).delete()
    return redirect('profile_view', username=username)
