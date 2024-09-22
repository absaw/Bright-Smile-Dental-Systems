from django.contrib import admin
from .models import Visit, Appointment, VisitProcedure, AppointmentProcedure

class VisitProcedureInline(admin.TabularInline):
    model = VisitProcedure
    extra = 1

class AppointmentProcedureInline(admin.TabularInline):
    model = AppointmentProcedure
    extra = 1

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'time_slot')
    list_filter = ('doctor', 'clinic')
    inlines = [VisitProcedureInline]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'time_slot', 'procedures')
    list_filter = ('doctor', 'clinic')
    inlines = [AppointmentProcedureInline]

    def procedures(self, obj):
        return obj.procedures()