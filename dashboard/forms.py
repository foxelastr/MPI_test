import datetime
from django import forms

from dashboard.models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birthdate', 'grade']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birthdate', 'grade']
        labels = {
            'name': '이름',
            'birthdate': '생년월일',
            'grade': '학년',
        }
        widgets = {
            'grade': forms.Select(choices=[
                (1, '초1'), (2, '초2'), (3, '초3'),
                (4, '초4'), (5, '초5'), (6, '초6'),
                (7, '중1'), (8, '중2'), (9, '중3')
            ]),
        }