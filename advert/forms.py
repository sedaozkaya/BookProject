from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'listing_type', 'donation_type', 'price', 'page_count',
            'related_course', 'school_name', 'valid_year',
            'resolution_level', 'publish_year', 'publisher'
        ]
        widgets = {
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'donation_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'related_course': forms.TextInput(attrs={'class': 'form-control'}),
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'valid_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'resolution_level': forms.Select(attrs={'class': 'form-select'}),
            'publish_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control'}),
        }
