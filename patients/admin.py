from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'date_of_birth', 'gender')
    list_filter = ('gender',)
    search_fields = ('name', 'phone_number')