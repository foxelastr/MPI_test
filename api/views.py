from django.views.generic.list import BaseListView
from django.http import JsonResponse
from api.utils import obj_to_student, obj_to_test
from dashboard.models import Student, Test


class ApiStudentLV(BaseListView):
    model = Student
    
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        StudentList = [obj_to_student(obj) for obj in qs]
        return JsonResponse(data=StudentList, safe=False, status=200)
    
class ApiStudentDV(BaseListView):
    model = Test

class ApiStudentDV(BaseListView):
    model = Test

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        return queryset
    
    def render_to_response(self, context, **response_kwargs):
        qs = context['object_list']
        
        # 여기서 student_id를 기반으로 학생 이름을 조회
        student_name = Student.objects.get(id=self.kwargs.get('student_id')).name
        
        TestList = [obj_to_test(obj) for obj in qs]
        
        # 응답 데이터에 학생 이름 추가
        response_data = {'student_name': student_name, 'tests': TestList}
        
        return JsonResponse(data=response_data, safe=False, status=200)
    
# class ApiStudentDV(BaseListView):
#     model = Test
    
#     def get_queryset(self):
#         # URLconf에서 'student_id' 파라미터를 캡처하도록 설정해야 합니다.
#         student_id = self.kwargs.get('student_id')
#         # 'student' 필드를 통해 특정 학생과 관련된 Test 인스턴스들을 필터링합니다.
#         # 여기서 'student__id'는 Test 모델과 ManyToMany 관계를 가진 Student 모델의 ID 필드를 참조합니다.
#         queryset = Test.objects.filter(student__id=student_id)
#         return queryset

#     def render_to_response(self, context, **response_kwargs):
#         # get_queryset 메서드를 통해 필터링된 쿼리셋을 가져옵니다.
#         qs = self.get_queryset()
#         # Test 인스턴스들과 관련된 모든 학생 이름들을 리스트로 생성합니다.
#         # ManyToMany 필드인 'student'를 통해 관련된 모든 학생 객체에 접근할 수 있습니다.
#         student_names = list(set([student.name for test in qs for student in test.student.all()]))
#         # 학생 이름들을 담은 리스트를 JSON 형태로 반환합니다.
#         return JsonResponse(data={'students': student_names}, safe=False, status=200)