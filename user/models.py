from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=20, )
    grad = models.CharField(max_length=20,)
    intake = models.IntegerField()

    def __str__(self) -> str:
        return self.user
    