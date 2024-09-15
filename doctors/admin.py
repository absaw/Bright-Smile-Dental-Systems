from django.contrib import admin
from .models import Doctor, DoctorClinicAffiliation, PatientDoctorAffiliation, DoctorProcedure

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'npi', 'email', 'phone_number')
    search_fields = ('name', 'npi', 'email')

@admin.register(DoctorClinicAffiliation)
class DoctorClinicAffiliationAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'clinic', 'office_address')
    list_filter = ('clinic',)
    search_fields = ('doctor__name', 'clinic__name')

@admin.register(PatientDoctorAffiliation)
class PatientDoctorAffiliationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor')
    list_filter = ('doctor',)
    search_fields = ('patient__name', 'doctor__name')

@admin.register(DoctorProcedure)
class DoctorProcedureAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'procedure')
    list_filter = ('doctor', 'procedure')
    search_fields = ('doctor__name', 'procedure__name')