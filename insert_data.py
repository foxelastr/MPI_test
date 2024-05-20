import os
import django
import json

# Django 프로젝트 설정 불러오기
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mpitest.settings')
django.setup()

from report.models import TestStatistics  # 모델 임포트

# 데이터가 있는 디렉토리 경로
base_dir = r"E:\PNS\MPI_test\media\data\2022_2_HME_DATA"  # 'r'을 사용하여 raw string으로 처리

# Seoul_Average.txt에서 서울 평균 점수 읽기
seoul_average_path = os.path.join(base_dir, "Seoul_Average", "Seoul_Average.txt")

# 파일에서 데이터를 리스트로 읽어오는 함수
def read_data_to_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data_list = [line.strip() for line in file if line.strip()]
    return data_list

# Seoul_Average.txt에서 서울 평균 점수 읽기
with open(seoul_average_path, 'r') as file:
    seoul_averages = [float(line.strip()) for line in file.readlines()]

# 1부터 9까지 각 학년에 대해 처리
for grade in range(1, 10):
    # 각 파일의 경로 설정
    accumulated_number_path = os.path.join(base_dir, f"Accumulated_Number\\{grade}.txt")
    accumulated_ratio_path = os.path.join(base_dir, f"Accumulated_Ratio\\{grade}.txt")
    answer_list_path = os.path.join(base_dir, f"Answer_list\\{grade}.txt")
    type_list_path = os.path.join(base_dir, f"Type_list\\{grade}.txt")
    score_list_path = os.path.join(base_dir, f"Score_list\\{grade}.txt")
    national_average_path = os.path.join(base_dir, f"National_Average\\{grade}.txt")
    seoul_region_average_path = os.path.join(base_dir, f"Seoul_Region_Average\\{grade}.txt")
    strong_point_path = os.path.join(base_dir, f"StrongPoint\\{grade}.txt")
    weak_point_path = os.path.join(base_dir, f"WeakPoint\\{grade}.txt")

    # 파일에서 데이터를 불러옴
    accumulated_number = read_data_to_list(accumulated_number_path)
    accumulated_ratio = read_data_to_list(accumulated_ratio_path)
    answer_list = read_data_to_list(answer_list_path)
    type_list = read_data_to_list(type_list_path)
    score_list = read_data_to_list(score_list_path)
    national_average = float(read_data_to_list(national_average_path)[0])  # 파일에 하나의 데이터만 있다고 가정
    seoul_region_average = read_data_to_list(seoul_region_average_path)
    strong_point = read_data_to_list(strong_point_path)
    weak_point = read_data_to_list(weak_point_path)

    # TestReport 인스턴스 생성 및 저장
    report = TestStatistics(
        Statistics_YearSemester=20222,
        Statistics_TestGrade=grade,
        Statistics_AnswerList=answer_list,
        Statistics_ProblemType=type_list,
        Statistics_StrongPoint=strong_point,
        Statistics_WeakPoint=weak_point,
        Statistics_AccumulatedNumber=accumulated_number,
        Statistics_AccumulatedRatio=accumulated_ratio,
        Statistics_NationalAverage=national_average,
        Statistics_SeoulAverage=seoul_averages[grade - 1],  # 서울 평균
        Statistics_SeoulRegionAverage=seoul_region_average,
    )
    report.save()

print("데이터가 성공적으로 저장되었습니다.")
