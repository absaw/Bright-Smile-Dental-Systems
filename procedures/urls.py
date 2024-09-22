from django.urls import path
from . import views

urlpatterns = [
    path('api/procedures/', views.procedure_list, name='procedure_list'),
]