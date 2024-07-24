from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)
admin.site.register(CourseTime)
admin.site.register(CourseSchedule)
admin.site.register(Feature)
admin.site.register(Enrollment)