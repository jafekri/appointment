from django.urls import path
from .views import (SignUpView, VerifyCodeView,
                    ProfileView, ProfileUpdateView,
                    TemplateView)


app_name = 'user'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
]
