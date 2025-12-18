from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username


