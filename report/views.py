from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views import View
from .models import TestResult
from django.template.response import TemplateResponse

class SubmitDV(CreateView):
    model = TestResult
    template_name = 'report/submit.html'
    fields = ['StudentId', 'ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults']
    success_url = '/some/success/url'

class ResultDV(View):
    template_name = 'report/result.html'
    
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        # 쿼리 파라미터에서 값을 읽어옵니다.
        year_semester = request.GET.get('year_semester')
        test_grade = request.GET.get('test_grade')

        # 여기서 필요한 데이터를 조회하거나 처리하는 로직을 추가합니다.
        # 예: TestResult와 TestStatistics 모델을 사용하여 관련 데이터 조회

        context = {'year_semester': year_semester, 'test_grade': test_grade}
        print("context:", context)
        # 추가적으로 필요한 데이터 조회 및 처리 로직을 여기에 구현하여 context에 추가
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs) -> HttpResponse:
        return render(self.request, self.template_name, context)

# class ResultDV(View):
#     template_name = 'report/result.html'
    
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data()
#         return self.render_to_response(context)
    
#     def get_context_data(self, **kwargs):
#         # 컨텍스트 데이터 생성 로직
#         context = {}
#         return context
    
#     def render_to_response(self, context, **response_kwargs):
#         return TemplateResponse(request=self.request, template=self.template_name, context=context, **response_kwargs)