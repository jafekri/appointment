from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, DoctorUserCreationForm, VerifyCodeForm, CustomUserChangeForm
from .models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('verify_code')

    def get_form_class(self):
        print(self.request.path)
        if self.request.path == '/auth/register/':
            return CustomUserCreationForm
        else:
            return DoctorUserCreationForm
    
    def form_valid(self, form):
        self.request.session["phone_number"] = form.cleaned_data['phone']
        return super().form_valid(form)

class VerifyCodeView(FormView):
    template_name = 'user/verifyCode.html'
    form_class = VerifyCodeForm
    success_url = reverse_lazy('doctor:doctor_list')

    def form_valid(self, form):
        user_phone_number = self.request.session['phone_number']
        entred_code = form.cleaned_data.get('code')

        try:
            target_user = User.objects.get(phone=user_phone_number)
        except User.DoesNotExist:
            messages.error(request, 'No OTP code found for this phone number.', 'danger')
            return redirect('user:verify_code')

        # TODO: refactor otp exp flow
        expiration_time = target_user.date_joined + timedelta(minutes=2)
        if timezone.now() > expiration_time:
            messages.error(self.request, 'This code has expired. Please request a new one.', 'danger')
            return redirect('user:login')

        if entred_code == target_user.otp_code:
            return redirect('login')
        else:
            messages.error(self.request, 'Incorrect code', 'danger')
            return redirect('user:verify_code')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user/profile_edit.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user

