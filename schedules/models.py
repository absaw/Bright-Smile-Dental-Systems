from django.db import models
from django.utils import timezone

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)

    def __str__(self):
        end_time = (timezone.datetime.combine(timezone.datetime.today(), self.start_time) + timezone.timedelta(hours=1)).time()
        return f"{self.date} {self.start_time}-{end_time} - {self.doctor} at {self.clinic}"

    class Meta:
        unique_together = ('date', 'start_time', 'doctor', 'clinic')
