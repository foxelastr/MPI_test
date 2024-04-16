from django.conf import settings
from django.db import models

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students', default=1)
    name = models.CharField(max_length=5, unique=True)
    birthdate = models.DateField('BIRTHDATE')
    grade = models.PositiveSmallIntegerField('GRADE')
    
    def __str__(self):
        return self.name
