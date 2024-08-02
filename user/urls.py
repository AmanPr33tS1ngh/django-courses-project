from .views import UserAPI
from django.urls import path


urlpatterns = [
    path("", UserAPI.as_view(), name="user_api"),
]
