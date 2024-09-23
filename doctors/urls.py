from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('api/doctors/', views.get_doctors, name='get_doctors'),
    path('api/doctors/<int:doctor_id>/', views.get_doctor_detail, name='get_doctor_detail'),
    path('api/doctors/<int:doctor_id>/update/', views.update_doctor, name='update_doctor'),
    path('api/doctors/by-procedure-and-clinic/<int:procedure_id>/<int:clinic_id>/', views.doctors_by_procedure_and_clinic, name='doctors_by_procedure_and_clinic'),
    path('api/add_doctor/', views.add_doctor, name='add_doctor'),
]