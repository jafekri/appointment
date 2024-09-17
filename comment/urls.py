from django.urls import path, include
from .views import doctor_comment

app_name = 'comment'

urlpatterns = [
    path('<doctor_id>/detail/commnet', doctor_comment, name='doctor_comment'),
]