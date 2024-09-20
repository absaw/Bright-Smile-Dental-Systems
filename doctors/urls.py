from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
    path('api/doctors/', views.get_doctors, name='get_doctors'),
    path('api/doctors/<int:doctor_id>/', views.get_doctor_detail, name='get_doctor_detail'),
    path('api/doctors/<int:doctor_id>/update/', views.update_doctor, name='update_doctor'),
]