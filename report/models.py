from django.db import models

class TestResult(models.Model):
    ExamYearSemester = models.DateField('EXAM_YEAR_AND_SEMESTER')
    ExamGrade = models.PositiveSmallIntegerField('EXAM_GRADE')
    ExamArea = models.TextField('EXAM_AREA', max_length=50)
    ExamResults = models.JSONField('EXAM_RESULTS', default=list)

class TestReport(models.Model):
    pass

