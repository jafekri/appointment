from django.urls import path
from reservation.views import ReservationView

app_name = 'reservation'

urlpatterns = [
    path('reservation/', ReservationView.as_view(), name='reservation'),
]
