from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Doctor, DoctorClinicAffiliation, PatientDoctorAffiliation, DoctorProcedure
from procedures.models import Procedure
def doctor_list(request):
    return render(request, 'doctors/doctor_list.html')

@ensure_csrf_cookie
def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})

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
# @ensure_csrf_cookie
# working
# def get_doctor_detail(request, doctor_id):
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     clinic_affiliations = DoctorClinicAffiliation.objects.filter(doctor=doctor).select_related('clinic')
#     patient_affiliations = PatientDoctorAffiliation.objects.filter(doctor=doctor).select_related('patient')
    
#     data = {
#         'id': doctor.id,
#         'npi': doctor.npi,
#         'name': doctor.name,
#         'email': doctor.email,
#         'phone_number': doctor.phone_number,
#         'specialties': [dp.procedure.name for dp in doctor.doctorprocedure_set.all()],
#         'affiliated_clinics': [{
#             'name': affiliation.clinic.name,
#             'office_address': affiliation.office_address,
#             'working_schedule': affiliation.working_schedule
#         } for affiliation in clinic_affiliations],
#         'affiliated_patients': [{
#             'name': affiliation.patient.name,
#             'date_of_birth': affiliation.patient.date_of_birth,
#             'last_visit_date': 'N/A'  # You'll need to implement this based on your visit model
#         } for affiliation in patient_affiliations]
#     }
#     # print(data)
#     return JsonResponse(data)

# def update_doctor(request, doctor_id):
#     if request.method == 'POST':
#         doctor = get_object_or_404(Doctor, id=doctor_id)
#         doctor.npi = request.POST.get('npi')
#         doctor.name = request.POST.get('name')
#         doctor.email = request.POST.get('email')
#         doctor.phone_number = request.POST.get('phone_number')
#         doctor.save()
        
#         # Update specialties (procedures)
#         # specialties = request.POST.get('specialties').split(',')
#         # doctor.doctorprocedure_set.all().delete()
#         # for specialty in specialties:
#         #     print(specialty)
#         #     procedure, _ = Procedure.objects.get_or_create(name=specialty.strip())
#         #     DoctorProcedure.objects.create(doctor=doctor, procedure=procedure)
#         # print("here")
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'}, status=400)