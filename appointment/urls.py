from .views import AppointmentAPI, AppointmentBooked, AppointmentsAPI
from django.urls import path

urlpatterns = [
    path("", AppointmentsAPI.as_view(), name="appointments"),
    path("<str:appointment_id>", AppointmentAPI.as_view(), name="appointment"),
    path('appointment_booked/', AppointmentBooked.as_view(), name='appointment_booked'),
]
