from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    email = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email address'
        })
    )
    new_username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username',
        }),
        label='Username'
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'maxlength': '150', 'minlength': '8'
        }),
        label='Password'
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password',
            'maxlength': '150', 'minlength': '8'
        }),
        label='Confirm Password'
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autofocus': 'autofocus'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'password'
        })
    )


class UserForm(forms.ModelForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        disabled=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control half_width input-group-sm',
            'placeholder': 'Your new username'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control half_width input-group-sm',
            'placeholder': 'Your first name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control half_width input-group-sm',
            'placeholder': 'Your last name'
        })
    )
    email = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control half_width input-group-sm',
            'placeholder': 'Email address'
        })
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name'
        )
