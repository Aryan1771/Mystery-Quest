from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'detective@agency.com'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Last Name'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control bg-dark text-light border-secondary',
            'placeholder': 'Choose Detective Handle'
        })
        if 'password_1' in self.fields:
            self.fields['password_1'].widget.attrs.update({
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'Enter Strong Password'
            })
        if 'password_2' in self.fields:
            self.fields['password_2'].widget.attrs.update({
                'class': 'form-control bg-dark text-light border-secondary',
                'placeholder': 'Confirm Password'
            })


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Detective Handle or Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Password'})
    )


class UserProfileUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control bg-dark text-light border-secondary', 'rows': 3, 'placeholder': 'Investigation specialization or detective notes...'})
    )

    class Meta:
        model = UserProfile
        fields = ('bio',)
