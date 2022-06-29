from django import forms
from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'email or username'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'password'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords Don\'t match')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'profile_photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
