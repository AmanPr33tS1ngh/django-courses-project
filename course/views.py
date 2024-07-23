from rest_framework.views import APIView
from .models import Course, Course, CourseSchedule, CourseTime
from django.http import JsonResponse
from .serializers import CourseSerializer
from datetime import datetime
# Create your views here.

""" COURSES API """

class CoursesAPI(APIView):
    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        courses_serialized = CourseSerializer(courses, many=True).data
        return JsonResponse(data={"courses": courses_serialized})
    
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
        course_id = kwargs.get('id')
        course = Course.objects.get(id=course_id)
        course_serialized = CourseSerializer(course).data
        return JsonResponse(course_serialized)
    
    def put(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        course = Course.objects.get(id=course_id)
        if not course:
            return JsonResponse(data={"message": "Course not found"})
        
        data = request.data
        batch, schedule_start, schedule_end = data.get('batch'), data.get('schedule_start'), data.get('schedule_start')

        if batch:
            course.batch = data.get('batch')
        if schedule_start:
            course.schedule_start = data.get('schedule_start')
        if schedule_end:
            course.schedule_end = data.get('schedule_end')
            
        course.save()
        course_serialized = CourseSerializer(course).data
        return JsonResponse(course_serialized)
    
    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        course = Course.objects.get(id=course_id)
        if not course:
            return JsonResponse(data={"message": "Course not found"})
        
        course.delete()
        return JsonResponse(data={"message": "Course deleted successfully"})
    