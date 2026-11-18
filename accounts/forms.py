from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
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



class SecurityQuestionForm(forms.Form):
    security_question = forms.ChoiceField(
        choices=UserProfile.SECURITY_QUESTION_CHOICES,
        label='Security question',
        widget=forms.Select(attrs={'class': 'form-select bg-dark text-light border-secondary'})
    )
    security_answer = forms.CharField(
        min_length=3, max_length=200, label='Your answer',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-light border-secondary',
            'autocomplete': 'off', 'placeholder': 'Enter an answer only you will remember'
        })
    )

    def clean_security_answer(self):
        answer = self.cleaned_data['security_answer'].strip().casefold()
        if len(answer) < 3:
            raise forms.ValidationError('Please enter at least 3 characters.')
        return answer


class RecoveryForm(forms.Form):
    username = forms.CharField(max_length=150)
    security_answer = forms.CharField(widget=forms.PasswordInput())
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('new_password1') and cleaned.get('new_password2'):
            if cleaned['new_password1'] != cleaned['new_password2']:
                self.add_error('new_password2', 'The passwords do not match.')
            else:
                try:
                    validate_password(cleaned['new_password1'])
                except forms.ValidationError as exc:
                    self.add_error('new_password1', exc)
        if cleaned.get('security_answer'):
            cleaned['security_answer'] = cleaned['security_answer'].strip().casefold()
        return cleaned
