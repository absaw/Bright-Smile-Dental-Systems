from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from .models import TimeSlot
from doctors.models import Doctor
from clinics.models import Clinic
from django.utils import timezone
from datetime import datetime, time, timedelta

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

    # Get all booked slots for the given doctor, clinic, and date
    booked_slots = TimeSlot.objects.filter(
        doctor=doctor,
        clinic=clinic,
        date=date
    ).values_list('start_time', flat=True)

    # Generate all possible time slots from 9 AM to 6 PM
    all_slots = [time(hour, 0) for hour in range(9, 18)]

    # Remove booked slots from all slots
    available_slots = [slot for slot in all_slots if slot not in booked_slots]

    # Format the available slots for the response
    slots_data = [
        {
            "date": date_str,
            "start_time": slot.strftime('%H:%M'),
            "end_time": (datetime.combine(date, slot) + timedelta(hours=1)).time().strftime('%H:%M')
        }
        for slot in available_slots
    ]

    return JsonResponse(slots_data, safe=False)