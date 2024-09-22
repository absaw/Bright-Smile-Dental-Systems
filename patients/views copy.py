from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
#Model Import
from .models import Patient
from schedules.models import TimeSlot
from appointments.models import Appointment, Visit, VisitProcedure, AppointmentProcedure
from doctors.models import Doctor
from clinics.models import Clinic
from procedures.models import Procedure
@login_required
@ensure_csrf_cookie
def patient_list(request):
    return render(request, 'patients/patient_list.html')

@login_required
@ensure_csrf_cookie
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'patients/patient_detail.html', {'patient': patient})

@login_required
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

@login_required
def get_patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = Visit.objects.filter(patient=patient).order_by('-time_slot__date', '-time_slot__start_time')
    
    visit_data = []
    for visit in visits:
        procedures = VisitProcedure.objects.filter(visit=visit)
        visit_data.append({
            'date_time': f"{visit.time_slot.date} {visit.time_slot.start_time}",
            'doctor_name': visit.doctor.name,
            'clinic_name': visit.clinic.name,
            'procedures': ', '.join([vp.procedure.name for vp in procedures]),
            'doctor_notes': visit.doctor_notes
        })

    data = {
        'id': patient.id,
        'name': patient.name,
        'address': patient.address,
        'phone_number': patient.phone_number,
        'date_of_birth': patient.date_of_birth,
        'ssn_last_4': patient.ssn_last_4,
        'gender': patient.gender,
        'visits': visit_data
    }
    
    return JsonResponse(data)

@login_required
def update_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        patient.name = request.POST.get('name')
        patient.address = request.POST.get('address')
        patient.phone_number = request.POST.get('phone_number')
        patient.date_of_birth = request.POST.get('date_of_birth')
        patient.ssn_last_4 = request.POST.get('ssn_last_4')
        patient.gender = request.POST.get('gender')
        patient.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)