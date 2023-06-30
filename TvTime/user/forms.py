from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one digit.")

        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("Password must contain at least one letter.")

        # Check for any other password validation conditions here

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2
    
class UserForm(CustomUserCreationForm):
    class Meta:
        model=User
        fields=[
            'email',
            'username',
            'password1','password2',
            
        ]


class UserLoginForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput())
    password=forms.CharField(max_length=100,widget=forms.TextInput())