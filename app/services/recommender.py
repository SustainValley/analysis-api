# 프로모션 추천 로직

import pandas as pd
from datetime import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.models import Reservation, MeetingType

# CSV 경로 (요일/시간대 상태는 여전히 파일 사용)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CAFE_STATUS_PATH = os.path.join(BASE_DIR, "data", "weekday_time_status.csv")
cafe_status_df = pd.read_csv(CAFE_STATUS_PATH)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_current_status():
    """현재 시간대와 요일에 맞는 상권 상태 반환"""
    now = datetime.now()
    weekday_map = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일']
    hour = now.hour
    weekday = weekday_map[now.weekday()]

    if hour < 6:
        time_slot = "00~06"
    elif hour < 11:
        time_slot = "06~11"
    elif hour < 14:
        time_slot = "11~14"
    elif hour < 17:
        time_slot = "14~17"
    elif hour < 21:
        time_slot = "17~21"
    else:
        time_slot = "21~24"

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
     
# GPT에게 상권 상태와 예약 목적을 넘겨주고,적절한 프로모션 메시지를 생성해주는 함수   
def generate_promotion_message(status: str, main_meeting_type: str, dayOfWeek: str, timeSlot: str) -> str:
 
    prompt = f"""
    너는 카페 마케팅 담당자야.
    현재 카페 상권 상태는 "{status}"이고,
    주요 예약 목적은 "{main_meeting_type}"이야.
    오늘 요일은 "{dayOfWeek}", 시간대는 "{timeSlot}"이야.

    조건:
    1. 이 메시지는 고객에게 보여주는 것이 아니라, 카페 사장에게 프로모션 아이디어를 추천하는 내용이어야 함.
    2. 프로모션은 현실적이어야 하고, 사장이 손해보지 않도록 구성.
        (예: 무료 제공보다는 추가 매출이 발생하는 현실적인 할인이나 세트 구성 등)
    3. 상권 상태가 "보통" 이상이면 강한 프로모션은 필요없고,
        상권 상태가 "비활성화"일 때 집중적으로 고객을 유입할 수 있는 프로모션을 제안.
    4. 어투은 자연스럽게, 간단히 1문장 정도로, 마지막에 “~하는 건 어떨까요?” 식으로 권고형/제안형 톤으로 마무리.

    위 조건을 반영해서, 고객에게 제공할 수 있는 프로모션 아이디어를 제안해줘.
    """

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "너는 카페 프로모션을 기획하는 마케터다."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.8,
    max_tokens=100
)

    return response.choices[0].message.content.strip()

