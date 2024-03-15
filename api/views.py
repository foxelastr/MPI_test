import json
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import BaseListView
from django.views.generic import CreateView, ListView
from django.http import JsonResponse
from api.utils import obj_to_student, obj_to_test
from dashboard.models import Student, Test
from report.forms import TestResultForm
from report.models import TestResult, TestStatistics


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
        # 폼 데이터가 유효하면 데이터 저장
        self.object = form.save()
        # AJAX 요청에 대해서는 JSON 응답 반환
        return JsonResponse({'status': 'success', 'data': self.object.id}, status=201)

    def form_invalid(self, form):
        # 폼 데이터가 유효하지 않으면 에러 메시지와 함께 응답 반환
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
class ApiReportLV(ListView):
    model = TestResult
    
    def get(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = Test.objects.filter(student__id=student_id)
        data = list(queryset.values())  # 또는 적절한 데이터 변환 로직
        return JsonResponse(data, safe=False)
    
    def get_queryset(self):
        # 필요한 경우, 특정 조건에 맞는 쿼리셋을 반환하는 로직을 구현합니다.
        # 예를 들어, 특정 학년의 시험 결과만 필터링하는 경우 등
        return super().get_queryset()

    def render_to_response(self, context, **response_kwargs):
        # 컨텍스트 데이터를 사용하여 비교 로직 구현
        results = []
        for test_result in context['object_list']:
            # TestStatistics에서 해당 시험의 통계 정보를 조회
            statistics = TestStatistics.objects.filter(
                Statistics_YearSemester=test_result.ExamYearSemester,
                Statistics_TestGrade=test_result.ExamGrade,
            ).first()

            if statistics:
                # 비교 로직 구현
                compare_results = self.compare_answers(test_result.ExamResults, statistics.Statistics_AnswerList)
                results.append({
                    'test_id': test_result.id,
                    'compare_results': compare_results,
                })

        return JsonResponse(results, safe=False, **response_kwargs)

    def compare_answers(self, exam_results, answer_list):
        # 시험 답안과 통계 답안을 비교하여 O/X 리스트 반환
        compare_results = ['O' if exam == stat else 'X' for exam, stat in zip(exam_results, answer_list)]
        return compare_results
    
    
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