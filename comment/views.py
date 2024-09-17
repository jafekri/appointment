from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.contrib import messages

from comment.forms import CommentForm
from user.models import DoctorProfile


class DoctorCommentView(FormView):
    template_name = "doctor/doctor_detail.html"
    form_class = CommentForm

    # def get_success_url(self):
    #     doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
    #     return reverse('doctor:doctor_detail', kwargs={'pk': doctor.id})
        # return doctor.get_absolute_url()
    # def get_success_url(self):
    #     doctor_pk = self.kwargs['pk']
    #     print("ssss"*50)
    #     print(doctor_pk)
    #     return reverse_lazy('doctor:doctor_detail', kwargs={'pk': doctor_pk})

    def form_valid(self, form):
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.doctor = doctor
        comment.author = self.request.user
        comment.save()

        messages.success(self.request, "Your comment has been posted successfully!")
        doctor = DoctorProfile.objects.get(pk=self.kwargs['pk'])
        return reverse('doctor:doctor_detail', kwargs={'pk': doctor.id})
        # return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("Doctor PK:", self.kwargs.get('pk'))
        context['form'] = self.get_form()
        return context
