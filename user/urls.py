from django.urls import path
from .views import SignUpView, CustomLoginView, LogoutView, VerifyCodeView

app_name = 'user'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
