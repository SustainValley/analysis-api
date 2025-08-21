# FastAPI 엔드포인트
from fastapi import FastAPI
from app.services import recommender

app = FastAPI()


@app.get("/promotion/{cafe_id}")
def promotion(cafe_id: str):
    status, time_slot, weekday = recommender.get_current_status()
    main_type, percent = recommender.get_main_meeting_type(cafe_id)
    
    if main_type is None:
        return {"error": "해당 카페의 예약 데이터가 없습니다."}

    message = recommender.get_promotion_message(status, main_type)
    return {
        "요일": weekday,
        "시간대": time_slot,
        "예상_상태": status,
        "주된_예약목적": main_type,
        "예약비중": f"{percent}%",
        "추천_프로모션": message
    }
