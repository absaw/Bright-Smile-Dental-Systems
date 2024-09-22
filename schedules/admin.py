from django.contrib import admin
from .models import TimeSlot, DoctorSchedule

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time_display')
    list_filter = ('date',)
    search_fields = ('date', 'start_time')

    def end_time_display(self, obj):
        return obj.__str__().split('-')[1]
    end_time_display.short_description = 'End Time'

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'clinic_name', 'time_slot', 'status')
    list_filter = ('status', 'doctor_clinic_affiliation__doctor', 'doctor_clinic_affiliation__clinic')
    search_fields = ('doctor_clinic_affiliation__doctor__name', 'doctor_clinic_affiliation__clinic__name', 'time_slot__date')

    def doctor_name(self, obj):
        return obj.doctor_clinic_affiliation.doctor.name
    doctor_name.short_description = 'Doctor'

    def clinic_name(self, obj):
        return obj.doctor_clinic_affiliation.clinic.name
    clinic_name.short_description = 'Clinic'