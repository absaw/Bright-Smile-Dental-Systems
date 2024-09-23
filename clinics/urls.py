from django.urls import path
from . import views
# urlpatterns = [
#     path('', views.get_index),
# ]


urlpatterns = [
    path('', views.clinic_list, name='clinic_list'),
    path('<int:clinic_id>/', views.clinic_detail, name='clinic_detail'),
    path('api/clinics/', views.get_clinics, name='get_clinics'),
    path('api/clinics/<int:clinic_id>/', views.get_clinic_detail, name='get_clinic_detail'),
    path('api/clinics/<int:clinic_id>/update/', views.update_clinic, name='update_clinic'),
    path('api/clinics/add/', views.add_clinic, name='add_clinic'),
    path('api/doctors/available/', views.get_available_doctors, name='get_available_doctors'),
    path('api/doctors/add-affiliation/', views.add_doctor_affiliation, name='add_doctor_affiliation'),
    path('api/doctors/<int:doctor_id>/update-affiliation/', views.update_doctor_affiliation, name='update_doctor_affiliation'),
    path('api/clinics/by-procedure/<int:procedure_id>/', views.clinics_by_procedure, name='clinics_by_procedure'),
]
