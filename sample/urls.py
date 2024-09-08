from django.urls import path, include

from sample.views import TestView

app_name = 'sample'
urlpatterns = [
    path('sample/', TestView.as_view(), name='test')
]