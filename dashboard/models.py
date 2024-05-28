from django.conf import settings
from django.db import models
from django.utils.formats import date_format

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='students', default=1)
    name = models.CharField(max_length=5, unique=True)
    birthdate = models.DateField('BIRTHDATE')
    grade = models.PositiveSmallIntegerField('GRADE')
    
    def __str__(self):
        return self.name
    
    def __str__(self):
        # '2012년 1월 1일' 형태로 날짜 포맷
        return date_format(self.birthdate, format='Y년 n월 j일')
