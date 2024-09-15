from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from user.models import DoctorProfile, Specialization

User = get_user_model()


class DoctorProfileTests(TestCase):
    def setUp(self):
        # Set up specializations
        self.cardiologist = Specialization.objects.create(name='Cardiologist')
        self.dermatologist = Specialization.objects.create(name='Dermatologist')

        # Create two users (doctors)
        self.user1 = User.objects.create_user(username='doctor1', password='pass', phone='1234567890')
        self.user2 = User.objects.create_user(username='doctor2', password='pass', phone='0987654321')

        # Create doctor profiles using the Specialization instances
        self.doctor_profile1 = DoctorProfile.objects.create(
            user=self.user1,
            specialization=self.cardiologist,
            experience=10,
            visit_fee=150
        )
        self.doctor_profile2 = DoctorProfile.objects.create(
            user=self.user2,
            specialization=self.dermatologist,
            experience=5,
            visit_fee=100
        )


class DoctorListViewTests(DoctorProfileTests):
    def test_doctor_list_view(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'doctor/doctor_list.html')
        self.assertContains(response, self.doctor_profile1.specialization.name)
        self.assertContains(response, self.doctor_profile2.specialization.name)


class DoctorDetailViewTests(DoctorProfileTests):
    def test_doctor_detail_view(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[self.doctor_profile1.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.doctor_profile1.specialization.name)

    def test_doctor_detail_view_not_accessible_by_other_user(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[self.doctor_profile2.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_doctor_detail_view_invalid_id(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.get(reverse('doctor:doctor_detail', args=[999]))  # ID does not exist
        self.assertEqual(response.status_code, 404)


class DoctorCreateViewTests(DoctorProfileTests):
    def test_create_doctor(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_create'), {
            'user': self.user1.id,
            'specialization': self.cardiologist.id,
            'experience': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(DoctorProfile.objects.filter(user=self.user1, specialization=self.cardiologist).exists())

    def test_create_doctor_requires_login(self):
        response = self.client.post(reverse('doctor:doctor_create'), {
            'user': self.user1.id,
            'specialization': self.cardiologist.id,
            'experience': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('user:login')}?next={reverse('doctor:doctor_create')}")


class DoctorUpdateViewTests(DoctorProfileTests):
    def test_update_own_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_update', args=[self.doctor_profile1.user.id]), {
            'specialization': self.cardiologist.id,
            'experience': 10,
            'visit_fee': 150
        })
        self.assertEqual(response.status_code, 200)
        self.doctor_profile1.refresh_from_db()
        self.assertEqual(self.doctor_profile1.experience, 10)
        self.assertEqual(self.doctor_profile1.visit_fee, 150)

    def test_update_other_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_update', args=[self.doctor_profile2.user.id]), {
            'specialization': self.cardiologist.id,
            'experience': 8,
            'visit_fee': 120
        })
        self.assertEqual(response.status_code, 403)


class DoctorDeleteViewTests(DoctorProfileTests):
    def test_delete_own_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_delete', args=[self.doctor_profile1.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(DoctorProfile.objects.filter(user=self.doctor_profile1.user).exists())

    def test_delete_other_doctor_profile(self):
        self.client.login(username='doctor1', password='pass')
        response = self.client.post(reverse('doctor:doctor_delete', args=[self.doctor_profile2.user.id]))
        self.assertEqual(response.status_code, 403)
