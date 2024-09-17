from django.contrib import admin
from django.contrib.admin import register

from appointmenttime.models import Appointment

@register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'status', ]
    filter_list = ['doctor', 'status']
    list_editable = ['status']



