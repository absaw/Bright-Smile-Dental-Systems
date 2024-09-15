from django.contrib import admin
from .models import Procedure

@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes')
    search_fields = ('name',)