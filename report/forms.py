from django import forms
from .models import TestResult

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['StudentId', 'ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults']