from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthdate', 'grade', 'test_list')

    # def test_list(self, obj):
    #     return ', '.join([test.student for test in obj.test_results.all()])
    # test_list.short_description = 'Tests'  # 해당 메서드에 대한 설명 추가
    def test_list(self, obj):
        tests_str = []
        for test in obj.test_results.all():
            # ExamYearSemester 필드에서 연도와 학기를 분리
            test_year = int((test.ExamYearSemester)/10)
            test_semester = (test.ExamYearSemester)%10
            # 문자열 포맷팅으로 연도, 학기, 학년 정보를 포함한 문자열 생성
            formatted_str = f'{test_year}년도 {test_semester}학기 {test.ExamGrade}학년'
            tests_str.append(formatted_str)
            
        return ', '.join(tests_str)
    test_list.short_description = 'Tests'
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('test_results')

# @admin.register(Test)
# class TestAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'student_name', 'test_date', 'consulting_schedule', 'consulting_content', 'consulting_status')

#     def student_name(self, obj):
#         return ', '.join([test.name for test in obj.student.all()])
#     student_name.short_description = 'Students'  # 해당 메서드에 대한 설명 추가

#     def get_queryset(self, request):
#         return super().get_queryset(request).prefetch_related('student')
    
# @admin.register(Test_report)
# class TestReportAdmin(admin.ModelAdmin):
#     list_display = ('id', 'student', 'create_dt')
