from django.db import models
from user.models import Specialization
from django.conf import settings
from django.shortcuts import reverse


# class DoctorModel(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
#     experience = models.PositiveIntegerField()
#     visit_fee = models.PositiveIntegerField()
#     average_rating = models.DecimalField(max_digits=3,
#                                          decimal_places=2,
#                                          default=0)
#
#     def get_absolute_url(self):
#         return reverse("doctor:doctor_detail", kwargs={"pk": self.pk})

