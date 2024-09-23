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
    list_display = ('patient', 'doctor', 'clinic', 'date', 'time')
    list_filter = ('doctor', 'clinic', 'date')
    search_fields = ('patient__name', 'doctor__name', 'clinic__name')
    date_hierarchy = 'date'
    inlines = [VisitProcedureInline]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'clinic', 'date', 'time', 'procedures', 'date_booked')
    list_filter = ('doctor', 'clinic', 'date')
    search_fields = ('patient__name', 'doctor__name', 'clinic__name')
    date_hierarchy = 'date'
    inlines = [AppointmentProcedureInline]

    def procedures(self, obj):
        return obj.procedures()