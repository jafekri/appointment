from email.policy import default

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Specialization, DoctorProfile
from django.contrib.auth.forms import PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]

    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all(), required=False)
    consultation_fee = forms.IntegerField()


    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'phone',
                  'password1',
                  'password2',
                   'role',
                  'specialization',
                  'consultation_fee',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.data.get('role') == 'doctor':
                self.fields['specialization'].required = True  # فیلد تخصص را اجباری می‌کنیم
                self.fields['consultation_fee'].required = True  # فیلد تخصص را اجباری می‌کنیم
            else:
                self.fields['specialization'].widget = forms.HiddenInput()  # مخفی کردن فیلد تخصص برای نقش‌های دیگر
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        else:
            return cd['password2']

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username',
                  'password',)


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
