from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm
from .models import UserProfile
from investigation.models import UserCaseProgress, Accusation


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Avoid leaving a user row behind if profile creation fails.
            with transaction.atomic():
                user = form.save()
            messages.success(
                request,
                f"Welcome to Mystery Quest, Detective {user.username}! Your badge has been issued. Log in to commence duty."
            )
            return redirect('login')
        messages.error(request, "Registration failed. Please check the details entered below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Restore a missing profile for older accounts without changing existing stats.
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Access granted. Welcome back, Detective {user.username}.")

            next_url = request.POST.get('next') or request.GET.get('next')
            if not url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                next_url = settings.LOGIN_REDIRECT_URL
            return redirect(next_url)
        messages.error(request, "Invalid detective credentials. Access denied.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have securely signed out of headquarters.")
    return redirect('home')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Detective dossier updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=profile)

    user_progresses = UserCaseProgress.objects.filter(user=request.user).select_related('case')
    accusations = Accusation.objects.filter(user=request.user).select_related('case', 'selected_suspect')
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form,
        'user_progresses': user_progresses,
        'accusations': accusations,
    })
