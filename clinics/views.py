from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Clinic,ClinicProcedure
from doctors.models import Doctor, DoctorClinicAffiliation, DoctorProcedure
from procedures.models import Procedure
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

@login_required
def clinic_list(request):
    return render(request, 'clinics/clinic_list.html')

@login_required
@ensure_csrf_cookie
def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    # print(clinic)
    return render(request, 'clinics/clinic_detail.html', {'clinic': clinic})

@login_required
def get_clinics(request):
    clinics = Clinic.objects.all()
    data = [{
        'id': clinic.id,
        'name': clinic.name,
        'phone_number': clinic.phone_number,
        'city': clinic.city,
        'state': clinic.state,
        'doctor_count': clinic.doctor_count(),
        'patient_count': clinic.patient_count()
    } for clinic in clinics]
    return JsonResponse(data, safe=False)

@login_required
@ensure_csrf_cookie
def get_clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctor_affiliations = DoctorClinicAffiliation.objects.filter(clinic=clinic).select_related('doctor')
    clinic_procedures = ClinicProcedure.objects.filter(clinic=clinic).select_related('procedure')
    
    data = {
        'id': clinic.id,
        'name': clinic.name,
        'address': clinic.address,
        'phone_number': clinic.phone_number,
        'email': clinic.email,
        'procedures': [{'id': cp.procedure.id, 'name': cp.procedure.name} for cp in clinic_procedures],
        'doctors': [{
            'id': affiliation.doctor.id,
            'name': affiliation.doctor.name,
            'office_address': affiliation.office_address,
            'working_schedule': affiliation.working_schedule,  
            'procedures': ', '.join([dp.procedure.name for dp in DoctorProcedure.objects.filter(doctor=affiliation.doctor).select_related('procedure')])
        } for affiliation in doctor_affiliations]
    }
    # print(data)
    return JsonResponse(data)

@login_required
def update_clinic(request, clinic_id):
    if request.method == 'POST':
        clinic = get_object_or_404(Clinic, id=clinic_id)
        clinic.name = request.POST.get('name')
        clinic.address = request.POST.get('address')
        clinic.phone_number = request.POST.get('phone_number')
        clinic.email = request.POST.get('email')
        clinic.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@ensure_csrf_cookie
def get_available_doctors(request):
    clinic_id = request.GET.get('clinic_id')
    affiliated_doctors = DoctorClinicAffiliation.objects.filter(clinic_id=clinic_id).values_list('doctor_id', flat=True)
    available_doctors = Doctor.objects.exclude(id__in=affiliated_doctors)
    data = [{'id': doctor.id, 'name': doctor.name} for doctor in available_doctors]
    return JsonResponse(data, safe=False)

@login_required
@ensure_csrf_cookie
def add_doctor_affiliation(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        clinic_id = request.POST.get('clinic_id')
        office_address = request.POST.get('office_address')
        working_schedule = request.POST.get('working_schedule')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        clinic = get_object_or_404(Clinic, id=clinic_id)

        affiliation, created = DoctorClinicAffiliation.objects.get_or_create(
            doctor=doctor,
            clinic=clinic,
            defaults={'office_address': office_address, 'working_schedule': working_schedule}
        )

        if not created:
            affiliation.office_address = office_address
            affiliation.working_schedule = working_schedule
            affiliation.save()
        
        # Update ClinicProcedure table
        doctor_procedures = DoctorProcedure.objects.filter(doctor=doctor)
        for doctor_procedure in doctor_procedures:
            ClinicProcedure.objects.get_or_create(
                clinic=clinic,
                procedure=doctor_procedure.procedure
            )
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
@ensure_csrf_cookie
def update_doctor_affiliation(request, doctor_id):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        office_address = request.POST.get('office_address')
        working_schedule = request.POST.get('working_schedule')

        affiliation = get_object_or_404(DoctorClinicAffiliation, doctor_id=doctor_id, clinic_id=clinic_id)
        affiliation.office_address = office_address
        affiliation.working_schedule = working_schedule
        affiliation.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def clinics_by_procedure(request, procedure_id):
    clinic_procedures = ClinicProcedure.objects.filter(procedure_id=procedure_id).select_related('clinic')
    clinics = [{'id': cp.clinic.id, 'name': cp.clinic.name} for cp in clinic_procedures]
    # print('clinics::',clinics) #verified
    return JsonResponse(clinics, safe=False)


@login_required
@require_POST
@ensure_csrf_cookie
def add_clinic(request):
    try:
        clinic = Clinic.objects.create(
            name=request.POST.get('name'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            phone_number=request.POST.get('phone_number'),
            email=request.POST.get('email')
        )
        return JsonResponse({'status': 'success', 'id': clinic.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)