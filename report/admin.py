from django.contrib import admin
from .models import TestStatistics, TestReport, TestResult

# Register your models here.
@admin.register(TestResult)
class TestResult(admin.ModelAdmin):
    list_display = ('StudentId', 'ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults')

@admin.register(TestStatistics)
class TestStatistics(admin.ModelAdmin):
    list_display = ('Statistics_YearSemester', 'Statistics_TestGrade', 'Statistics_AnswerList', 'Statistics_StrongPoint', 'Statistics_WeakPoint', 'Statistics_AccumulatedNumber', 'Statistics_AccumulatedRatio', 'Statistics_NationalAverage', 'Statistics_SeoulAverage', 'Statistics_SeoulRegionAverage')

@admin.register(TestReport)
class TestReport(admin.ModelAdmin):
    list_display = ('Student_YearSemester', 'Student_TestGrade', 'Student_AnswerList', 'Student_StrongPoint', 'Student_WeakPoint', 'Student_AccumulatedNumber', 'Student_AccumulatedRatio', 'Student_NationalAverage', 'Student_SeoulAverage', 'Student_SeoulRegionAverage')