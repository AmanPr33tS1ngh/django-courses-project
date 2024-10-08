from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Weekdays(models.TextChoices):
    MONDAY = "Monday", _('Monday')
    TUESDAY = 'Tuesday', _('Tuesday')
    WEDNESDAY = 'Wednesday', _('Wednesday')
    THURSDAY = 'Thursday', _('Thursday')
    FRIDAY = 'Friday', _('Friday')
    SATURDAY = 'Saturday', _('Saturday')
    SUNDAY = 'Sunday', _('Sunday')


class CourseTime(models.Model):
    start_time = models.TimeField(null=True, default=None)
    end_time = models.TimeField(null=True, default=None)

    def __str__(self) -> str:
        output = ""
        if not self.start_time:
            return None
        
        if self.start_time:
            output += f"Start Time: {self.start_time} "
        if self.end_time:
            output += f"| End Time: {self.end_time}"
        
        return output
    
class CourseSchedule(models.Model):
    start = models.CharField(
        max_length=9,
        choices=Weekdays.choices,
        null=True,
        default=None
    )
    end = models.CharField(
        max_length=9,
        choices=Weekdays.choices,
        null=True,
        default=None
    )
    def __str__(self) -> str:
        output = ""
        if not self.start:
            return None
        
        if self.start:
            output += f"Start: {self.start} "
        if self.end:
            output += f"| End: {self.end}"
        
        return output

class Feature(models.Model):
    detail = models.TextField(max_length=100)

    def __str__(self):
        return self.detail

    
class Course(models.Model):
    name = models.TextField(max_length=100)
    batch = models.IntegerField()
    detail = models.TextField(max_length=200)

    is_started = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, default=None)
    schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, related_name="schedule", null=True, default=None)
    time = models.ForeignKey(CourseTime, on_delete=models.CASCADE, related_name="time", null=True, default=None)
    features = models.ManyToManyField(Feature, related_name='features')
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return f"{self.name} - Batch {self.batch}"

class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    username = models.TextField(max_length=100)
    email = models.TextField(max_length=100)
    phone_number = models.TextField(max_length=15)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.email} - {self.phone_number}"
    