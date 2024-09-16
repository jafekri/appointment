from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from appointmenttime.models import Appointment
from user.models import PatientProfile, DoctorProfile
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
        appointment = get_object_or_404(Appointment, id=self.kwargs['pk'])
        doctor = appointment.doctor
        doctor_profile = DoctorProfile.objects.get(pk=doctor.id)
        if appointment.status is False:

            messages.warning(self.request, "This appointment is no longer available.", 'error')
            return redirect('doctor:doctor_detail', doctor_profile.id)

        user = self.request.user
        visit_fee = doctor.visit_fee

        # Fetch or create PatientProfile instance
        patient_profile, created = PatientProfile.objects.get_or_create(user=user)

        # Check if the user has enough balance
        # if user.balance < visit_fee:
        #     messages.error(self.request, "Insufficient balance.")
        #     return redirect('doctor:doctor_detail', appointment.doctor.user.id)

        # Update user's balance
        if patient_profile.user.balance > visit_fee:
            patient_profile.user.balance -= visit_fee
            patient_profile.user.save()

        # Update doctor's balance
        doctor_profile.user.balance += visit_fee
        doctor_profile.user.save()

        # Update appointment status
        appointment.status = False
        appointment.save()

        # Create and save Reservation
        reservation = form.save(commit=False)
        reservation.patient = patient_profile
        reservation.doctor = doctor_profile
        reservation.appointment = appointment
        reservation.visit_fee = visit_fee
        reservation.payment_status = True
        reservation.save()

        # Success message
        messages.success(self.request, "Payment successful.")
        return redirect('doctor:doctor_detail', doctor_profile.id)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = 'reservation/details.html'
    context_object_name = 'reservation'