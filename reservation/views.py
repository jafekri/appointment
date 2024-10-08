from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from .models import Appointment
from user.models import PatientProfile, DoctorProfile
from .models import Reservation
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin


from comment.forms import CommentForm
from django.db.models import Q
from rating.forms import RatingForm
from comment.forms import CommentForm

from user.models import DoctorProfile


class ReservationCreateView(LoginRequiredMixin, CreateView):
    model = Reservation
    template_name = "reservation/reservation_create.html"
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = get_object_or_404(Appointment, id=self.kwargs["pk"])
        context["appointment"] = appointment
        context["doctor"] = appointment.doctor
        return context

    def form_valid(self, form):
        appointment = get_object_or_404(Appointment, id=self.kwargs["pk"])
        doctor = appointment.doctor
        doctor_profile = DoctorProfile.objects.get(pk=doctor.id)
        if appointment.status is False:

            messages.warning(
                self.request, "This appointment is no longer available.", "error"
            )
            return redirect("doctor:doctor_detail", doctor_profile.id)

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

        subject = "Reservation Confirmation"
        message = f"Dear {user.first_name},\n\nYour appointment with Dr. {doctor_profile.user.first_name} : {doctor_profile.user.last_name} has been successfully reserved.\n\nVisit Fee: {visit_fee}\nAppointment Time: {appointment.date} At {appointment.start_time}-{appointment.end_time} \n\nThank you!"
        recipient_list = [user.username]

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
        # Success message
        messages.success(self.request, "Payment successful.")
        return redirect("doctor:doctor_detail", doctor_profile.id)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    template_name = "reservation/details.html"
    context_object_name = "reservation"


class DoctorListView(ListView):
    model = DoctorProfile
    template_name = "doctor/doctor_list.html"
    context_object_name = "doctor_list"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Fetch the query parameter from the search form
        query = self.request.GET.get("q", None)

        # Filter by doctor's name (first or last name) or specialization if the query is present
        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
                | Q(specialization__name__icontains=query)
            )
        return queryset

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DoctorDetailView(DetailView):
    model = DoctorProfile
    template_name = "doctor/doctor_detail.html"
    context_object_name = "doctor"
    login_url = reverse_lazy("user:login")
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        doctor = self.object
        context = super().get_context_data(**kwargs)
        context["appointments"] = doctor.appointments.all()
        context["rating_form"] = self.form_class()
        context["average_rating"] = doctor.average_rating()
        context["comments"] = self.object.comments.filter(activate=True)
        context["form"] = CommentForm()
        return context

    form_class = RatingForm


class DoctorCreateView(LoginRequiredMixin, CreateView):
    model = DoctorProfile
    template_name = "doctor/doctor_create.html"
    fields = ["user", "specialization", "experience", "visit_fee"]
    success_url = reverse_lazy("doctor:doctor_detail")
    login_url = reverse_lazy("user:login")


class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DoctorProfile
    template_name = "doctor/doctor_update.html"
    fields = ["user", "specialization", "experience", "visit_fee"]
    login_url = reverse_lazy("user:login")

    def test_func(self):
        return self.request.user == self.get_object().user


class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DoctorProfile
    template_name = "doctor/doctor_delete.html"
    success_url = reverse_lazy("doctor:doctor_list")
    context_object_name = "doctor"
    login_url = reverse_lazy("user:login")

    def test_func(self):
        return self.request.user == self.get_object().user
