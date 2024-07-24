from datetime import datetime
from django.shortcuts import render
from appointment.serializers import AppointmentSerializer
from course.models import Course
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Appointment

# Create your views here.
class AppointmentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return JsonResponse(data={"message": "User not authenticated"})
        
        appointments = AppointmentAPI.objects.all()
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous:
            return JsonResponse(data={"message": "User not authenticated"})
        
        timestamp = request.data.get("timestamp")
        if not timestamp:
            return JsonResponse(data={"message": "Timestamp is required"})
        
        course_id = request.data.get("course_id")
        if not course_id:
            return JsonResponse(data={"message": "Please select course"})
        
        phone_number = request.data.get("phone_number", "").strip()
        if not phone_number:
            return JsonResponse(data={"message": "Phone number is required"})
        
        appointment_time = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

        if appointment_time < datetime.now():
            return JsonResponse(data={"message": "Cannot book an appointment in the past"})
        
        booked_appointment = Appointment.objects.filter(
            course__id=course_id,
            timestamp=appointment_time
        ).first()

        if booked_appointment:
            return JsonResponse(data={"message": "There's an already booked appointment for this course at this time"})
        
        course = self.get_course(course_id=course_id)
        if not course:
            return JsonResponse(data={"message": "Course not found"})
        
        if not course.is_started:
            return JsonResponse(data={"message": "Course has not started yet"})

        appointment = Appointment.objects.create(
            user=user,
            course=course,
            timestamp=timestamp,
            phone_number=phone_number,
        )
        serialized_appointment = AppointmentSerializer(appointment).data
        return JsonResponse(data=serialized_appointment)
    
    def get_course(self, course_id: int):
        try:
            return Course.objects.get(course__id=course_id)
        except Course.DoesNotExist:
            return None
        
class AppointmentAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # user = request.user
            # if user.is_anonymous:
            #     return JsonResponse(data={"message": "User not authenticated"})
            
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
        
        