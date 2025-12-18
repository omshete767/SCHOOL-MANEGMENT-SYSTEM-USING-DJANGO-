from django.db import models
from teachers.models import Teacher
from students.models import Student

class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    students = models.ManyToManyField(
        Student,
        blank=True
    )
    total_lectures = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.name} ({self.code})"
