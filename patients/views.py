from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Patient
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
        last_visit = Visit.objects.filter(patient=patient).order_by('-date', '-time').first()
        next_appointment = Appointment.objects.filter(
            patient=patient, 
            date__gte=timezone.now().date()
        ).order_by('date', 'time').first()
        
        patient_data = {
            'id': patient.id,
            'name': patient.name,
            'date_of_birth': patient.date_of_birth,
            'last_visit_date': last_visit.date if last_visit else None,
            'last_visit_doctor': last_visit.doctor.name if last_visit else None,
            'last_visit_procedures': ', '.join([vp.procedure.name for vp in VisitProcedure.objects.filter(visit=last_visit)]) if last_visit else None,
            'next_appointment_date': next_appointment.date if next_appointment else None,
            'next_appointment_doctor': next_appointment.doctor.name if next_appointment else None,
            'next_appointment_procedure': ', '.join([ap.procedure.name for ap in AppointmentProcedure.objects.filter(appointment=next_appointment)]) if next_appointment else None,
        }
        data.append(patient_data)
    
    return JsonResponse(data, safe=False)

@login_required
def get_patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    visits = Visit.objects.filter(patient=patient).order_by('-date', '-time')
    
    visit_data = []
    for visit in visits:
        procedures = VisitProcedure.objects.filter(visit=visit)
        visit_data.append({
            'date_time': f"{visit.date} {visit.time}",
            'doctor_name': visit.doctor.name,
            'clinic_name': visit.clinic.name,
            'procedures': ', '.join([vp.procedure.name for vp in procedures]),
            'doctor_notes': visit.doctor_notes
        })

    next_appointment = Appointment.objects.filter(
        patient=patient,
        date__gte=timezone.now().date()
    ).order_by('date', 'time').first()

    next_appointment_data = None
    if next_appointment:
        procedures = AppointmentProcedure.objects.filter(appointment=next_appointment)
        next_appointment_data = {
            'date_time': f"{next_appointment.date} {next_appointment.time}",
            'doctor_name': next_appointment.doctor.name,
            'clinic_name': next_appointment.clinic.name,
            'procedure_name': ', '.join([ap.procedure.name for ap in procedures])
        }

    data = {
        'id': patient.id,
        'name': patient.name,
        'address': patient.address,
        'phone_number': patient.phone_number,
        'date_of_birth': patient.date_of_birth,
        'ssn_last_4': patient.ssn_last_4,
        'gender': patient.gender,
        'visits': visit_data,
        'next_appointment': next_appointment_data
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

@login_required
@require_POST
def add_visit(request):
    with transaction.atomic():
        patient = get_object_or_404(Patient, id=request.POST.get('patient_id'))
        doctor = get_object_or_404(Doctor, id=request.POST.get('visit-doctor'))
        clinic = get_object_or_404(Clinic, id=request.POST.get('visit-clinic'))
        date_time = timezone.datetime.strptime(request.POST.get('visit-date'), '%Y-%m-%dT%H:%M')
        
        visit = Visit.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=clinic,
            date=date_time.date(),
            time=date_time.time(),
            doctor_notes=request.POST.get('visit-notes')
        )
        
        for procedure_id in request.POST.getlist('visit-procedures'):
            procedure = get_object_or_404(Procedure, id=procedure_id)
            VisitProcedure.objects.create(visit=visit, procedure=procedure)
        
        return JsonResponse({'status': 'success'})
    
    
    
@login_required
@require_POST
@csrf_exempt
def add_patient(request):
    try:
        # print(request.body)
        patient = Patient.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            phone_number=request.POST.get('phone_number'),
            date_of_birth=request.POST.get('date_of_birth'),
            ssn_last_4=request.POST.get('ssn_last_4'),
            gender=request.POST.get('gender')
        )
        return JsonResponse({'status': 'success', 'message': 'Patient added successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)