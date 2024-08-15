from appointment.models import Appointment
from course.serializers import CourseSerializer
from rest_framework import serializers

class AppointmentSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField()
    course = serializers.SerializerMethodField()

    # def get_timestamp(self, obj):
    #     return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_course(self, obj):
        return CourseSerializer(obj.course).data
    
    class Meta:
        model = Appointment
        fields = ("fullname", "email", "phone_number", "timestamp", "message", 'course')
