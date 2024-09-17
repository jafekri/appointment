from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from comment.forms import CommentForm
from rating.forms import RatingForm
from user.models import DoctorProfile

class DoctorCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm
    template_name = "doctor/doctor_detail.html"  # You can use the same template or create a separate one
    def get_success_url(self):
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return doctor.get_absolute_url()

    def form_valid(self, form):
        doctor = get_object_or_404(DoctorProfile, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.doctor = doctor
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctor'] = get_object_or_404(DoctorProfile, pk=self.kwargs['pk'])
        context['appointments'] = context['doctor'].appointments.all()
        context['rating_form'] = RatingForm()
        context['average_rating'] = context['doctor'].average_rating()
        context['comments'] = context['doctor'].comments.filter(activate=True)
        return context
