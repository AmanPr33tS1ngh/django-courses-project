from django.shortcuts import render
from appointment.serializers import AppointmentSerializer
from course.models import Course
from rest_framework.views import APIView
from django.http import JsonResponse
from django.views import View
from .models import Appointment
from django.db.models import Q

# Create your views here.
class AppointmentsAPI(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_anonymous:
            return JsonResponse(status=401, data=dict())
        
        appointments = Appointment.objects.filter(user=user)
        serialized_appointments = AppointmentSerializer(appointments).data
        return JsonResponse(data=serialized_appointments)

    def post(self, request, *args, **kwargs):   
        try:
            user = request.user
            if user.is_anonymous:
                return JsonResponse(status=401, data=dict())

            course_name = request.data.get('course', '').strip()
            if not course_name:
                return JsonResponse({"message": "Course name is required"})

            course = Course.objects.get(name=course_name)
            if not course:
                return JsonResponse({"message": "Course not found"})
            
            fullname = request.data.get("fullName", '').strip()
            if not fullname:
                return JsonResponse({"message": "name is required"})
            
            email = request.data.get("email", '').strip()
            if not email:
                return JsonResponse({"message": "Email is required"})
            
            phone_number = request.data.get("phoneNumber", '').strip()
            if not phone_number:
                return JsonResponse({"message": "Phone number is required"})

            message = request.data.get("message", "").strip()

            existing_appointment = Appointment.objects.filter(
                Q(user__id=user.id) | Q(email=email) | Q(phone_number=phone_number), course__id=course.id,
            ).first()
            if existing_appointment:
                return JsonResponse({"message": "You have already booked for this demo. Please wait for our team to reach out to you."})

            appointment = Appointment.objects.create(
                user=user,
                fullname=fullname,
                email=email,
                phone_number=phone_number,
                message=message,
                course=course,
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({"message": f"Unexpected error occurred: {e}"})
        
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
        return render(request, 'appointment_booked.html')
    