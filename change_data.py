import os
import django
import json

# Django 프로젝트 설정 불러오기
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpitest.settings')
django.setup()

from report.models import TestStatistics  # 모델 임포트

# 데이터가 있는 디렉토리 경로
base_dir = r"E:\PNS\MPI_test\media\data\2022_2_HME_DATA"  # 'r'을 사용하여 raw string으로 처리

# 기존 데이터를 읽어와서 수정하는 함수
def modify_data_list(data_list):
    # 여기에 데이터를 수정하는 로직을 작성
    # 예를 들어, 각 항목에 특정 문자열을 추가한다든지, 값을 변경하는 등의 작업
    modified_data_list = [data for data in data_list]
    return modified_data_list

# 파일에서 데이터를 리스트로 읽어오는 함수
def read_data_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = [line.strip() for line in file if line.strip()]
    return data_list

# 1부터 9까지 각 학년에 대해 처리
for grade in range(1, 10):
    # 기존 데이터 읽기
    answer_list_path = os.path.join(base_dir, f"Answer_list\\{grade}.txt")
    type_list_path = os.path.join(base_dir, f"Type_list\\{grade}.txt")

    answer_list = read_data_to_list(answer_list_path)
    type_list = read_data_to_list(type_list_path)

    # 데이터 수정
    modified_answer_list = modify_data_list(answer_list)
    modified_type_list = modify_data_list(type_list)

    # 해당 학년의 TestStatistics 객체 가져오기
    report = TestStatistics.objects.get(Statistics_YearSemester=20211, Statistics_TestGrade=grade)

    # 데이터 수정 및 저장
    report.Statistics_AnswerList = modified_answer_list
    report.Statistics_ProblemType = modified_type_list
    report.save()

print("데이터가 성공적으로 수정되었습니다.")
