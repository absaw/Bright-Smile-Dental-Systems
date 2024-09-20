from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('api/patients/', views.get_patients, name='get_patients'),
]