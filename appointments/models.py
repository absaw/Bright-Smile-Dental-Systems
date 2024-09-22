from django.db import models

class Visit(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)
    time_slot = models.ForeignKey('schedules.TimeSlot', on_delete=models.CASCADE)
    doctor_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Visit for {self.patient} on {self.time_slot}"

class Appointment(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)
    time_slot = models.ForeignKey('schedules.TimeSlot', on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient} on {self.time_slot}"

    def procedures(self):
        return ", ".join([ap.procedure.name for ap in self.appointmentprocedure_set.all()])

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