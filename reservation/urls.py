from django.urls import path
from reservation.views import (
    ReservationCreateView,
    DoctorListView,
    DoctorDetailView,
    DoctorCreateView,
    DoctorUpdateView,
    DoctorDeleteView,
)

app_name = "reservation"

urlpatterns = [
    path("<int:pk>/", ReservationCreateView.as_view(), name="make_reservation"),
    
    path("", DoctorListView.as_view(), name="doctor_list"),
    path("<int:pk>/detail/", DoctorDetailView.as_view(), name="doctor_detail"),
    path("create/", DoctorCreateView.as_view(), name="doctor_create"),
    path("<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor_update"),
    path("<int:pk>/delete/", DoctorDeleteView.as_view(), name="doctor_delete"),
]
