from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
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

    next_appointment = Appointment.objects.filter(
        patient=patient,
        time_slot__date__gte=timezone.now().date()
    ).order_by('time_slot__date', 'time_slot__start_time').first()

    next_appointment_data = None
    if next_appointment:
        procedures = AppointmentProcedure.objects.filter(appointment=next_appointment)
        next_appointment_data = {
            'date_time': f"{next_appointment.time_slot.date} {next_appointment.time_slot.start_time}",
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
    print(data)
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
def add_visit(request):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=request.POST.get('patient_id'))
        doctor = get_object_or_404(Doctor, id=request.POST.get('visit-doctor'))
        clinic = get_object_or_404(Clinic, id=request.POST.get('visit-clinic'))
        time_slot = TimeSlot.objects.create(
            date=request.POST.get('visit-date').split('T')[0],
            start_time=request.POST.get('visit-date').split('T')[1],
            end_time=(timezone.datetime.strptime(request.POST.get('visit-date'), '%Y-%m-%dT%H:%M') + timezone.timedelta(hours=1)).time()
        )
        
        visit = Visit.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=clinic,
            time_slot=time_slot,
            doctor_notes=request.POST.get('visit-notes')
        )
        
        for procedure_id in request.POST.getlist('visit-procedures'):
            procedure = get_object_or_404(Procedure, id=procedure_id)
            VisitProcedure.objects.create(visit=visit, procedure=procedure)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


# @login_required
# @require_POST
# def book_appointment(request):
#     with transaction.atomic():
#         patient = get_object_or_404(Patient, id=request.POST.get('patient_id'))
#         doctor = get_object_or_404(Doctor, id=request.POST.get('appointment-doctor'))
#         clinic = get_object_or_404(Clinic, id=request.POST.get('appointment-clinic'))
#         procedure = get_object_or_404(Procedure, id=request.POST.get('appointment-procedure'))
#         time_slot = get_object_or_404(TimeSlot, id=request.POST.get('appointment-date'))

#         if Appointment.objects.filter(time_slot=time_slot).exists():
#             return JsonResponse({'status': 'error', 'message': 'This time slot is no longer available.'}, status=400)

#         appointment = Appointment.objects.create(
#             patient=patient,
#             doctor=doctor,
#             clinic=clinic,
#             time_slot=time_slot
#         )
        
#         AppointmentProcedure.objects.create(appointment=appointment, procedure=procedure)
        
#     return JsonResponse({'status': 'success'})
# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         patient = get_object_or_404(Patient, id=request.POST.get('patient_id'))
#         doctor = get_object_or_404(Doctor, id=request.POST.get('appointment-doctor'))
#         clinic = get_object_or_404(Clinic, id=request.POST.get('appointment-clinic'))
#         procedure = get_object_or_404(Procedure, id=request.POST.get('appointment-procedure'))
#         appointment_date = request.POST.get('appointment-date')

#         with transaction.atomic():
#             # Check if the time slot is available
#             time_slot = TimeSlot.objects.filter(
#                 date=appointment_date.split('T')[0],
#                 start_time=appointment_date.split('T')[1],
#                 doctor_schedule__doctor_clinic_affiliation__doctor=doctor,
#                 doctor_schedule__doctor_clinic_affiliation__clinic=clinic,
#                 appointment__isnull=True
#             ).first()

#             if not time_slot:
#                 return JsonResponse({'status': 'error', 'message': 'The selected time slot is not available.'}, status=400)

#             # Create the appointment
#             appointment = Appointment.objects.create(
#                 patient=patient,
#                 doctor=doctor,
#                 clinic=clinic,
#                 time_slot=time_slot
#             )
            
#             AppointmentProcedure.objects.create(appointment=appointment, procedure=procedure)
        
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


# @login_required
# def get_available_time_slots(request, doctor_id, clinic_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     clinic = get_object_or_404(Clinic, id=clinic_id)
    
#     # Get all time slots for the next 3 months
#     start_date = timezone.now().date()
#     end_date = start_date + timezone.timedelta(days=90)
    
#     all_slots = TimeSlot.objects.filter(
#         date__range=(start_date, end_date),
#         doctor_schedule__doctor_clinic_affiliation__doctor=doctor,
#         doctor_schedule__doctor_clinic_affiliation__clinic=clinic
#     ).exclude(
#         appointment__isnull=False
#     ).order_by('date', 'start_time')
    
#     available_slots = [
#         {
#             'start_time': f"{slot.date}T{slot.start_time}",
#             'end_time': f"{slot.date}T{slot.end_time}"
#         }
#         for slot in all_slots
#     ]
    
#     return JsonResponse(available_slots, safe=False)



# @login_required
# def book_appointment(request):
#     if request.method == 'POST':
#         patient = get_object_or_404(Patient, id=request.POST.get('patient_id'))
#         doctor = get_object_or_404(Doctor, id=request.POST.get('appointment-doctor'))
#         clinic = get_object_or_404(Clinic, id=request.POST.get('appointment-clinic'))
#         procedure = get_object_or_404(Procedure, id=request.POST.get('appointment-procedure'))
#         time_slot = TimeSlot.objects.create(
#             date=request.POST.get('appointment-date').split('T')[0],
#             start_time=request.POST.get('appointment-date').split('T')[1],
#             end_time=(timezone.datetime.strptime(request.POST.get('appointment-date'), '%Y-%m-%dT%H:%M') + timezone.timedelta(minutes=procedure.duration_minutes)).time()
#         )
        
#         appointment = Appointment.objects.create(
#             patient=patient,
#             doctor=doctor,
#             clinic=clinic,
#             time_slot=time_slot
#         )
        
#         AppointmentProcedure.objects.create(appointment=appointment, procedure=procedure)
        
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'}, status=400)