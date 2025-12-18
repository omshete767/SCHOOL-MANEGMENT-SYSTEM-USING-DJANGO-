from django.db import models
from courses.models import Course
from students.models import Student

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)
    is_absent = models.BooleanField(default=True)

    class Meta:
        unique_together = ('course', 'student', 'date')

    def __str__(self):
        return f"{self.student} - {self.course} - {self.date}"
