import hashlib
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import UserRegistrationForm, UserLoginForm, UserProfileUpdateForm, SecurityQuestionForm, RecoveryForm
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

    if request.method == 'POST' and request.POST.get('form_type') == 'security':
        security_form = SecurityQuestionForm(request.POST)
        if security_form.is_valid():
            profile.security_question = security_form.cleaned_data['security_question']
            profile.security_answer_hash = make_password(security_form.cleaned_data['security_answer'])
            profile.save(update_fields=['security_question', 'security_answer_hash'])
            messages.success(request, 'Your account recovery question has been saved securely.')
            return redirect('profile')
    else:
        security_form = SecurityQuestionForm(initial={'security_question': profile.security_question} if profile.security_question else None)

    if request.method == 'POST' and request.POST.get('form_type') == 'bio':
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
        'security_form': security_form,
        'user_progresses': user_progresses,
        'accusations': accusations,
    })



def forgot_password_view(request):
    from django.contrib.auth.models import User
    stage, question, username, message, form = 'username', None, '', None, None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        key = 'recovery:' + hashlib.sha256((username.casefold() + ':' + ip).encode()).hexdigest()
        attempts = cache.get(key, 0)
        if attempts >= 5:
            return render(request, 'accounts/forgot_password.html', {
                'stage': 'locked', 'message': 'Too many attempts. Please try again in 15 minutes.'
            })
        user = User.objects.filter(username__iexact=username).select_related('profile').first()
        if 'security_answer' not in request.POST:
            if not user or not user.profile.has_recovery_setup:
                return render(request, 'accounts/forgot_password.html', {
                    'stage': 'username', 'message': 'No recovery question is configured for those details.'
                })
            return render(request, 'accounts/forgot_password.html', {
                'stage': 'answer', 'username': user.username,
                'question': user.profile.get_security_question_display()
            })
        form = RecoveryForm(request.POST)
        if form.is_valid():
            valid = bool(user and user.profile.has_recovery_setup and check_password(
                form.cleaned_data['security_answer'], user.profile.security_answer_hash
            ))
            if not valid:
                cache.set(key, attempts + 1, 900)
                return render(request, 'accounts/forgot_password.html', {
                    'stage': 'answer', 'username': username,
                    'question': user.profile.get_security_question_display() if user and user.profile.has_recovery_setup else 'Your account recovery question',
                    'message': 'The recovery details could not be verified.'
                })
            user.set_password(form.cleaned_data['new_password1'])
            user.save(update_fields=['password'])
            cache.delete(key)
            messages.success(request, 'Your password has been changed. You can now sign in.')
            return redirect('login')
        stage = 'answer'
        question = user.profile.get_security_question_display() if user and user.profile.has_recovery_setup else 'Your account recovery question'
    return render(request, 'accounts/forgot_password.html', {
        'stage': stage, 'question': question, 'username': username,
        'message': message, 'form': form
    })
