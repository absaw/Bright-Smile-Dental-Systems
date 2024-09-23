from django.urls import path
from . import views

urlpatterns = [
    path('api/available-time-slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('api/book/', views.book_appointment, name='book_appointment'),
]