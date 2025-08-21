import pandas as pd

# 파일 경로
file1 = '/Users/jeong-yujin/Downloads/서울시 상권분석서비스(영역-상권).csv'
file2 = '/Users/jeong-yujin/Downloads/서울시 상권분석서비스(추정매출-상권)_2024년.csv'

# CSV 읽기
df_area = pd.read_csv(file1, encoding='cp949')
df_sales = pd.read_csv(file2, encoding='cp949')

# 병합
merged_df = pd.merge(
    df_sales,
    df_area,
    on=['상권_코드', '상권_구분_코드', '상권_구분_코드_명'],
    how='left'
)

# 공릉1,2동 + 카페 데이터 한 번에 필터링
target_dongs = [11350595, 11350600]
cafe_code = 'CS100010'

gongneung_cafe_df = merged_df[
    (merged_df['자치구_코드'] == 11350) & 
    (merged_df['행정동_코드'].isin(target_dongs)) & 
    (merged_df['서비스_업종_코드'] == cafe_code)
]

# 저장
gongneung_cafe_df.to_csv('/Users/jeong-yujin/csv_model_project/gongneung_cafe.csv', index=False, encoding='utf-8-sig')
print(f"공릉1동,2동 카페 데이터 저장 완료! ({len(gongneung_cafe_df)}행)")
