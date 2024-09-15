from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import DoctorModel, Specialization

User = get_user_model()


class DoctorModelTests(TestCase):
    def setUp(self):
        self.cardiologist = Specialization.objects.create(name='Cardiologist')
        self.dermatologist = Specialization.objects.create(name='Dermatologist')

        self.user1 = User.objects.create_user(username='doctor1', password='pass', phone='1234567890')
        self.user2 = User.objects.create_user(username='doctor2', password='pass', phone='0987654321')

        self.doctor1 = DoctorModel.objects.create(
            user=self.user1,
            specialization=self.cardiologist,
            experience_year=10,
            visit_fee=150
        )
        self.doctor2 = DoctorModel.objects.create(
            user=self.user2,
            specialization=self.dermatologist,
            experience_year=5,
            visit_fee=100
        )


class DoctorListViewTests(DoctorModelTests):
    def test_doctor_list_view(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/doctor_list.html')
        self.assertContains(response, self.doctor1.specialization.name)
        self.assertContains(response, self.doctor2.specialization.name)

    def test_doctor_list_view_requires_login(self):
        response = self.client.get(reverse('doctor:doctor_list'))
        self.assertEqual(response.status_code, 302)


class DoctorDetailViewTests(DoctorModelTests):
    def test_doctor_detail_view(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[self.doctor1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor1.specialization.name)

    def test_doctor_detail_view_not_accessible_by_other_user(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[self.doctor2.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_doctor_detail_view_invalid_id(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[999]))  # ID does not exist
        self.assertEqual(response.status_code, 404)


class DoctorCreateViewTests(DoctorModelTests):
    def test_create_doctor(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_create'), {
            'user': self.user1.id,
            'specialization': self.cardiologist.id,
            'experience_year': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DoctorModel.objects.filter(user=self.user1, specialization=self.cardiologist).exists())

    def test_create_doctor_requires_login(self):
        response = self.client.post(reverse('doctor:doctor_create'), {
            'user': self.user1.id,
            'specialization': self.cardiologist.id,
            'experience_year': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 302)


class DoctorUpdateViewTests(DoctorModelTests):
    def test_update_own_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_update', args=[self.doctor1.id]), {
            'specialization': self.cardiologist.id,
            'experience_year': 10,
            'visit_fee': 150
        })
        self.assertEqual(response.status_code, 200)
        self.doctor1.refresh_from_db()
        self.assertEqual(self.doctor1.experience_year, 10)
        self.assertEqual(self.doctor1.visit_fee, 150)

    def test_update_other_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_update', args=[self.doctor2.id]), {
            'specialization': self.cardiologist.id,
            'experience_year': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 403)


class DoctorDeleteViewTests(DoctorModelTests):
    def test_delete_own_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_delete', args=[self.doctor1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DoctorModel.objects.filter(id=self.doctor1.id).exists())

    def test_delete_other_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_delete', args=[self.doctor2.id]))
        self.assertEqual(response.status_code, 403)
