# 프로모션 추천 로직

import pandas as pd
from datetime import datetime
import os
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.models import Reservation, MeetingType

# CSV 경로 (요일/시간대 상태는 여전히 파일 사용)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CAFE_STATUS_PATH = os.path.join(BASE_DIR, "data", "weekday_time_status.csv")
cafe_status_df = pd.read_csv(CAFE_STATUS_PATH)

PROMOTION_RULES = {
    "비활성화": {
        "STUDY": "3시간 이용 시 아메리카노 증정",
        "PROJECT": "팀 단체 할인 쿠폰 제공",
        "MEETING": "커피 1+1 제공",
        "INTERVIEW": "조용한 룸 무료 제공",
        "NETWORKING": "소규모 모임 할인",
        "ETC": "방문 시 소정의 음료 쿠폰 증정"
    },
    "보통": {
        "STUDY": "음료 10% 할인",
        "PROJECT": "단체 음료 1잔 무료",
        "MEETING": "기본 서비스 안내 쿠폰",
        "INTERVIEW": "음료 5% 할인",
        "NETWORKING": "모임 예약 시 간단 다과 제공",
        "ETC": "방문 시 쿠폰 제공"
    },
    "활성화": {
        "STUDY": "일반 요금 적용",
        "PROJECT": "일반 요금 적용",
        "MEETING": "일반 요금 적용",
        "INTERVIEW": "일반 요금 적용",
        "NETWORKING": "일반 요금 적용",
        "ETC": "일반 요금 적용"
    }
}

def get_current_status():
    """현재 시간대와 요일에 맞는 상권 상태 반환"""
    now = datetime.now()
    weekday_map = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    hour = now.hour
    weekday = weekday_map[now.weekday()]

    if hour < 6:
        time_slot = "~06"
    elif hour < 11:
        time_slot = "~11"
    elif hour < 14:
        time_slot = "~14"
    elif hour < 17:
        time_slot = "~17"
    elif hour < 21:
        time_slot = "~21"
    else:
        time_slot = "~24"

    row = cafe_status_df[
        (cafe_status_df['요일'] == weekday) & 
        (cafe_status_df['시간대'] == time_slot)
    ]
    if not row.empty:
        return row.iloc[0]['예상_상태'], time_slot, weekday
    return "보통", time_slot, weekday


def get_main_meeting_type(cafe_id: int):
    """카페별 주된 예약목적과 예약 비중 (DB에서 조회)"""
    db: Session = SessionLocal()
    try:
        reservations = db.query(Reservation).filter(Reservation.cafe_id == cafe_id).all()
        if not reservations:
            return None, 0
        
        # meeting_type Enum → 문자열 변환 후 pandas 집계
        meeting_types = [r.meeting_type.value for r in reservations if r.meeting_type]
        df = pd.DataFrame(meeting_types, columns=["meeting_type"])

        counts = df['meeting_type'].value_counts()
        main_type = counts.idxmax()   # "STUDY", "PROJECT" 등
        percent = round(counts.max() / counts.sum() * 100, 1)
        return main_type, percent
    finally:
        db.close()


def get_promotion_message(status: str, main_meeting_type: str) -> str:
    return PROMOTION_RULES.get(status, {}).get(main_meeting_type, "방문 시 혜택 없음")
