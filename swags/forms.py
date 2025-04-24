from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Swag

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SwagForm(forms.ModelForm):
    class Meta:
        model = Swag
        fields = ['name', 'photo', 'company', 'conference', 'rating', 'comments']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class SwagSearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search swags...'})
    )