from django.contrib import admin
from django.contrib.admin import register

from user.models import User, PatientUser


# Register your models here.
@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'otp_code', 'role')

    def role(self, obj):
        return obj.get_role()

    role.short_description = 'Role'
