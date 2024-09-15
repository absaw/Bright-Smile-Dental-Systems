from django.db import models

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time}"

class DoctorSchedule(models.Model):
    doctor_clinic_affiliation = models.ForeignKey('doctors.DoctorClinicAffiliation', on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')

    class Meta:
        unique_together = ('doctor_clinic_affiliation', 'time_slot')