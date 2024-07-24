from .views import AppointmentAPI, AppointmentsAPI
from django.urls import path

urlpatterns = [
    path("", AppointmentsAPI.as_view(), name="appointments"),
    path("<str:appointment_id>", AppointmentAPI.as_view(), name="appointment"),
]
