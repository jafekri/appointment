from django.urls import path

from doctor.views import DoctorListView

app_name = "doctor"
urlpatterns = [
    path('list/', DoctorListView.as_view(), name='doctor_list')
]