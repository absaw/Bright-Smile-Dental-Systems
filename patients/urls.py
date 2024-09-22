from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('api/patients/', views.get_patients, name='get_patients'),
    path('api/patients/<int:patient_id>/', views.get_patient_detail, name='get_patient_detail'),
    path('api/patients/<int:patient_id>/update/', views.update_patient, name='update_patient'),
    path('api/visits/add/', views.add_visit, name='add_visit'),
    path('api/appointments/book/', views.book_appointment, name='book_appointment'),
    # path('api/time-slots/available/<int:doctor_id>/<int:clinic_id>/', views.get_available_time_slots, name='get_available_time_slots'),

]