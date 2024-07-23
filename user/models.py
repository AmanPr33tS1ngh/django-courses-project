from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    banner = models.ImageField(upload_to="user_banner/", default='user_banner.jpg')
    profile_picture = models.ImageField(upload_to="user_profile_picture/", default='user_banner.jpg')
    joining_date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self) -> str:
        return super().__str__() + " -> " + self.username
