from django.db import models

from course.models import Course
from user.models import User

# Create your models here.

class Appointment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="appointment_user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course")
    timestamp = models.DateTimeField()
