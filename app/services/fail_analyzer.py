# 예약 거절/실패 분석 로직
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.models.models import Reservation, CancelReason
from openai import OpenAI 

# 관심 있는 사유 6개
FOCUS_REASONS = [
    CancelReason.CLOSED_TIME,
    CancelReason.EQUIPMENT_UNAVAILABLE,
    CancelReason.PEAK_LIMIT,
    CancelReason.CROWDED,
    CancelReason.LOCATION_CHANGE,
    CancelReason.BUDGET_ISSUE
]

# OpenAI 인스턴스 생성
client = OpenAI() 

def get_cancel_reason_percentage(db: Session, cafe_id: int):
    # 현재 시각 기준 이전 달 계산
    now = datetime.now()
    
    # 앞뒤 한 달 범위
    start_date = (now - relativedelta(months=1)).strftime("%Y-%m-%d")
    end_date = (now + relativedelta(months=1)).strftime("%Y-%m-%d")

    # 사유별 건수 조회
    cancel_counts = {}
    for reason in FOCUS_REASONS:
        count = db.query(Reservation).filter(
            Reservation.cafe_id == cafe_id,
            Reservation.cancel_reason == reason,
            Reservation.date >= start_date,
            Reservation.date < end_date
        ).count()
        cancel_counts[reason.name] = count

    # 1차 GPT 호출: 조언 생성
    advice_prompt = (
    "다음 카페 예약 취소 건수를 기반으로, 사장님이 취할 수 있는 총체적 완화 조치를 "
    "한 문장으로 요약해서 추천해주세요.\n\n"
    f"{cancel_counts}\n\n"
    "참고할 전략 패턴:\n"
    "- 운영/시설 관련 취소 다수 (CLOSED_TIME, CROWDED, PEAK_LIMIT 건수가 높음) → 예약 막기/예약 시간 조정, 피크 시간 공지, 좌석 배치 최적화\n"
    "- 비용/장소 관련 취소 다수 (LOCATION_CHANGE, BUDGET_ISSUE 건수가 높음) → 프로모션/할인, 예약 안내 개선, 경쟁력 강화\n"
    "- 장비/준비 관련 취소 다수 (EQUIPMENT_UNAVAILABLE 건수가 높음) → 장비 점검 강화, 예비 장비 확보, 사전 장비 예약 안내\n"
    "- 특정 사유 혼합 → 종합 점검 필요, 사용자 설문/피드백 받아 개선 방향 설정"
    )
    advice_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": advice_prompt}],
        temperature=0.7
    )
    rec_advice = advice_response.choices[0].message.content.strip()


    # 2차 GPT 호출: 원인 명명
    cause_prompt = (
    "아래는 카페 예약 취소 현황과 이에 대한 조언입니다.\n\n"
    f"취소 건수: {cancel_counts}\n"
    f"조언: {rec_advice}\n\n"
    "이 상황의 근본 원인을 최대 8어 이하로 짧게 명명해주세요.\n"
    "단, 사장님 잘못처럼 보이지 않도록 중립적이고 개선 여지가 드러나게 표현해주세요."
    )   
    cause_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": cause_prompt}],
        temperature=0.7
    )
    root_cause = cause_response.choices[0].message.content.strip()

    # 결과 반환
    result = [{k: v} for k, v in cancel_counts.items()]
    return {
        "cafe_id": cafe_id,
        "year": now.year,
        "month": now.month,
        "focused_cancel_reason": result,
        "rec_advice": rec_advice,
        "root_cause": root_cause
    }