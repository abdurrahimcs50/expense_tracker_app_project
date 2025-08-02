# forms.py
from django import forms
from .models import UserProfile  # or your user profile model

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile  # your model here
        fields = ['profession', 'Savings', 'income', 'image']
        widgets = {
            'profession': forms.Select(attrs={'class': 'form-select'}),
            'Savings': forms.NumberInput(attrs={'class': 'form-control'}),
            'income': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
