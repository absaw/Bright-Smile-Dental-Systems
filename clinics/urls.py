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
]