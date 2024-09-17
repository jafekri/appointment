from django.urls import path

from reservation.views import ReservationCreateView

app_name = 'reservation'

urlpatterns = [
    path('<int:pk>/', ReservationCreateView.as_view(), name='make_reservation'),
]