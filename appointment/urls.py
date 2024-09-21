"""
URL configuration for appointment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user.views import SignUpView, VerifyCodeView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # auth urls
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/register/', SignUpView.as_view(), name='signup'),
    path('auth/register/doctor/', SignUpView.as_view(), name='doctor_signup'),
    path('auth/verify/', VerifyCodeView.as_view(), name='verify_code'),

    path('user/', include('user.urls', namespace='user')),
    path('', include('doctor.urls', namespace='doctor')),
    path('appointment/', include('appointmenttime.urls', namespace='appointmenttime')),
    path('reservation/', include('reservation.urls', namespace='reservation')),
    path('rating/', include('rating.urls', namespace='rating')),
    path('comment/', include('comment.urls', namespace='comment')),
]
