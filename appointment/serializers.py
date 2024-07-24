from appointment.models import Appointment
from rest_framework import serializers

class AppointmentSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField()

    def get_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    class Meta:
        model = Appointment
        fields = ("username", "email", "phone_number", "timestamp")