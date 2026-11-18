from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'detective@agency.com', 'autocomplete': 'email'
    }))
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'First Name', 'autocomplete': 'given-name'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'Last Name', 'autocomplete': 'family-name'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Choose Detective Handle', 'autocomplete': 'username'
        })
        # UserCreationForm field names are password1/password2.
        for field_name, placeholder in (
            ('password1', 'Enter Strong Password'),
            ('password2', 'Confirm Password'),
        ):
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': placeholder, 'autocomplete': 'new-password'
            })


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'Detective Handle or Username',
        'autocomplete': 'username', 'autofocus': True
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'placeholder': 'Password', 'autocomplete': 'current-password'
    }))


class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control bg-dark text-light border-secondary',
        'rows': 3,
        'placeholder': 'Investigation specialization or detective notes...'
    }))

    class Meta:
        model = UserProfile
        fields = ('bio',)
