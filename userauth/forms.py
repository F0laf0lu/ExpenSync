from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from django.forms import FileInput, ImageField


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email"]

    # Customize fields individually
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'firstname'})
    )

    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lastname'})
    )

    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'})
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'})
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm password'}),
        strip=False,
    )



class CustomUserChangeForm(UserChangeForm):
    avatar = ImageField(widget=FileInput)
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "avatar"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}), 
        }