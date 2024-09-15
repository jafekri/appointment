from appointment import settings
from django.db import models
from django.urls import reverse
from user.models import DoctorUser
# from reservation.models import Reservation



# Create your models here.
class Comment(models.Model):
    # reservation = models.ForeignKey(
    #     Reservation,
    #     on_delete=models.CASCADE,
    # )
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_comments',
    )
    doctor = models.ForeignKey(
        DoctorUser,
        on_delete=models.CASCADE,
        related_name='doctor_comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return reverse("comment_list")
