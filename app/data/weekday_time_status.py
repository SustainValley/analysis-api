import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(__file__)  # app/data
csv_path = os.path.join(current_dir, "gongneung_cafe.csv")

df = pd.read_csv(csv_path)

weekday_cols = [
    '월요일_매출_건수','화요일_매출_건수','수요일_매출_건수',
    '목요일_매출_건수','금요일_매출_건수','토요일_매출_건수','일요일_매출_건수'
]

time_cols = [
    '시간대_건수~06_매출_건수','시간대_건수~11_매출_건수','시간대_건수~14_매출_건수',
    '시간대_건수~17_매출_건수','시간대_건수~21_매출_건수','시간대_건수~24_매출_건수'
]

# 요일별 평균
weekday_avg = df[weekday_cols].mean()
# 시간대별 평균
time_avg = df[time_cols].mean()

# predicted 값 배열 만들기
predicted_list = [(3*wd_val + t_val)/4 for wd_val in weekday_avg.values for t_val in time_avg.values]
predicted_array = np.array(predicted_list)

# 분위수 기준 계산
low_thresh = np.percentile(predicted_array, 40)   # 하위 30% -> 비활성화
high_thresh = np.percentile(predicted_array, 60)  # 상위 30% -> 활성화

result = []

for wd_col, wd_val in weekday_avg.items():
    for t_col, t_val in time_avg.items():
        predicted = (3*wd_val + t_val) / 4
        if predicted <= low_thresh:
            status = '비활성화'
        elif predicted >= high_thresh:
            status = '활성화'
        else:
            status = '보통'
            
        result.append({
            '요일': wd_col.replace('_매출_건수',''),
            '시간대': t_col.replace('시간대_건수','').replace('_매출_건수',''),
            '예상_상태': status
        })

res_df = pd.DataFrame(result)

output_path = os.path.join(current_dir, "weekday_time_status.csv")
res_df.to_csv(output_path, index=False)
print(f"CSV 저장 완료: {output_path}")