from django.urls import path, include
from .views import AddRatingView

app_name = 'rating'

urlpatterns = [
    path('rating/<int:pk>/', AddRatingView.as_view(), name='rating'),
]