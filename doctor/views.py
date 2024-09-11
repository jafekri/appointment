from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin

from user.models import DoctorProfile


class DoctorListView(ListView):
    model = DoctorProfile
    template_name = "doctor/doctor_list.html"
    context_object_name = 'doctor_list'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DoctorDetailView(DetailView):
    model = DoctorProfile
    template_name = "doctor/doctor_detail.html"
    context_object_name = 'doctor'


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = DoctorProfile
    template_name = "doctor/doctor_create.html"
    fields = ['user', 'specialization', 'experience_year', 'visit_fee']


class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DoctorProfile
    template_name = "doctor/doctor_update.html"
    fields = ['user', 'specialization', 'experience_year', 'visit_fee']

    def test_func(self):
        return self.request.user == self.get_object().user


class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DoctorProfile
    template_name = "doctor/doctor_delete.html"
    success_url = reverse_lazy("doctor:doctor_list")
    context_object_name = 'doctor'

    def test_func(self):
        return self.request.user == self.get_object().user

