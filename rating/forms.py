from django import forms
from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rate']
        widgets = {
            'rate': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
