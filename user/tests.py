from django.test import TestCase, Client
from django.urls import reverse, resolve

from .views import (
    SignUpView, VerifyCodeView,
    CustomLoginView, LogoutView,
    ProfileView, ProfileUpdateView,
    CustomPasswordChangeView
)
from .models import User, DoctorProfile, PatientProfile, Specialization
from .forms import CustomUserCreationForm

"""
Test for Models
"""


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            phone='09123456789'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.phone, '09123456789')
        self.assertEqual(self.user.balance, 0)

    def test_user_role_doctor(self):
        doctor = DoctorProfile.objects.create(user=self.user)
        self.assertEqual(self.user.get_role(), 'doctor')

    def test_user_role_patient(self):
        patient_user = User.objects.create_user(
            username='patientuser',
            password='password123',
            phone='09123456780'
        )
        PatientProfile.objects.create(user=patient_user)
        self.assertEqual(patient_user.get_role(), 'patient')

    def test_user_role_admin(self):
        admin_user = User.objects.create_user(
            username='adminuser',
            password='password123',
            phone='09123456781'
        )

        self.assertFalse(hasattr(admin_user, 'doctorprofile'))
        self.assertFalse(hasattr(admin_user, 'patientprofile'))
        self.assertEqual(admin_user.get_role(), 'admin')


class DoctorProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='doctoruser', phone='09123456780')
        self.specialization = Specialization.objects.create(name='Dermatology')
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.user,
            specialization=self.specialization,
            experience=10,
            visit_fee=50000
        )

    def test_doctor_profile_creation(self):
        self.assertEqual(self.doctor_profile.user.username, 'doctoruser')
        self.assertEqual(self.doctor_profile.specialization.name, 'Dermatology')
        self.assertEqual(self.doctor_profile.experience, 10)
        self.assertEqual(self.doctor_profile.visit_fee, 50000)


class SpecializationModelTest(TestCase):
    def setUp(self):
        self.specialization = Specialization.objects.create(name='Neurology')

    def test_specialization_creation(self):
        self.assertEqual(self.specialization.name, 'Neurology')


class PatientProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='patientuser',
            password='password123',
            phone='09123456781'
        )
        self.patient_profile = PatientProfile.objects.create(user=self.user)

    def test_patient_profile_creation(self):
        self.assertEqual(self.patient_profile.user.username, 'patientuser')


"""
Test for URLs
"""


class UrlsTest(TestCase):
    def test_signup_url_is_resolved(self):
        url = reverse('user:signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_verify_code_url_is_resolved(self):
        url = reverse('user:verify_code')
        self.assertEqual(resolve(url).func.view_class, VerifyCodeView)

    def test_login_url_is_resolved(self):
        url = reverse('user:login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_is_resolved(self):
        url = reverse('user:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_profile_url_is_resolved(self):
        url = reverse('user:profile')
        self.assertEqual(resolve(url).func.view_class, ProfileView)

    def test_profile_edit_url_is_resolved(self):
        url = reverse('user:profile_edit')
        self.assertEqual(resolve(url).func.view_class, ProfileUpdateView)

    def test_password_change_url_is_resolved(self):
        url = reverse('user:password_change')
        self.assertEqual(resolve(url).func.view_class, CustomPasswordChangeView)


"""
Test for Views
"""


class UserViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_signup_view(self):
        response = self.client.get(reverse('user:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_login_view(self):
        response = self.client.get(reverse('user:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/login.html')

    def test_profile_view_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('user:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_profile_view_not_authenticated(self):
        response = self.client.get(reverse('user:profile'))
        self.assertNotEqual(response.status_code, 200)


"""
Test for Forms
"""


class CustomUserCreationFormTest(TestCase):
    def test_form_valid_data(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'phone': '09123456789',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'doctor',
            'specialization': 'Cardiology'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form = CustomUserCreationForm(data={
            'username': 'newuser',
            'phone': '09123456789',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
            'role': 'doctor',
            'specialization': 'Cardiology'
        })
        self.assertFalse(form.is_valid())


