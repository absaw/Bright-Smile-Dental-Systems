from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Patient
from appointments.models import Appointment,Visit, VisitProcedure
from schedules.models import TimeSlot

@ensure_csrf_cookie
def patient_list(request):
    return render(request, 'patients/patient_list.html')

def get_patients(request):
    patients = Patient.objects.all()
    data = []
    for patient in patients:
        last_visit = Visit.objects.filter(patient=patient).order_by('-time_slot__date', '-time_slot__start_time').first()
        next_appointment = Appointment.objects.filter(
            patient=patient, 
            time_slot__date__gte=timezone.now().date()
        ).order_by('time_slot__date', 'time_slot__start_time').first()
        
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'date_of_birth': patient.date_of_birth,
            'last_visit_date': last_visit.time_slot.date if last_visit else None,
            'last_visit_doctor': last_visit.doctor.name if last_visit else None,
            'last_visit_procedures': ', '.join([vp.procedure.name for vp in VisitProcedure.objects.filter(visit=last_visit)]) if last_visit else None,
            'next_appointment_date': next_appointment.time_slot.date if next_appointment else None,
            'next_appointment_doctor': next_appointment.doctor.name if next_appointment else None,
            'next_appointment_procedure': next_appointment.procedure.name if next_appointment else None,
        }
        data.append(patient_data)
    
    return JsonResponse(data, safe=False)