from django.contrib import admin
from .models import Student, Test, Test_report

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthdate', 'grade', 'test_list')

    def test_list(self, obj):
        return ', '.join([test.name for test in obj.test_set.all()])
    test_list.short_description = 'Tests'  # 해당 메서드에 대한 설명 추가

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('test_set')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'student_name', 'test_date', 'consulting_schedule', 'consulting_content', 'consulting_status')

    def student_name(self, obj):
        return ', '.join([test.name for test in obj.student.all()])
    student_name.short_description = 'Students'  # 해당 메서드에 대한 설명 추가

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('student')
    
@admin.register(Test_report)
class TestReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'create_dt')
