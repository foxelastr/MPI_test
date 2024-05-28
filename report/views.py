from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from .models import TestResult

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

class TestResultUV(UpdateView):
    model = TestResult
    fields = ['ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults']
    template_name = 'report/test_result_update_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.ExamResults:
            # 인덱스와 값의 쌍을 리스트로 변환하여 전달
            context['exam_results'] = list(enumerate(self.object.ExamResults, start=1))
        else:
            context['exam_results'] = list(enumerate([0] * 25, start=1))  # 기본값으로 0이 채워진 25개의 리스트 제공
        return context
    
    def get_success_url(self):
        return reverse_lazy('dashboard:student_detail', kwargs={'pk': self.object.student.pk})
    
def my_view(request):
    context = {
        'input_numbers': list(range(1, 26))  # 1부터 25까지의 숫자 리스트를 생성
    }
    return render(request, 'my_template.html', context)
