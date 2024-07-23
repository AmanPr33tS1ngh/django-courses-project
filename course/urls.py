from .views import CoursesAPI, CourseAPI
from django.urls import path

urlpatterns = [
    path("", CoursesAPI.as_view(), name="courses"),
    path("<str:id>", CourseAPI.as_view(), name="course"),
]
