from django.db import models
from user.models import *
from datetime import date
from django.utils import timezone

# Create your models here.
class AppointmentTime(models.Model):
    class Status(models.TextChoices):
        EMPTY = '0', 'EMPTY'
        COMPLETION = '1', 'COMPLETION'

    doctor_id = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='doctor_reservations')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    appointment_date = models.DateField(default=date.today)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.EMPTY)


class Reservation(models.Model):
    class PaymentStatus(models.TextChoices):
        DONE = 'DN', 'DONE'
        PENDENT = 'PD', 'PENDENT'
        CANCELED = 'CN', 'CANCELED'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reservations')
    doctor_id = models.ForeignKey(DoctorUser, on_delete=models.CASCADE, related_name='doctor_reservations')
    appointment_id = models.OneToOneField(AppointmentTime, on_delete=models.CASCADE)
    visit_fee = models.PositiveIntegerField(default=0)
    payment_status = models.CharField(max_length=2, choices=PaymentStatus.choices, default=PaymentStatus.PENDENT)

