from django.test import TestCase
from django.contrib.auth import get_user_model
from user.models import DoctorProfile
from .models import Comment

class CommentModelTest(TestCase):

    def setUp(self):
        # Set up a user and a doctor profile for foreign key relations
        self.user = get_user_model().objects.create_user(username='testuser', password='password123')
        self.doctor = DoctorProfile.objects.create(name='Dr. Smith')

    def test_comment_creation(self):
        # Create a comment
        comment = Comment.objects.create(
            doctor=self.doctor,
            author=self.user,
            body='This is a test comment.'
        )
        self.assertEqual(comment.body, 'This is a test comment.')
        self.assertFalse(comment.activate)  # Default should be False

    def test_foreign_key_relations(self):
        # Create a comment and check relations
        comment = Comment.objects.create(
            doctor=self.doctor,
            author=self.user,
            body='Another test comment.'
        )
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.doctor, self.doctor)

    def test_comment_string_representation(self):
        # Test the __str__ method of the Comment model
        comment = Comment.objects.create(
            doctor=self.doctor,
            author=self.user,
            body='A string representation test.'
        )
        self.assertEqual(str(comment), f'{self.user}: {self.doctor}')
