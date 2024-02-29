from pathlib import Path
from django.views.generic import DetailView, TemplateView

from dashboard.models import Student
from mpitest import settings


class StudentDV(DetailView):
    model = Student
    template_name = 'dashboard/student_detail.html'
    
class TestDV(TemplateView):
    template_name = 'test_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 파일 저장 위치를 Path 객체로 관리
        files_dir = Path(settings.MEDIA_ROOT) / 'downloads'
        file_names = [f.name for f in files_dir.iterdir() if f.is_file()]  # 디렉토리 내의 파일 이름 리스트
        file_urls = [settings.MEDIA_URL + 'downloads/' + file for file in file_names]  # 파일 URL 리스트
        
        context['file_urls'] = file_urls
        return context