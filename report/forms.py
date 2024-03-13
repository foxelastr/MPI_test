from django import forms
from .models import TestResult

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults']