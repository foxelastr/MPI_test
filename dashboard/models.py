from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', default=1)
    name = models.CharField(max_length=5, unique=True)
    birthdate = models.DateField('BIRTHDATE')
    grade = models.PositiveSmallIntegerField('GRADE')
    
    def __str__(self):
        return self.name
