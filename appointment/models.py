from django.db import models
from django.contrib.auth.models import User

from course.models import Course

# Create your models here.

class Appointment(models.Model):
    user = models.ForeignKey(User, related_name='appointments', on_delete=models.CASCADE, )
    fullname = models.TextField(max_length=150)
    email = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    course = models.ForeignKey(Course, related_name='appointments', on_delete=models.CASCADE, )
    
    def __str__(self, ):
        return f'{self.fullname} - {self.email} - {self.phone_number}'
    