from django.contrib import admin
from .models import Clinic, PatientClinicAffiliation, ClinicProcedure

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'phone_number', 'email')
    search_fields = ('name', 'city', 'state')

@admin.register(PatientClinicAffiliation)
class PatientClinicAffiliationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'clinic')
    list_filter = ('clinic',)
    search_fields = ('patient__name', 'clinic__name')

@admin.register(ClinicProcedure)
class ClinicProcedureAdmin(admin.ModelAdmin):
    list_display = ('clinic', 'procedure')
    list_filter = ('clinic', 'procedure')
    search_fields = ('clinic__name', 'procedure__name')