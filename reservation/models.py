from django.db import models
from user.models import DoctorProfile, PatientProfile


class Appointment(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, related_name="appointments", on_delete=models.CASCADE
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reservation(models.Model):
    patient = models.ForeignKey(
        PatientProfile, related_name="reservations", on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        DoctorProfile, related_name="reservations", on_delete=models.CASCADE
    )
    appointment = models.OneToOneField(
        Appointment, related_name="reservation", on_delete=models.CASCADE
    )
    visit_fee = models.PositiveBigIntegerField()
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reservation by {self.patient.user.username} for {self.doctor.user.first_name} on {self.appointment.date}"
