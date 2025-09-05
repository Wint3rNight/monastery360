"""
Authentication views for Monastery360.

Handles user registration, login, logout, and profile management.
"""

from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form with additional fields."""

    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form that allows login with email or username."""

    def clean_username(self):
        username = self.cleaned_data['username']

        # Check if the input is an email
        if '@' in username:
            try:
                # Try to find user by email
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                pass  # Let the normal authentication handle the error

        return username


def login_view(request):
    """Handle user login and registration."""

    if request.user.is_authenticated:
        return redirect('core:home')

    login_form = CustomAuthenticationForm()
    signup_form = CustomUserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            # Handle login
            login_form = CustomAuthenticationForm(data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                    next_url = request.GET.get('next', reverse('core:home'))
                    return redirect(next_url)
                else:
                    messages.error(request, 'Invalid username/email or password.')
            else:
                messages.error(request, 'Please correct the errors below.')

        elif 'signup_submit' in request.POST:
            # Handle signup
            signup_form = CustomUserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, f'Welcome to Monastery360, {user.first_name}!')
                return redirect('core:home')
            else:
                messages.error(request, 'Please correct the errors below.')

    return render(request, 'auth/login_test.html', {
        'login_form': login_form,
        'signup_form': signup_form,
        'show_signup': request.GET.get('signup') == 'true',
    })


@require_http_methods(["POST"])
def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('core:home')


def signup_redirect(request):
    """Redirect to login page with signup form active."""
    return redirect('core:login' + '?signup=true')


@login_required
def profile_view(request):
    """User profile view."""
    return render(request, 'auth/profile.html', {
        'user': request.user,
    })


@login_required
@require_http_methods(["POST"])
def profile_update_view(request):
    """Handle profile updates."""
    try:
        user = request.user

        # Update user fields
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()

        # Validate email uniqueness (excluding current user)
        if email and email != user.email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)

        # Update user fields
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email

        user.save()

        return JsonResponse({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
