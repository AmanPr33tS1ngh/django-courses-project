from django.shortcuts import render
from appointment.serializers import AppointmentSerializer
from rest_framework.views import APIView
from django.http import JsonResponse

# Create your views here.
class AppointmentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return JsonResponse(data={"message": "User not authenticated"})
        
        appointments = AppointmentAPI.objects.all()
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return JsonResponse(data={"message": "User not authenticated"})
        
        appointments = AppointmentAPI.objects.all()
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)
    

class AppointmentAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous():
            return JsonResponse(data={"message": "User not authenticated"})
        
        appointment_id = kwargs.get('appointment_id')
        if not appointment_id:
            return JsonResponse(data={"message": "Appointment ID not provided"})
        
        appointment = AppointmentAPI.objects.get(id=appointment_id)
        if not appointment:
            return JsonResponse(data={"message": "Appointment not found"})
        
        appointments = AppointmentAPI.objects.filter(appointment__id=appointment_id).first()
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)
    