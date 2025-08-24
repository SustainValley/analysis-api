# 예약 거절/실패 분석 로직
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.models.models import Reservation, CancelReason
from openai import OpenAI 
from datetime import datetime
from zoneinfo import ZoneInfo

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
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    
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
    "한 문장으로 요약해서 '제안'해주세요. "
    "직접 실행을 약속하는 말투(예: ~하겠습니다)는 피하고, "
    "사장님이 참고할 수 있는 권장 조치(예: ~하는 것이 좋습니다, ~를 고려해보세요)로 표현해주세요.\n\n"

    "취소 사유는 크게 두 그룹으로 나뉩니다:\n"
    "- 사장님 사정으로 인한 취소: CLOSED_TIME, CROWDED, PEAK_LIMIT, EQUIPMENT_UNAVAILABLE\n"
    "- 고객 사정으로 인한 취소: LOCATION_CHANGE, BUDGET_ISSUE\n\n"
    "추천 문장은 원인을 설명할 때 '사장님 사정'과 '고객 사정'을 구분해서 표현해주세요.\n"
    "예: '고객님의 위치 변경과 예산 문제로 인한 취소가 많아...' 또는 '운영 시간 외 예약과 매장 혼잡으로 인한 취소가 많아...'\n\n"
    
    "참고할 전략 패턴:\n"
    "- 사장님 사정 취소 다수 → 예약 시간 조정, 사전 예약 차단, 시설/장비 관리 강화\n"
    "- 고객 사정 취소 다수 → 프로모션/할인, 예약 안내 개선, 경쟁력 강화\n"
    "- 혼합 → 종합 점검 및 피드백 수집\n"
)
    advice_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": advice_prompt}],
        temperature=0.7
    )
    rec_advice = advice_response.choices[0].message.content.strip()
    
    # 앞뒤 작은따옴표만 감싸져 있으면 제거
    if rec_advice.startswith("'") and rec_advice.endswith("'"):
        rec_advice = rec_advice[1:-1]


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