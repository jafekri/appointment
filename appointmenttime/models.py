from django.db import models

from user.models import DoctorProfile


# Create your models here.
class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, related_name='appointments', on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)