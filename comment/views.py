from django.shortcuts import render, get_object_or_404
from django.template.defaulttags import comment
from django.views.decorators.http import require_POST
from user.models import DoctorProfile
from .forms import CommentForm



# Create your views here.
@require_POST
def doctor_comment(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.doctor = doctor
        comment.save()
    context = {
        'doctor': doctor,
        'form': form,
        'comment': comment,
    }
    return render(request, "comment/comment.html", context)

