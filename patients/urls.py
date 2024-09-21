from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('api/patients/', views.get_patients, name='get_patients'),
    path('api/patients/<int:patient_id>/', views.get_patient_detail, name='get_patient_detail'),
    path('api/patients/<int:patient_id>/update/', views.update_patient, name='update_patient'),
]