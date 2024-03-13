from django.db import models

class TestResult(models.Model):
    ExamYearSemester = models.PositiveIntegerField('EXAM_YEAR_AND_SEMESTER')
    ExamGrade = models.PositiveSmallIntegerField('EXAM_GRADE')
    ExamArea = models.TextField('EXAM_AREA', max_length=50)
    ExamResults = models.JSONField('EXAM_RESULTS', default=list)
    
    def result_info(self):
        return f"RESULT:TEST_{self.ExamYearSemester}_GRADE_{self.ExamGrade}"
    
    def __str__(self):
        return self.result_info()

class TestStatistics(models.Model):
    #  학년 / 답리스트 / 강약점 / 누적인원 / 누적비율 / 전국평균 / 서울평균 / 서울지역별평균
    Statistics_YearSemester = models.PositiveIntegerField('YEAR_AND_SEMESTER', default=20231)
    Statistics_TestGrade = models.PositiveSmallIntegerField('TEST_GRADE', default=1)
    Statistics_AnswerList = models.JSONField('ANSWER_LIST', default=list)
    Statistics_StrongPoint = models.JSONField('STRONG_POINT', default=list)
    Statistics_WeakPoint = models.JSONField('WEAK_POINT', default=list)
    Statistics_AccumulatedNumber = models.JSONField('ACCUMULATED_NUMBER', default=list)
    Statistics_AccumulatedRatio = models.JSONField('ACCUMULATED_RATIO', default=list)
    Statistics_NationalAverage = models.FloatField('NATIONAL_AVERAGE', default=0.0)
    Statistics_SeoulAverage = models.FloatField('SEOUL_AVERAGE', default=0.0)
    Statistics_SeoulRegionAverage = models.JSONField('SEOULRegion_AVERAGE', default=list)
    
    # def test_info(self):
    #     return f"REPORT:TEST_{self.YearSemester}_GRADE_{self.TestGrade}"
    
    # def __str__(self):
    #     return self.test_info

class TestReport(models.Model):
    #  학년 / 답리스트 / 강약점 / 누적인원 / 누적비율 / 전국평균 / 서울평균 / 서울지역별평균
    Student_YearSemester = models.PositiveIntegerField('YEAR_AND_SEMESTER', default=20231)
    Student_TestGrade = models.PositiveSmallIntegerField('TEST_GRADE', default=1)
    Student_AnswerList = models.JSONField('ANSWER_LIST', default=list)
    Student_StrongPoint = models.JSONField('STRONG_POINT', default=list)
    Student_WeakPoint = models.JSONField('WEAK_POINT', default=list)
    Student_AccumulatedNumber = models.JSONField('ACCUMULATED_NUMBER', default=list)
    Student_AccumulatedRatio = models.JSONField('ACCUMULATED_RATIO', default=list)
    Student_NationalAverage = models.FloatField('NATIONAL_AVERAGE', default=0.0)
    Student_SeoulAverage = models.FloatField('SEOUL_AVERAGE', default=0.0)
    Student_SeoulRegionAverage = models.JSONField('SEOULRegion_AVERAGE', default=list)
    
    # def test_info(self):
    #     return f"REPORT:TEST_{self.YearSemester}_GRADE_{self.TestGrade}"
    
    # def __str__(self):
    #     return self.test_info
