from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

    def doctor_count(self):
        return self.doctorclinicaffiliation_set.count()
    
    def patient_count(self):
        return self.patientclinicaffiliation_set.count()

class PatientClinicAffiliation(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('patient', 'clinic')

class ClinicProcedure(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    procedure = models.ForeignKey('procedures.Procedure', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('clinic', 'procedure')