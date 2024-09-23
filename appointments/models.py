from django.db import models
from django.utils import timezone
class Visit(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit for {self.patient} on {self.date} at {self.time}"

class Appointment(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    # time_slot = models.ForeignKey('schedules.TimeSlot', on_delete=models.CASCADE)  # Keep this for now
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient} on {self.date} at {self.time}"

    def procedures(self):
        return ", ".join([ap.procedure.name for ap in self.appointmentprocedure_set.all()])
    
    class Meta:
        unique_together = ('doctor', 'date', 'time')
        
class VisitProcedure(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    procedure = models.ForeignKey('procedures.Procedure', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('visit', 'procedure')

class AppointmentProcedure(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    procedure = models.ForeignKey('procedures.Procedure', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'procedure')