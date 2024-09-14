from django.urls import path
from .views import (SignUpView, CustomLoginView,
                    LogoutView, VerifyCodeView,
                    ProfileView, ProfileUpdateView,
                    CustomPasswordChangeView, TemplateView)


app_name = 'user'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', TemplateView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
