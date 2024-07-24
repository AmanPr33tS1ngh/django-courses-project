from .views import CoursesAPI, CourseAPI, EnrollCourseAPI
from django.urls import path

urlpatterns = [
    path("enroll", EnrollCourseAPI.as_view(), name="enroll"),
    path("", CoursesAPI.as_view(), name="courses"),
    path("<str:id>", CourseAPI.as_view(), name="course"),
]
