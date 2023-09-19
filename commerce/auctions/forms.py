from django.forms import ModelForm
from .models import auction
from django import forms

class CustomerForm(forms.ModelForm):
    class Meta:
        model = auction
        fields = ('item', 'starting_bid', 'description', 'image', 'category')
        
        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input item name'}),
            'starting_bid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter starting bid'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Item description'}),
            'image': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select category'}),
        }