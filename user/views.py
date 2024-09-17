import random
from datetime import timedelta
from django.utils import timezone

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView,  PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from .forms import (CustomUserCreationForm, CustomAuthenticationForm,
                    VerifyCodeForm, CustomUserChangeForm,
                    CustomPasswordChangeForm,)
from .models import User, DoctorProfile, PatientProfile, Specialization
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, UpdateView


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('user:verify_code')

    def form_valid(self, form):
        code = random.randint(1000, 9999)
        print(f"code: {code}")
        form.cleaned_data['otp_code'] = code
        user = form.save(commit=False)
        user.otp_code = code
        user.save()

        role = form.cleaned_data.get('role')
        specialization_name = form.cleaned_data.get('specialization')
        visit_fee = form.cleaned_data.get('consultation_fee')
        if role == 'doctor':
            if specialization_name:
                specialization, created = Specialization.objects.get_or_create(name=specialization_name)
                DoctorProfile.objects.create(user=user, specialization=specialization, visit_fee=visit_fee)
            else:
                messages.error(self.request, 'Please provide a specialization for the doctor.', 'danger')
                return self.form_invalid(form)
        elif role == 'patient':
            PatientProfile.objects.create(user=user)

        self.request.session['user_info'] = {
            'phone_number': form.cleaned_data['phone'],
            'username': form.cleaned_data['username'],
            'password': form.cleaned_data['password1'],
        }
        messages.success(self.request, 'We send a Code.', 'success')
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class VerifyCodeView(View):
    verify_form = VerifyCodeForm

    def get(self, request):
        form = self.verify_form()
        return render(request, 'user/verifyCode.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_info']
        form = self.verify_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            try:
                code_instance = User.objects.get(phone=user_session['phone_number'], otp_code=cd['code'])
            except User.DoesNotExist:
                messages.error(request, 'No OTP code found for this phone number.', 'danger')
                return redirect('user:verify_code')

            expiration_time = code_instance.date_joined + timedelta(minutes=2)
            if timezone.now() > expiration_time:
                messages.error(request, 'This code has expired. Please request a new one.', 'danger')
                return redirect('user:login')

            if cd['code'] == code_instance.otp_code:
                user_login = authenticate(request, username=user_session['username'], password=user_session['password'])
                if user_login:
                    login(request, user_login)
                    messages.success(request, 'You have logged in successfully', 'success')
                    return redirect('user:profile')
            else:
                messages.error(request, 'Incorrect code', 'danger')
                return redirect('user:verify_code')

        return render(request, 'user/verifyCode.html', {'form': form})


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('user:profile')


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you log out successfully')
        return render(request,'base.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'user/profile_edit.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('user:password_change_done')
