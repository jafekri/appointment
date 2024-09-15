from django.db import models

# Create your models here.
from django.db import models
from appointmenttime.models import Appointment
from user.models import DoctorProfile, PatientProfile


class Reservation(models.Model):
    patient = models.ForeignKey(PatientProfile, related_name="reservations", on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, related_name="reservations", on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, related_name="reservation", on_delete=models.CASCADE)
    visit_fee = models.PositiveBigIntegerField()
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation by {self.patient.user.username} for {self.doctor.user.first_name} on {self.appointment.date}"
