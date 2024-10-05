from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

from user.views import SignUpView, VerifyCodeView
from user.forms import AuthenticationForm


urlpatterns = [
    path("admin/", admin.site.urls),
    
    # auth urls
    path("auth/login/", LoginView.as_view(form_class=AuthenticationForm), name="login"),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/register/", SignUpView.as_view(), name="signup"),
    path("auth/register/doctor/", SignUpView.as_view(), name="doctor_signup"),
    path("auth/verify/", VerifyCodeView.as_view(), name="verify_code"),
    
    # local apps
    path("user/", include("user.urls", namespace="user")),
    path("", include("reservation.urls", namespace="reservation")),
    path("rating/", include("rating.urls", namespace="rating")),
    path("comment/", include("comment.urls", namespace="comment")),
]
