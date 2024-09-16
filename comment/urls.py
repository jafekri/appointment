from django.urls import path, include
from .views import CommentView

app_name = 'rating'

urlpatterns = [
    path('comment/<int:pk>/', CommentView.as_view(), name='comment'),
]