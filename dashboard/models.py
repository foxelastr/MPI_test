from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=5, unique=True)
    birthdate = models.DateField('BIRTHDATE')
    grade = models.PositiveSmallIntegerField('GRADE')
    
    def __str__(self):
        return self.name
    
    
class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    student = models.ManyToManyField('STUDENT', blank=True)
    test_date = models.DateField('Test_date', auto_now_add=True)
    consulting_schedule = models.DateTimeField('SCHEDULE', blank=True, null=True)
    consulting_content = models.TextField('CONTENT', max_length=200, blank=True, help_text='상담 내용을 적으세요.')
    consulting_status = models.BooleanField('CONSULTING STATUS', default=False)
    
    def __str__(self):
        return self.name
    
    
class Test_report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    # 원점수 / 전국 백분위 / 수능 예상 등급 / 고1 내신 예상 등급 / 중학교 내신 예상 백분위 / 수학적 능력 분석(계산력/이해력/추론력/문제해결력) / 강점 및 약점 / 문항분석(번호-배점-정답-학생답)
    create_dt = models.DateTimeField('CREATE DT', auto_now_add=True)
