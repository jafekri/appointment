from django.urls import path

from .views import DoctorListView, DoctorDetailView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView

app_name = "doctor"
urlpatterns = [
    path('', DoctorListView.as_view(), name='doctor_list'),
    path('<int:pk>/detail/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('create/', DoctorCreateView.as_view(), name='doctor_create'),
    path('<int:pk>/update/', DoctorUpdateView.as_view(), name='doctor_update'),
    path('<int:pk>/delete/', DoctorDeleteView.as_view(), name='doctor_delete'),
]