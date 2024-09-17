from django.contrib import admin

from user.models import PatientUser, User, PatientProfile, Specialization, DoctorUser, DoctorProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


# Inline for Doctor Profile
class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile
    can_delete = False
    verbose_name_plural = 'Doctor Profile'
    fk_name = 'user'

@admin.register(DoctorUser)
class DoctorUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'balance', 'extra')  # Add more fields as needed
    search_fields = ('username', 'first_name', 'last_name', 'phone')
    list_filter = ('doctorprofile__specialization', 'doctorprofile__experience')
    inlines = [DoctorProfileInline]
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(PatientUser)
class PatientUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'balance', 'extra')
    search_fields = ('username', 'first_name', 'last_name', 'phone')

    def has_add_permission(self, request, obj=None):
        return False



# Inline for Patient Profile
# class PatientProfileInline(admin.StackedInline):
#     model = PatientProfile
#     can_delete = False
#     verbose_name_plural = 'Patient Profile'
#     fk_name = 'user'

# Extend the User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (DoctorProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_select_related = ('doctorprofile', 'patientprofile')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_role(self, obj):
        if hasattr(obj, 'doctorprofile'):
            return 'Doctor'
        elif hasattr(obj, 'patientprofile'):
            return 'Patient'
        else:
            return 'Admin'
    get_role.short_description = 'Role'

# Unregister the original User admin.
admin.site.unregister(User)

admin.site.register(User, UserAdmin)