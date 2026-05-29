from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=50, help_text="본명")
    grade = models.IntegerField(default=1, help_text="학년 (1~4)")

def __str__(self):
    return self.username