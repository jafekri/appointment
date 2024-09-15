from django.db import models
from django.utils import timezone
from django.conf import settings
from user.models import DoctorProfile
# from reservation.models import Reservation


class Rating(models.Model):
    user = models.ForeignKey(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            )
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    # reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)   ########
    rate = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Rating {self.rate} by {self.user} for {self.doctor}'
