from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Remove 'role' from this list to hide the dropdown
        fields = ['username', 'email'] 

    def save(self, commit=True):
        user = super().save(commit=False)
        # Explicitly set the role to 'user' so new signups 
        # don't accidentally get higher permissions
        user.role = 'user' 
        if commit:
            user.save()
        return user

class AssignAnalystForm(forms.Form):
    email = forms.EmailField(
        label="User Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter user email to make Analyst"
        })
    )


