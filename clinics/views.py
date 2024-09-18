from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Clinic,ClinicProcedure
from doctors.models import Doctor, DoctorClinicAffiliation, DoctorProcedure
from procedures.models import Procedure
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie

def get_index(request):
    if request.method == "GET":
        return render(request,'index.html')
    
def clinic_list(request):
    return render(request, 'clinics/clinic_list.html')

@ensure_csrf_cookie
def clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    print(clinic)
    return render(request, 'clinics/clinic_detail.html', {'clinic': clinic})

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

# def get_clinic_detail(request, clinic_id):
#     clinic = get_object_or_404(Clinic, id=clinic_id)
#     doctor_affiliations = DoctorClinicAffiliation.objects.filter(clinic=clinic).select_related('doctor')
    
#     data = {
#         'id': clinic.id,
#         'name': clinic.name,
#         'address': clinic.address,
#         'phone_number': clinic.phone_number,
#         'email': clinic.email,
#         'doctors': [{
#             'id': affiliation.doctor.id,
#             'name': affiliation.doctor.name,
#             'office_address': affiliation.office_address,
#             'schedule': 'Schedule info not available'  # You'll need to implement this based on your schedule model
#         } for affiliation in doctor_affiliations]
#     }
#     return JsonResponse(data)

# def update_clinic(request, clinic_id):
#     if request.method == 'POST':
#         clinic = get_object_or_404(Clinic, id=clinic_id)
#         clinic.name = request.POST.get('name')
#         clinic.address = request.POST.get('address')
#         clinic.phone_number = request.POST.get('phone_number')
#         clinic.email = request.POST.get('email')
#         clinic.save()
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'error'}, status=400)
@ensure_csrf_cookie
def get_clinic_detail(request, clinic_id):
    clinic = get_object_or_404(Clinic, id=clinic_id)
    doctor_affiliations = DoctorClinicAffiliation.objects.filter(clinic=clinic).select_related('doctor')
    # clinic_procedures = ClinicProcedure.objects.filter(clinic=clinic).select_related('procedure')
    
    data = {
        'id': clinic.id,
        'name': clinic.name,
        'address': clinic.address,
        'phone_number': clinic.phone_number,
        'email': clinic.email,
        # 'procedures': [{'id': cp.procedure.id, 'name': cp.procedure.name} for cp in clinic_procedures],
        'doctors': [{
            'id': affiliation.doctor.id,
            'name': affiliation.doctor.name,
            'office_address': affiliation.office_address,
            'schedule': 'Schedule info not available',  # You'll need to implement this based on your schedule model
            'procedures': ', '.join([dp.procedure.name for dp in DoctorProcedure.objects.filter(doctor=affiliation.doctor).select_related('procedure')])
        } for affiliation in doctor_affiliations]
    }
    return JsonResponse(data)

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