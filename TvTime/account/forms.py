from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=["user"]
        widgets = {
            "dob":forms.DateInput(attrs={"type":"date"}),
        }
