from django.urls import path

from appointmenttime.views import appointment

app_name = 'reservation'

urlpatterns = [
    path('', appointment.as_view(), name='reservation'),
]