from datetime import datetime
from django.shortcuts import render, redirect
from appointment.serializers import AppointmentSerializer
from course.models import Course
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from .models import Appointment

# Create your views here.
class AppointmentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.all()
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            return JsonResponse(data={"message": "Username is required"})
        
        email = request.data.get("email")
        if not email:
            return JsonResponse(data={"message": "Email is required"})
        
        phone_number = request.data.get("phone", "").strip()
        if not phone_number:
            return JsonResponse(data={"message": "Phone number is required"})
        
        Appointment.objects.create(
            username=username,
            email=email,
            phone_number=phone_number,
        )
        return redirect('appointment_booked')
    
        # serialized_appointment = AppointmentSerializer(appointment).data
        # return JsonResponse(data=serialized_appointment)
    
        
class AppointmentAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            appointment_id = kwargs.get('appointment_id')
            if not appointment_id:
                return JsonResponse(data={"message": "Appointment ID not provided"})
            
            appointments = Appointment.objects.get(id=appointment_id)
            serialized_appointments = AppointmentSerializer(appointments).data
            return JsonResponse(data=serialized_appointments)
        
        except Appointment.DoesNotExist:
            return JsonResponse(data={"message": "Appointment not found"})
        except Exception as e:
            return JsonResponse(data={"message": f"Unexpected exception {e}"})
        
class AppointmentBooked(View):
    def get(self, request, *args, **kwargs):
        print("renderr")
        return render(request, 'appointment_booked.html')
    