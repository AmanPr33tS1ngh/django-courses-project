from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    timings = serializers.SerializerMethodField()
    
    def get_schedule(self, obj):
        if not obj.schedule:
            return "Customized"
        return f"{obj.schedule.start} - {obj.schedule.end}"
        
    def get_timings(self, obj):
        course_timing = obj.time
        if not course_timing:
            return "Per Availability"
        
        return f"{course_timing.start_time.strftime("%I %p")} - {course_timing.end_time.strftime("%I %p")}"
        
    class Meta:
        model = Course
        fields = ("name", "is_started", "start_date", "batch", "schedule", 'timings')
