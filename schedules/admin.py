from django.contrib import admin
from .models import TimeSlot, DoctorSchedule

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time')
    list_filter = ('date',)
    search_fields = ('date',)

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor_clinic_affiliation', 'time_slot', 'status')
    list_filter = ('status', 'doctor_clinic_affiliation__doctor', 'doctor_clinic_affiliation__clinic')
    search_fields = ('doctor_clinic_affiliation__doctor__name', 'doctor_clinic_affiliation__clinic__name')