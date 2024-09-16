from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from rating.forms import RatingForm
from user.models import DoctorProfile


class DoctorListView(ListView):
    model = DoctorProfile
    template_name = "doctor/doctor_list.html"
    context_object_name = 'doctor_list'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Fetch the query parameter from the search form
        query = self.request.GET.get('q', None)

        # Filter by doctor's name (first or last name) or specialization if the query is present
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(specialization__name__icontains=query)
            )
        return queryset

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DoctorDetailView(DetailView):
    model = DoctorProfile
    template_name = "doctor/doctor_detail.html"
    context_object_name = 'doctor'
    login_url = reverse_lazy('user:login')
    form_class = RatingForm


    def get_context_data(self, **kwargs):
        doctor = self.object
        context = super().get_context_data(**kwargs)
        context['appointments'] =doctor.appointments.all()
        context['rating_form'] = self.form_class()
        context['average_rating'] = doctor.average_rating()
        return context

class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = DoctorProfile
    template_name = "doctor/doctor_create.html"
    fields = ['user', 'specialization', 'experience', 'visit_fee']
    success_url = reverse_lazy('doctor:doctor_detail')
    login_url = reverse_lazy('user:login')


class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DoctorProfile
    template_name = "doctor/doctor_update.html"
    fields = ['user', 'specialization', 'experience', 'visit_fee']
    login_url = reverse_lazy('user:login')

    def test_func(self):
        return self.request.user == self.get_object().user


class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DoctorProfile
    template_name = "doctor/doctor_delete.html"
    success_url = reverse_lazy("doctor:doctor_list")
    context_object_name = 'doctor'
    login_url = reverse_lazy('user:login')

    def test_func(self):
        return self.request.user == self.get_object().user

