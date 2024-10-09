from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from .models import Doctor, DoctorClinicAffiliation, PatientDoctorAffiliation, DoctorProcedure
from procedures.models import Procedure
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

@login_required
def doctor_list(request):
    return render(request, 'doctors/doctor_list.html')

@login_required
@ensure_csrf_cookie
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

@login_required
def get_doctors(request):
    doctors = Doctor.objects.all()
    data = [{
        'id': doctor.id,
        'npi': doctor.npi,
        'name': doctor.name,
        'specialties': [dp.procedure.name for dp in doctor.doctorprocedure_set.all()],
        'affiliated_clinics': doctor.doctorclinicaffiliation_set.count(),
        'affiliated_patients': doctor.patientdoctoraffiliation_set.count()
    } for doctor in doctors]
    # print(data)
    return JsonResponse(data, safe=False)
# working final version
@login_required
@ensure_csrf_cookie
def get_doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    clinic_affiliations = DoctorClinicAffiliation.objects.filter(doctor=doctor).select_related('clinic')
    patient_affiliations = PatientDoctorAffiliation.objects.filter(doctor=doctor).select_related('patient')
    
    data = {
        'id': doctor.id,
        'npi': doctor.npi,
        'name': doctor.name,
        'email': doctor.email,
        'phone_number': doctor.phone_number,
        'specialties': [dp.procedure.name for dp in doctor.doctorprocedure_set.all()],
        'all_procedures': list(Procedure.objects.values('id', 'name')),
        'affiliated_clinics': [{
            'name': affiliation.clinic.name,
            'office_address': affiliation.office_address,
            'working_schedule': affiliation.working_schedule
        } for affiliation in clinic_affiliations],
        'affiliated_patients': [{
            'name': affiliation.patient.name,
            'date_of_birth': affiliation.patient.date_of_birth.strftime('%Y-%m-%d') if affiliation.patient.date_of_birth else None,
            'last_visit_date': 'N/A'  # You'll need to implement this based on your visit model
        } for affiliation in patient_affiliations]
    }
    # print(data)
    return JsonResponse(data)

@login_required
def update_doctor(request, doctor_id):
    if request.method == 'POST':
        doctor = get_object_or_404(Doctor, id=doctor_id)
        doctor.npi = request.POST.get('npi')
        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.save()
        
        # Update specialties (procedures)
        new_specialties = request.POST.getlist('specialties')
        current_specialties = set(dp.procedure.id for dp in doctor.doctorprocedure_set.all())
        new_specialties_set = set(map(int, new_specialties))
        
        # Remove specialties that are no longer selected
        for dp in doctor.doctorprocedure_set.filter(procedure__id__in=current_specialties - new_specialties_set):
            dp.delete()
        
        # Add new specialties
        for procedure_id in new_specialties_set - current_specialties:
            DoctorProcedure.objects.create(doctor=doctor, procedure_id=procedure_id)
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def doctors_by_procedure_and_clinic(request, procedure_id, clinic_id):
    doctor_procedures = DoctorProcedure.objects.filter(procedure_id=procedure_id, doctor__doctorclinicaffiliation__clinic_id=clinic_id).select_related('doctor')
    doctors = [{'id': dp.doctor.id, 'name': dp.doctor.name} for dp in doctor_procedures]
    return JsonResponse(doctors, safe=False)



    
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def add_doctor(request):
    try:
        data = request.POST
        new_doctor = Doctor.objects.create(
            npi=data['npi'],
            name=data['name'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        
        specialties = data.getlist('specialties')
        for specialty_id in specialties:
            DoctorProcedure.objects.create(doctor=new_doctor, procedure_id=specialty_id)
        
        return JsonResponse({'status': 'success', 'message': 'Doctor added successfully'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    




