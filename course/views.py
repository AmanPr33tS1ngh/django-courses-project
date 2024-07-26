from django.views import View
from rest_framework.views import APIView
from .models import Course, Course, CourseSchedule, CourseTime, Enrollment
from django.http import JsonResponse
from .serializers import CourseSerializer
from datetime import datetime
from django.shortcuts import render
from django.db.models import Q

# Create your views here.

""" COURSES API """

class CoursesAPI(APIView):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        courses_serialized = CourseSerializer(courses, many=True).data
        return JsonResponse(data={'courses': courses_serialized})
        # return render(request, 'courses.html', {"courses": courses_serialized})
        
    def post(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name', None)
        batch = data.get('batch', None)
        start_date = data.get('start_date', None)
        schedule = data.get('schedule', None)
        time = data.get('time', None)

        if not name:
            return JsonResponse(data={"message": "Name is required"})
        elif not batch:
            return JsonResponse(data={"message": "Batch is required"})
        elif not start_date:
            return JsonResponse(data={"message": "Start date is required"})
        elif not schedule:
            return JsonResponse(data={"message": "Schedule is required"})
        elif not time:
            return JsonResponse(data={"message": "Time is required"})
        
        if not schedule.get("start") or not schedule.get("end"):
            return JsonResponse(data={"message": "Invalid schedule"})
        if not time.get("start_time") or not time.get("end_time"):
            return JsonResponse(data={"message": "Invalid time"})

        start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")

        course_schedule = CourseSchedule.objects.create(
            start=schedule['start'],
            end=schedule['end'],
        )

        course_time = CourseTime.objects.create(
            start_time=datetime.strptime(time['start_time'], "%H:%M:%S"),
            end_time=datetime.strptime(time['end_time'], "%H:%M:%S"),
        )
        
        Course.objects.create(
            name=name,
            batch=batch,
            start_date=start_date,
            schedule=course_schedule,
            time=course_time,
        )
        return JsonResponse(data={"message": "Course created successfully"})
    
class CourseAPI(APIView):
    def get(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('id')
            course = Course.objects.get(id=course_id)
            course_serialized = CourseSerializer(course).data
            print("kksss", course_serialized)
            return JsonResponse(status=200, data={'course': course_serialized})
            # return render(request, 'course.html', {"course": course_serialized})
        except Course.DoesNotExist:
            return JsonResponse(status=404)
            # return render(request, 'course.html', {"error": "Course not found"})
        except Exception as e:
            return JsonResponse(status=400)
            # return render(request, 'course.html', {"error": f"Unexpected exception {e}"})
    
    def put(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('id')
            course = Course.objects.get(id=course_id)
            if not course:
                return JsonResponse(data={"message": "Course not found"})
            
            data = request.data
            name, batch, start_date, schedule, time, is_started = data.get('name'), data.get('batch'),
            data.get('start_date'), data.get('schedule'), data.get('time'), data.get('is_started')

            if batch:
                course.batch = batch
            if name:
                course.name = name
            if start_date:
                course.start_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
            if schedule:
                schedule_start = schedule.get("start")
                if schedule_start:
                    course.schedule.start = schedule_start
                schedule_end = schedule.get("end")
                if schedule_end:
                    course.schedule.end = schedule_end
                course.schedule.save()
            if time:
                time_start = time.get("start_time")
                if time_start:
                    course.time.start_time = datetime.strptime(time_start, "%H:%M:%S")
                time_end = time.get("end_time")
                if time_end:
                    course.time.end_time = datetime.strptime(time_end, "%H:%M:%S")
                course.time.save()
            if is_started:
                course.is_started = is_started

            course.save()
            course_serialized = CourseSerializer(course).data
            return JsonResponse(course_serialized)
        
        except Course.DoesNotExist:
            return JsonResponse(data={"message": "Course not found"})
        except Exception as e:
            return JsonResponse(data={"message": f"Unexpected exception {e}"})
        

    def delete(self, request, *args, **kwargs):
        try:
            course_id = kwargs.get('id')
            course = Course.objects.get(id=course_id)
            if not course:
                return JsonResponse(data={"message": "Course not found"})
            
            course.delete()
            return JsonResponse(data={"message": "Course deleted successfully"})

        except Course.DoesNotExist:
            return JsonResponse(data={"message": "Course not found"})
        except Exception as e:
            return JsonResponse(data={"message": f"Unexpected exception {e}"})
        
class EnrollCourseAPI(APIView):
    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get("name", None)
            email = request.POST.get("email", None)
            phone_number = request.POST.get("phone", None)
            course_id = request.POST.get('course_id')

            if not name or not email or not phone_number or not course_id:
                return JsonResponse(data={"error": "All fields are required"})
            
            existing_enrollment = Enrollment.objects.filter(Q(email=email, course__id=course_id) | Q(phone_number=phone_number, course__id=course_id))
            if existing_enrollment:
                return JsonResponse(data={"error": "Enrollment already exists for this course"})
            
            course = Course.objects.get(id=course_id)
            Enrollment.objects.create(
                course=course,
                username=name,
                email=email,
                phone_number=phone_number,
            )
            return JsonResponse(status=200)
            # return render(request, 'enrolled.html')
        
        except Course.DoesNotExist:
            return JsonResponse(data={"error": "Course not found"})
        except Exception as e:
            return JsonResponse(data={"error": f"Unexpected error: {e}"})