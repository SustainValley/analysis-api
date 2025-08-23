# 예약 거절/실패 분석 로직
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.models.models import Reservation, CancelReason

# 관심 있는 사유 6개
FOCUS_REASONS = [
    CancelReason.CLOSED_TIME,
    CancelReason.EQUIPMENT_UNAVAILABLE,
    CancelReason.PEAK_LIMIT,
    CancelReason.CROWDED,
    CancelReason.LOCATION_CHANGE,
    CancelReason.BUDGET_ISSUE
]

def get_cancel_reason_percentage(db: Session, cafe_id: int):
    # 현재 시각 기준 이전 달 계산
    now = datetime.now()
    
    # 앞뒤 한 달 범위
    start_date = (now - relativedelta(months=1)).strftime("%Y-%m-%d")
    end_date = (now + relativedelta(months=1)).strftime("%Y-%m-%d")
    
    # 전체 예약 수
    total_count = db.query(Reservation).filter(
        Reservation.cafe_id == cafe_id,
        Reservation.date >= start_date,
        Reservation.date < end_date
    ).count()

    # 대상 사유
    target_reasons = [
        CancelReason.CLOSED_TIME,
        CancelReason.EQUIPMENT_UNAVAILABLE,
        CancelReason.PEAK_LIMIT,
        CancelReason.CROWDED,
        CancelReason.LOCATION_CHANGE,
        CancelReason.BUDGET_ISSUE,
    ]

    result = []
    for reason in FOCUS_REASONS:
        count = db.query(Reservation).filter(
            Reservation.cafe_id == cafe_id,
            Reservation.cancel_reason == reason,
            Reservation.date >= start_date,
            Reservation.date < end_date
        ).count()
        result.append({reason.name: count})

    return {
        "cafe_id": cafe_id,
        "year": now.year,
        "month": now.month,
        "focused_cancel_reason": result
    }