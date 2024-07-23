from appointment.models import Appointment
from course.serializers import CourseSerializer
from rest_framework import serializers
from user.serializers import UserSerializer

class AppointmentSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    appointment_timestamp = serializers.DateTimeField()

    def get_user(self, obj):
        return UserSerializer(obj.user).data
    
    def get_course(self, obj):
        return CourseSerializer(obj.course).data
    
    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Appointment
        fields = ("user", "course", "timestamp")