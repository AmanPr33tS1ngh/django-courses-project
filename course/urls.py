from .views import CoursesAPI, CourseAPI, EnrollCourseAPI
from django.urls import path

urlpatterns = [
    path("", CoursesAPI.as_view(), name="courses"),
    path("enroll", EnrollCourseAPI.as_view(), name="enroll"),
    path("<str:slug>", CourseAPI.as_view(), name="course"),
]
