from django.contrib import admin
from user.models import DoctorProfile
from .models import Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class DoctorProfileAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

admin.site.register(DoctorProfile, DoctorProfileAdmin)
admin.site.register(Comment)
