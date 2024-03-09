import json
from django.views import View
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

class ApiSubmitV(View):
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
class ApiResultV(View):
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    # POST 요청 처리
    def post(self, request, *args, **kwargs):
        # 요청 바디를 JSON으로 파싱
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        # 필요한 데이터 처리 로직 구현
        # 예시: body 데이터를 사용하여 새 Test 객체 생성
        # new_test = Test.objects.create(**body)
        
        # 데이터를 딕셔너리 형태로 변환
        # 예시: 생성된 Test 객체의 정보를 딕셔너리 형태로 변환
        # data = {'id': new_test.id, 'name': new_test.name, ...}
        
        # JsonResponse를 사용하여 JSON 형태로 응답
        return JsonResponse(body, safe=False)  # 여기서는 예시로 받은 데이터를 그대로 반환