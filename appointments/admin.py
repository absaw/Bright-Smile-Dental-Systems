from django.contrib import admin
from .models import Visit, Appointment, VisitProcedure

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'time_slot')
    list_filter = ('clinic', 'doctor')
    search_fields = ('patient__name', 'doctor__name', 'clinic__name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'procedure', 'time_slot', 'date_booked')
    list_filter = ('clinic', 'doctor', 'procedure')
    search_fields = ('patient__name', 'doctor__name', 'clinic__name')

@admin.register(VisitProcedure)
class VisitProcedureAdmin(admin.ModelAdmin):
    list_display = ('visit', 'procedure')
    list_filter = ('procedure',)
    search_fields = ('visit__patient__name', 'procedure__name')