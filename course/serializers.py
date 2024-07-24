from rest_framework import serializers
from .models import Course, Feature

class CourseSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()
    timings = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    def get_schedule(self, obj):
        if not obj.schedule:
            return "Customized"
        return f"{obj.schedule.start} - {obj.schedule.end}"
        
    def get_timings(self, obj):
        course_timing = obj.time
        if not course_timing:
            return "Per Availability"
        
        return f"{course_timing.start_time.strftime("%I %p")} - {course_timing.end_time.strftime("%I %p")}"
        
    def get_start_date(self, obj):
        start_date = obj.start_date
        if not start_date:
            return "Customize"
        
        return start_date.strftime("%Y-%m-%d at %I %p")
    
    def get_features(self, obj):
        return FeatureSerializer(obj.features.all(), many=True).data
    
    class Meta:
        model = Course
        fields = ("id", "name", "is_started", "start_date", "batch", "schedule", 'timings', 'features')

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = '__all__'