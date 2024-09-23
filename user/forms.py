import random
from email.policy import default
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Specialization, DoctorProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('first_name',
                                                'last_name',
                                                'username',
                                                'phone')
        
    def save(self, commit=True):
        code = random.randint(1000, 9999)
        print(f"code: {code}")
        obj = super().save(False)
        obj.otp_code = code
        obj.save()
        return obj


class DoctorUserCreationForm(CustomUserCreationForm):
    
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all())
    consultation_fee = forms.IntegerField()
    

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control form-control-lg'})

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ['old_password', 'new_password1', 'new_password2']
