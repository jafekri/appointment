from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from doctor.views import  DoctorDetailView
from .forms import CommentForm
from .models import Comment


# Create your views here.
class CommentView(DoctorDetailView, LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        return view(request, *args, **kwargs)

class CommentGet(DetailView):
    model = Comment
    template_name = "comment/comment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context

class CommentPost(SingleObjectMixin, FormView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/comment.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.doctor = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        doctor = self.get_object()
        return reverse("doctor_detail", kwargs={"pk": doctor.pk})
