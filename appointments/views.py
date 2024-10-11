from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST
from django.contrib.auth.decorators import login_required
from .models import Appointment
from doctors.models import Doctor
from clinics.models import Clinic
from patients.models import Patient  
from procedures.models import Procedure  
from datetime import datetime, time, timedelta
from django.db import transaction
from .models import Appointment, AppointmentProcedure

@login_required
@require_GET
def get_available_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    clinic_id = request.GET.get('clinic_id')
    date_str = request.GET.get('date')

    if not all([doctor_id, clinic_id, date_str]):
        return JsonResponse({"error": "Missing required parameters"}, status=400)

    try:
        doctor = Doctor.objects.get(id=doctor_id)
        clinic = Clinic.objects.get(id=clinic_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (Doctor.DoesNotExist, Clinic.DoesNotExist, ValueError):
        return JsonResponse({"error": "Invalid doctor, clinic, or date"}, status=400)

    # Get all booked appointments for the given doctor, clinic, and date
    booked_appointments = Appointment.objects.filter(
        doctor=doctor,
        clinic=clinic,
        date=date
    ).values_list('time', flat=True)

    # Generate all possible time slots from 9 AM to 6 PM
    all_slots = [time(hour, 0) for hour in range(9, 18)]

    # Remove booked slots from all slots
    available_slots = [slot for slot in all_slots if slot not in booked_appointments]
    slots_data = [slot.strftime('%H:%M') for slot in available_slots]
    # print(slots_data)
    return JsonResponse(slots_data, safe=False)

@login_required
@require_POST
@transaction.atomic
def book_appointment(request):
    # Extract data from request
    patient_id = request.POST.get('patient_id')
    doctor_id = request.POST.get('doctor_id')
    clinic_id = request.POST.get('clinic_id')
    date_str = request.POST.get('date')
    time_str = request.POST.get('time')
    procedure_id = request.POST.get('procedure_id')

    # Validate data
    if not all([patient_id, doctor_id, clinic_id, date_str, time_str, procedure_id]):
        return JsonResponse({"status": "error", "message": "Missing required parameters"}, status=400)

    try:
        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)
        clinic = Clinic.objects.get(id=clinic_id)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        procedure = Procedure.objects.get(id=procedure_id)
    except (ValueError, Patient.DoesNotExist, Doctor.DoesNotExist, Clinic.DoesNotExist, Procedure.DoesNotExist):
        return JsonResponse({"status": "error", "message": "Invalid input data"}, status=400)

    # Check if the slot is still available
    if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
        return JsonResponse({"status": "error", "message": "This time slot is no longer available"}, status=400)

    try:
        # Create the appointment
        appointment = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            clinic=clinic,
            date=date,
            time=time
        )

        # Create the AppointmentProcedure
        AppointmentProcedure.objects.create(
            appointment=appointment,
            procedure=procedure
        )

        return JsonResponse({"status": "success", "appointment_id": appointment.id})
    except Exception as e:
        # If any error occurs, the transaction will be rolled back
        return JsonResponse({"status": "error", "message": str(e)}, status=500)