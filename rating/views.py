from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Rating
from .forms import RatingForm
from django.conf import settings
from user.models import DoctorProfile
# from reservation.models import Reservation


class AddRatingView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = 'rating/rating.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])

        # try:
        #     form.instance.reservation = Reservation.objects.get(user=self.request.user, doctor=form.instance.doctor)
        # except Reservation.DoesNotExist:
        #     form.add_error(None, "You must have a reservation with this doctor to rate them.")
        #     return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return doctor.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        context['doctor'] = doctor
        context['ratings'] = Rating.objects.filter(doctor=doctor)
        return context



