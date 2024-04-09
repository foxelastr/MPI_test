import pandas as pd
import os

# # # 지정된 디렉토리 경로
# directory = 'E:/PNS/MCLS/TCNP_data/통계 자료 추출 데이터/2021_1_HME_DATA'

# # 디렉토리 내의 모든 파일을 순회
# for filename in os.listdir(directory):
#     # CSV 파일인지 확인
#     if filename.endswith('statistics.csv'):
#         # 파일의 전체 경로
#         file_path = os.path.join(directory, filename)
#         # 파일 읽기 (header로 첫 행을 사용)
#         df = pd.read_csv(file_path, header=1)
#         # 3열의 데이터 추출 (파이썬은 0부터 인덱싱 하므로 2를 사용, 열 인덱스 주의)
#         column_data = df.iloc[:, 2].tolist()  # '인원' 열 데이터 추출, 필요한 열 인덱스로 조정

#         # 결과를 저장할 파일명 설정 (원본 파일명에 '_result' 추가)
#         result_filename = filename.replace('20211_hme_', '')
#         result_filename = result_filename.replace('_statistics.csv', '.txt')
#         result_file_path = os.path.join(directory, result_filename)

#         # 추출된 데이터를 새로운 텍스트 파일로 저장
#         with open(result_file_path, 'w') as f:
#             for item in column_data:
#                 f.write("%s\n" % item)


# 파일 경로 지정
file_path = './2021_1_서울주요지역.csv'

# CSV 파일 읽기, 2행부터 시작하므로 header=1로 설정
df = pd.read_csv(file_path, header=0)

# 5열 데이터 추출, 판다스 인덱스는 0부터 시작하므로 4를 사용
column_data = df.iloc[:, 4].tolist()

# 9로 나눈 나머지별로 분류할 리스트 딕셔너리 초기화
remainder_lists = {i: [] for i in range(9)}

# 행 번호에 따라 데이터 분류
for i, item in enumerate(column_data, start=1):  # 2행부터 시작
    remainder = i % 9
    remainder_lists[remainder].append(item)

# 분류된 데이터를 각각의 txt 파일로 저장
for remainder, items in remainder_lists.items():
    if remainder == 0:
        file_name = f'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/Seoul_Region_Average/{remainder+9}.txt'
    else:
        # file_name = f'E:/PNS/MCLS/TCNP_data/통계 자료 추출 데이터/2021_1_HME_DATA/{remainder}.txt'
        file_name = f'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/Seoul_Region_Average/{remainder}.txt'
    with open(file_name, 'w') as f:
        for item in items:
            f.write(f"{item}\n")

# # 파일 경로
# file_path = 'E:/PNS/MCLS/TCNP_data/통계 자료 추출 데이터/2021_1_HBM_DATA/2021_1_HME_DATA - 답 유형 출제의도.csv'

# # CSV 파일 읽기, 3행부터 시작하므로 header=2로 설정
# df = pd.read_csv(file_path, header=1)

# # 5~7열 데이터 추출, 판다스는 0부터 인덱싱하므로 각각 4, 5, 6을 사용
# columns_data = {
#     # 'answer': df.iloc[:, 4].tolist(),
#     # 'score': df.iloc[:, 5].tolist(),
#     'type': df.iloc[:, 6].tolist(),
# }

# # 각 열마다 25개씩 잘라서 저장
# for column_name, data in columns_data.items():
#     for i in range(0, len(data), 25):
#         # 현재 슬라이스의 데이터
#         slice_data = data[i:i+25]
#         # 파일 번호 (1부터 시작)
#         file_number = i // 25 + 1
#         # 파일 이름 설정
#         if column_name == 'answer':
#             file_name = f'{file_number}_answer.txt'
#         elif column_name == 'score':
#             file_name = f'{file_number}_score.txt'
#         elif column_name == 'type':
#             file_name = f'{file_number}.txt'
        
#         # 설정된 이름으로 파일 저장
#         file_path = f'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/Math_Ability/{file_name}'
#         with open(file_path, 'w') as f:
#             for item in slice_data:
#                 f.write(f"{item}\n")

# data = """
# 학년,초1,초2,초3,초4,초5,초6,중1,중2,중3
# 평균,82.8/100,74.7/100,70.8/100,71.7/100,69.5/100,72.0/100,57.6/100,62.8/100,57.5/100
# 계산력,26.2/28,26.3/28,24.6/28,26.1/28,21.8/28,22.9/28,22.0/28,22.9/28,23.9/28
# 이해력,29.4/32,30.4/32,24.2/32,26.0/32,23.3/32,29.0/32,19.4/32,23.8/32,22.6/32
# 추론력,14.4/20,9.3/20,13.5/20,7.1/20,9.6/20,9.1/20,6.3/20,10.2/20,6.7/20
# 문제해결력,12.7/20,8.6/20,8.5/20,12.6/20,14.8/20,11.0/20,10.0/20,5.9/20,4.2/20
# """

# # 데이터를 줄 단위로 분리
# lines = data.strip().split('\n')

# # 학년을 추출하여 리스트 생성
# grades = lines[0].split(',')[1:]

# # 각 학년에 대해 점수 추출 및 파일 저장
# for grade_index, grade in enumerate(grades, start=1):
#     scores_list = []
#     for line in lines[1:]:
#         parts = line.split(',')
#         score = parts[grade_index].split('/')[0]
#         scores_list.append(score)
    
#     file_name = f'{grade}.txt'
#     with open(file_name, 'w') as f:
#         for score in scores_list:
#             f.write(f"{score}\n")
    
#     print(f"{file_name}에 데이터가 저장되었습니다.")


# # 파일이 위치한 디렉토리
# directory = 'E:/PNS/MPI_test/media/data/2021_1_HME_DATA'

# # 파일 이름 변경 규칙
# rename_rules = {
#     'cho1': '1',
#     'cho2': '2',
#     'cho3': '3',
#     'cho4': '4',
#     'cho5': '5',
#     'cho6': '6',
#     'jung1': '7',
#     'jung2': '8',
#     'jung3': '9'
# }

# # 디렉토리 내의 모든 파일을 순회하며 이름 변경
# for filename in os.listdir(directory):
#     # 원본 파일 경로
#     old_file = os.path.join(directory, filename)
    
#     # 새 파일 이름을 위한 번호 추출
#     for key, value in rename_rules.items():
#         if key in filename:
#             # 새 파일 이름 생성
#             new_filename = filename.replace(key, value)
#             new_file = os.path.join(directory, new_filename)
            
#             # 파일 이름 변경
#             os.rename(old_file, new_file)
#             print(f"Renamed '{filename}' to '{new_filename}'")
#             break  # 일치하는 첫 번째 규칙을 적용한 후 반복 중단

# print("All files have been renamed.")


# # 파일이 위치한 디렉토리 경로
# directory = 'E:/PNS/MPI_test/media/data/2021_1_HME_DATA/Type_list'

# # 1부터 9까지의 숫자에 대응하는 파일 이름 변경
# for n in range(1, 10):
#     old_name = f'{n}_type.txt'  # 기존 파일 이름
#     new_name = f'{n}.txt'  # 새 파일 이름
    
#     # 파일 이름 변경을 위한 전체 경로 구성
#     old_path = os.path.join(directory, old_name)
#     new_path = os.path.join(directory, new_name)
    
#     # 파일 이름 변경
#     try:
#         os.rename(old_path, new_path)
#         print(f'파일 이름이 변경되었습니다: {old_name} -> {new_name}')
#     except FileNotFoundError:
#         print(f'{old_name} 파일을 찾을 수 없습니다.')
#     except Exception as e:
#         print(f'파일 이름 변경 중 오류가 발생했습니다: {e}')

# # CSV 파일 경로
# file_path = 'E:/PNS/MCLS/TCNP_data/2023_1_HME_DATA.csv'  # CSV 파일의 실제 경로

# # 데이터 읽기 (제목이 없으므로 header=None)
# df = pd.read_csv(file_path, header=None)

# # StrongPoint와 WeakPoint에 대한 데이터 추출
# strong_point_data = df.iloc[:, 0]  # 첫 번째 열
# weak_point_data = df.iloc[:, 1]    # 두 번째 열

# # StrongPoint와 WeakPoint 폴더 경로
# strong_point_dir = 'E:/PNS/MCLS/TCNP_data/2023_1_HME_DATA/StrongPoint'
# weak_point_dir = 'E:/PNS/MCLS/TCNP_data/2023_1_HME_DATA/WeakPoint'

# # 폴더가 없으면 생성
# os.makedirs(strong_point_dir, exist_ok=True)
# os.makedirs(weak_point_dir, exist_ok=True)

# # 데이터를 25개씩 나누어 파일로 저장
# for i in range(0, len(df), 25):
#     # 각각의 열에 대해 25개씩 데이터를 나누어 저장
#     strong_point_slice = strong_point_data[i:i+25]
#     weak_point_slice = weak_point_data[i:i+25]

#     # 파일 번호 결정 (1부터 시작)
#     file_number = i // 25 + 1
#     if file_number > 9:
#         break  # 1.txt부터 9.txt까지만 저장하기 위해

#     # StrongPoint 데이터 저장
#     strong_point_filename = os.path.join(strong_point_dir, f'{file_number}.txt')
#     with open(strong_point_filename, 'w', encoding='utf-8') as f:  # 인코딩을 utf-8로 지정
#         for item in strong_point_slice:
#             f.write(f"{item}\n")

#     # WeakPoint 데이터 저장
#     weak_point_filename = os.path.join(weak_point_dir, f'{file_number}.txt')
#     with open(weak_point_filename, 'w', encoding='utf-8') as f:  # 인코딩을 utf-8로 지정
#         for item in weak_point_slice:
#             f.write(f"{item}\n")
