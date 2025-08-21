# 예약 거절/실패 분석 로직
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Reservation, CancelReason

# 관심 있는 사유 6개
FOCUS_REASONS = [
    CancelReason.CLOSED_TIME,
    CancelReason.EQUIPMENT_UNAVAILABLE,
    CancelReason.PEAK_LIMIT,
    CancelReason.NO_SHOW,
    CancelReason.LOCATION_CHANGE,
    CancelReason.BUDGET_ISSUE
]

def get_cancel_reason_percentage(db: Session, cafe_id: int, year: int, month: int):
    # 월 범위 계산
    start_date = f"{year:04d}-{month:02d}-01"
    if month == 12:
        end_year = year + 1
        end_month = 1
    else:
        end_year = year
        end_month = month + 1
    end_date = f"{end_year:04d}-{end_month:02d}-01"

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
        CancelReason.NO_SHOW,
        CancelReason.LOCATION_CHANGE,
        CancelReason.BUDGET_ISSUE,
    ]

    result = []
    for reason in target_reasons:
        count = db.query(Reservation).filter(
            Reservation.cafe_id == cafe_id,
            Reservation.cancel_reason == reason,
            Reservation.date >= start_date,
            Reservation.date < end_date
        ).count()
        percentage = (count / total_count * 100) if total_count > 0 else 0
        result.append({reason.name: f"{percentage:.1f}%"})

    return {
        "cafe_id": cafe_id,
        "year": year,
        "month": month,
        "focused_cancel_reason": result
    }