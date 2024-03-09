from django.views.generic.edit import CreateView
from django.views import View
from .models import TestResult
from django.template.response import TemplateResponse

class SubmitDV(CreateView):
    model = TestResult
    template_name = 'report/submit.html'
    fields = ['ExamYearSemester', 'ExamGrade', 'ExamArea', 'ExamResults']
    success_url = '/some/success/url'

class ResultDV(View):
    template_name = 'report/result.html'
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        # 컨텍스트 데이터 생성 로직
        context = {}
        return context
    
    def render_to_response(self, context, **response_kwargs):
        return TemplateResponse(request=self.request, template=self.template_name, context=context, **response_kwargs)