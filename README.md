## MOCA 분석 코드

#### 파일구조
```
promotion-analysis-api/프로모션 분석 ​​-API/
├── app/
│   ├── main.py          # FastAPI , 프로모션 추천 & 취소/거절 사유 분석 API
│   ├── data/
│   │   ├── weekday_time_status.py
│   │   ├── weekday_time_status.csv
│   │   ├── data_settings.py
│   │   └── gongneung_cafe.csv   
│   ├── services/
│   │   ├── recommender.py      # 프로모션 추천 로직
│   │   ├── recommender.py      # 프로모션 추천 로직
│   │   └── fail_analyzer.py    # 예약 실패 분석 로직
│   ├── models/
|   |   ├── cafe.py
|   |   ├── reservation.py
|   |   ├── connect_test.py     # DB 연결 테스트
│   │   └── models.py           # 데이터 모델 설계  
│   └── db.py                   # DB 연결
└──  requirements.txt
``````````````

#### 코드 컨벤션
| Commit Type | 설명 |
|-------------|------|
| `feat`      | 기능 추가 |
| `fix`       | 버그 수정 |
| `refactor`  | 리팩토링 |
| `docs`      | 문서 수정 |
| `test`      | 테스트 또는 테스트 코드 추가 |
| `style`     | 코드 포맷팅, 세미콜론 누락, 코드 의미에 영향 없는 변경 |
| `build`     | 빌드 시스템 수정, 외부 종속 라이브러리 수정 (gradle, npm 등) |
| `rename`    | 파일명 또는 폴더명 수정 |
| `remove`    | 코드 또는 파일 삭제 |
| `chore`     | 그 외 자잘한 수정 |
