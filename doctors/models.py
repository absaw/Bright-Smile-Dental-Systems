from django.db import models

class Doctor(models.Model):
    npi = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    # schedule = models.TextField(blank=True)
    def __str__(self):
        return self.name

class DoctorClinicAffiliation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey('clinics.Clinic', on_delete=models.CASCADE)
    office_address = models.TextField()
    working_schedule = models.TextField(blank=True)
    class Meta:
        unique_together = ('doctor', 'clinic')

class PatientDoctorAffiliation(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patient', 'doctor')

class DoctorProcedure(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    procedure = models.ForeignKey('procedures.Procedure', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('doctor', 'procedure')