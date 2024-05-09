from django.contrib import admin
from .models import TestStatistics, TestResult

# Register your models here.
@admin.register(TestResult)
class TestResult(admin.ModelAdmin):
    list_display = ('StudentId', 'student', 'ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults')

@admin.register(TestStatistics)
class TestStatistics(admin.ModelAdmin):
    list_display = ('Statistics_YearSemester', 'Statistics_TestGrade', 'Statistics_AnswerList', 'Statistics_ProblemType', 'Statistics_StrongPoint', 'Statistics_WeakPoint', 'Statistics_ScoreList', 'Statistics_AccumulatedNumber', 'Statistics_AccumulatedRatio', 'Statistics_NationalAverage', 'Statistics_SeoulAverage', 'Statistics_SeoulRegionAverage')
