from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect

from appointmenttime.models import Appointment
from .models import Reservation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = 'reservation/reservation_create.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = get_object_or_404(Appointment, id=self.kwargs['pk'])
        context['appointment'] = appointment
        context['doctor'] = appointment.doctor

        return context

    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, id=self.kwargs['appointment_id'])
        if appointment.status is False:
            messages.error(self.request, "This appointment is no longer available.")
            return redirect('appointment_list')

        doctor = appointment.doctor
        visit_fee = doctor.visit_fee

        form.instance.user = self.request.user
        form.instance.doctor = doctor
        form.instance.appointment = appointment
        form.instance.visit_fee = visit_fee

class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservation/details.html'
    context_object_name = 'reservation'