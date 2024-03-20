import json
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import BaseListView
from django.views.generic import CreateView, ListView
from django.http import HttpRequest, HttpResponse, JsonResponse
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
    
# class ApiReportLV(ListView):
#     model = TestResult
#     template_name = 'report/result.html'
#     context_object_name = 'test_results'
    
#     def get_queryset(self):
#         # URL의 파라미터로부터 student_id를 받아와서 필터링합니다.
#         self.student_id = self.kwargs.get('student_id')
#         return super().get_queryset().filter(StudentId=self.student_id)
    
#     def get_context_data(self, **kwargs):
#         # 부모 클래스의 get_context_data 메서드 호출로 기본 컨텍스트 데이터 가져오기
#         context = super(ApiReportLV, self).get_context_data(**kwargs)
        
#         # 필요한 추가 데이터를 context 딕셔너리에 추가
#         year_semester = self.request.GET.get('year_semester')
#         test_grade = self.request.GET.get('test_grade')
        
#         # 예제에서 utils.get_std_result 함수는 모델 인스턴스를 반환하는 것으로 보임
#         # 반환된 모델 인스턴스를 context 딕셔너리에 추가하지 말고, 이를 사용하여 필요한 데이터만 추출해서 추가해야 함
#         test_result = utils.get_std_result(self.student_id, year_semester, test_grade)
#         print("test result : ", test_result)
        
#         test_result_data = {
#             'StudentId': test_result.StudentId,
#             'ExamYearSemester': test_result.ExamYearSemester,
#             'ExamGrade': test_result.ExamGrade,
#             'ExamArea': test_result.ExamArea,
#             'ExamResults': test_result.ExamResults,
#         }

#         print("test result data: ", test_result_data)
        
#         match_statistics = utils.get_statistics(test_result.ExamYearSemester, test_result.ExamGrade)
#         print("\n\n")
#         print("match statistics : ", match_statistics)
        
#         # 모델 인스턴스 대신 필요한 정보만을 딕셔너리에 추가
#         context['additional_info'] = {
#             'year_semester': year_semester,
#             'test_grade': test_grade,
#             # 추가로 필요한 정보를 여기에 추가
#         }
        
#         return context

class ApiReportLV(ListView):
    model = TestResult
    template_name = 'report/result.html'
    context_object_name = 'test_results'

    def get(self, request, *args, **kwargs):
        # URL의 쿼리 파라미터에서 year_semester와 test_grade 값을 가져옵니다.
        year_semester = request.GET.get('year_semester')
        test_grade = request.GET.get('test_grade')

        # utils.get_std_result 함수를 사용하여 테스트 결과 객체를 가져옵니다.
        test_result = utils.get_std_result(self.kwargs.get('student_id'), year_semester, test_grade)
        
        match_statistics = utils.get_statistics(test_result.ExamYearSemester, test_result.ExamGrade)
        
        # 필요한 추가 데이터를 JSON 형식으로 클라이언트에 전송합니다.
        response_data = {
            'StudentId': test_result.StudentId,
            'ExamYearSemester': test_result.ExamYearSemester,
            'ExamGrade': test_result.ExamGrade,
            'ExamArea': test_result.ExamArea,
            'ExamResults': test_result.ExamResults,
            'Statistics_AnswerList' : match_statistics[0].first().Statistics_AnswerList,
            'Statistics_StrongPoint' : match_statistics[0].first().Statistics_StrongPoint,
            'Statistics_WeakPoint' : match_statistics[0].first().Statistics_WeakPoint,
            'Statistics_AccumulatedNumber' : match_statistics[0].first().Statistics_AccumulatedNumber,
            'Statistics_NationalAverage' : match_statistics[0].first().Statistics_NationalAverage,
            'Statistics_SeoulAverage' : match_statistics[0].first().Statistics_SeoulAverage,
        }

        # JsonResponse 객체를 사용하여 응답을 반환합니다.
        return JsonResponse(response_data)


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