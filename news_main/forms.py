from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']
        
class UserProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['avatar' , 'full_name' , 'bio']
        widgets = {
            'bio':forms.Textarea(attrs={'class': 'form-control','rows':3}),
        }

