from pathlib import Path
from django.views.generic import DetailView, View

from dashboard.models import Student
from mpitest import settings
from django.http import FileResponse, Http404
import os

class StudentDV(DetailView):
    model = Student
    template_name = 'dashboard/student_detail.html'
    
class TestDV(View):
    template_name = 'dashboard/test_list.html'

    def get(self, request, *args, **kwargs):
        # HME_TESTS 내의 모든 파일에 대한 경로를 가져옵니다.
        base_dir = Path(settings.MEDIA_ROOT) / 'downloads' / 'HME_TESTS'
        file_urls = []

        # 각 하위 디렉토리를 순회합니다.
        for year_folder in base_dir.iterdir():
            if year_folder.is_dir():  # 디렉토리인 경우
                # 해당 디렉토리 내의 모든 파일을 순회합니다.
                for file in year_folder.iterdir():
                    if file.is_file() and file.suffix == '.pdf':  # PDF 파일인 경우
                        # 파일 URL을 생성하여 리스트에 추가합니다.
                        relative_path = file.relative_to(settings.MEDIA_ROOT)
                        file_urls.append(settings.MEDIA_URL + str(relative_path))

        # 템플릿에 전달할 컨텍스트 생성
        context = {'file_urls': file_urls}
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        from django.shortcuts import render
        return render(self.request, self.template_name, context)