from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import DoctorModel
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class DoctorListView(LoginRequiredMixin, ListView):
    model = DoctorModel
    template_name = "doctor_app/doctor_list.html"
    context_object_name = 'doctor_list'


class DoctorDetailView(LoginRequiredMixin, DetailView):
    model = DoctorModel
    template_name = "doctor_app/doctor_detail.html"
    context_object_name = 'doctor'


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = DoctorModel
    template_name = "doctor_app/doctor_create.html"
    fields = ['user', 'specialization', 'experience_year', 'visit_fee']


class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = DoctorModel
    template_name = "doctor_app/doctor_update.html"
    fields = ['user', 'specialization', 'experience_year', 'visit_fee']


class DoctorDeleteView(LoginRequiredMixin, DeleteView):
    model = DoctorModel
    template_name = "doctor_app/doctor_delete.html"
    success_url = reverse_lazy("doctor:doctor_list")
    context_object_name = 'doctor'

