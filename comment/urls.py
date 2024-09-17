from django.urls import path, include
from .views import DoctorCommentView

app_name = 'comment'

urlpatterns = [
    path('comment/<int:pk>/', DoctorCommentView.as_view(), name='doctor_comment'),
]