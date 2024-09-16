from django.contrib import admin
from django.contrib.admin import register

from reservation.models import Reservation


# Register your models here.

@register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('patient_username', 'doctor_first_name', 'appointment_date', 'visit_fee', 'payment_status')

    def has_add_permission(self, request, obj=None):
        return False

    def patient_username(self, obj):
        return obj.patient.user.username
    patient_username.admin_order_field = 'patient__user__username'
    patient_username.short_description = 'Patient Username'

    def doctor_first_name(self, obj):
        return obj.doctor.user.first_name
    doctor_first_name.admin_order_field = 'doctor__user__first_name'
    doctor_first_name.short_description = 'Doctor First Name'

    def appointment_date(self, obj):
        return obj.appointment.date
    appointment_date.admin_order_field = 'appointment__date'
    appointment_date.short_description = 'Appointment Date'
