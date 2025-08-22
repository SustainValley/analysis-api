# FastAPI 엔드포인트
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.services import recommender, fail_analyzer
from sqlalchemy.orm import Session
from app.db import get_db

app = FastAPI(
    title="MOCA AI API",
    docs_url="/docs"
)

# 프론트 CORS 설정
origins = [
    "http://localhost:3000",
    "https://mocacafe.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status")
def health_check():
    return {"status": "ok"}

@app.get("/promotion/{cafe_id}")
def promotion(cafe_id: str):
    status, time_slot, weekday = recommender.get_current_status()
    main_type, percent = recommender.get_main_meeting_type(cafe_id)
    
    if main_type is None:
        return {"error": "해당 카페의 예약 데이터가 없습니다."}

    message = recommender.generate_promotion_message(status, main_type, weekday, time_slot)
    return {
        "dayOfWeek": weekday,
        "timeSlot": time_slot,
        "commercial_status": status,
        "main_purpose": main_type,
        "percent": f"{percent}%",
        "rec_promotion": message
    }


@app.get("/cafe/{cafe_id}/cancel-reason")
def cancel_reason(cafe_id: int, db: Session = Depends(get_db)):
    return fail_analyzer.get_cancel_reason_percentage(db, cafe_id)