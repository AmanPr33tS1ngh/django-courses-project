from django.db import models
# Create your models here.

class Appointment(models.Model):
    username = models.TextField(max_length=150)
    email = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self, ):
        return f'{self.username} - {self.email} - {self.phone_number}'
    
class Contact(models.Model):
    name = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    subject = models.TextField(max_length=100)
    message = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.name} - {self.email}"