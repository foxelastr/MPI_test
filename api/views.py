import json
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import BaseListView
from django.views.generic import CreateView, ListView
from django.http import JsonResponse
from api.utils import obj_to_student, obj_to_test
from dashboard.models import Student, Test
from report.forms import TestResultForm
from report.models import TestResult
from report import utils


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

class ApiSubmitCV(CreateView):
    model = TestResult
    form_class = TestResultForm
    success_url = reverse_lazy('result')  # 성공시 리다이렉트 될 URL 설정
    
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    def form_valid(self, form):
        # 폼 데이터가 유효하면 데이터 저장
        self.object = form.save()
        # AJAX 요청에 대해서는 JSON 응답 반환
        return JsonResponse({'status': 'success', 'data': self.object.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
class ApiResultLV(CreateView):
    model = TestResult
    form_class = TestResultForm
    success_url = reverse_lazy('result')  # 성공시 리다이렉트 될 URL 설정
    
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    def form_valid(self, form):
        print(form.cleaned_data)  # 폼 데이터 로깅하여 StudentId 값 확인

        # 폼 데이터가 유효하면 데이터 저장
        self.object = form.save()
        # AJAX 요청에 대해서는 JSON 응답 반환
        return JsonResponse({'status': 'success', 'data': self.object.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
class ApiReportLV(ListView):
    #####################################################
    ############ 통계처리 여기다 해라!!!!!!!!! ###########
    #####################################################
    # report/utils.py에 통계처리에 필요한 함수들 정의돼있음
    # import까지 했음

    model = TestResult
    context_object_name = 'test_results'
    
    def get_queryset(self):
        """
        필요에 따라 queryset을 커스터마이즈 할 수 있습니다.
        예를 들어, 특정 학생의 결과만 필터링하려면 여기서 조건을 추가할 수 있습니다.
        """
        student_id = self.kwargs.get('student_id')
        return TestResult.objects.filter(student_id=student_id)

    def render_to_response(self, context, **response_kwargs):
        """
        컨텍스트 데이터를 사용하여 각 시험 결과에 대한 점수를 계산하고, 이를 응답 데이터로 포함합니다.
        """
        # 시험 결과와 점수를 저장할 리스트 초기화
        results_with_scores = []

        for test_result in context['test_results']:
            try:
                # 각 시험 결과에 대한 점수 계산
                score = utils.calculate_score(
                    student_id=test_result.student_id,
                    year_semester=test_result.ExamYearSemester,
                    test_grade=test_result.ExamGrade
                )
                result_data = {
                    'test_id': test_result.id,
                    'score': score
                }
                results_with_scores.append(result_data)
            except ValueError as e:
                # 에러 처리: 적절한 로그 출력 또는 결과에 에러 메시지 추가 등
                print(f"Error calculating score for test result {test_result.id}: {e}")

        # 최종 결과를 JSON 형태로 응답
        return JsonResponse(results_with_scores, safe=False, **response_kwargs)
    
    
    # # POST 요청 처리
    # def post(self, request, *args, **kwargs):
    #     # 요청 바디를 JSON으로 파싱
    #     body_unicode = request.body.decode('utf-8')
    #     body = json.loads(body_unicode)
        
    #     # 필요한 데이터 처리 로직 구현
    #     # 예시: body 데이터를 사용하여 새 Test 객체 생성
    #     # new_test = Test.objects.create(**body)
        
    #     # 데이터를 딕셔너리 형태로 변환
    #     # 예시: 생성된 Test 객체의 정보를 딕셔너리 형태로 변환
    #     # data = {'id': new_test.id, 'name': new_test.name, ...}
        
    #     # JsonResponse를 사용하여 JSON 형태로 응답
    #     return JsonResponse(body, safe=False)  # 여기서는 예시로 받은 데이터를 그대로 반환