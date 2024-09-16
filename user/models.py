from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
# from django.utils.text import slugify
from django.shortcuts import reverse


class User(AbstractUser):
    """
       username , password , first_name and last_name
       inherited from AbstractUser
    """
    # first_name = models.CharField(max_length=150, blank=True, null=True)
    # last_name = models.CharField(max_length=150, blank=True, null=True)
    balance = models.BigIntegerField(default=0)
    otp_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(regex=r"^09[0-9]{9}$",
                           message="Phone number is not correct!")
        ]
    )

    """
        To avoid interference with auth.User.groups
    """
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions',
        blank=True,
    )

    def get_role(self):
        if hasattr(self, "doctorprofile") and self.doctorprofile:
            return "doctor"
        elif hasattr(self, "patientprofile") and self.patientprofile:
            return "patient"
        else:
            return "admin"

    def __str__(self):
        return self.username


class Specialization(models.Model):
    name = models.CharField("Specialization Name",
                            max_length=100)
    slug = models.SlugField("Slug",
                            blank=True)

    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.name)
    #         # Check if the slug already exists
    #         counter = 1
    #         original_slug = self.slug
    #         while Specialization.objects.filter(slug=self.slug).exists():
    #             self.slug = f"{original_slug}-{counter}"
    #             counter += 1
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
    )
    specialization = models.ForeignKey(Specialization,
                                         on_delete=models.CASCADE,
                                         verbose_name="Specialization", null=True, blank=True)
    experience = models.PositiveIntegerField("Years of Experience", default=5)
    visit_fee = models.PositiveBigIntegerField("Consultation Fee", default=0)

    def get_absolute_url(self):
        return reverse("doctor:doctor_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Doctor Profile of {self.user.username}"


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="User",
    )

    def __str__(self):
        return f"Patient Profile of {self.user.username}"


class DoctorUser(User):
    class Meta:
        proxy = True

    class DoctorManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(doctorprofile__isnull=False)

    objects = DoctorManager()

    @property
    def extra(self):
        return self.doctorprofile


class PatientUser(User):
    class Meta:
        proxy = True

    class PatientManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(patientprofile__isnull=False)

    objects = PatientManager()

    @property
    def extra(self):
        return self.patientprofile
