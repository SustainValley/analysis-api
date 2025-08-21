# app/models/dto.py
from app.db import SessionLocal
from app.models.models import Cafe, Reservation

def main():
    # 세션 열기
    session = SessionLocal()
    try:
        # Cafe 5개 조회
        cafes = session.query(Cafe).limit(5).all()
        print("===== Cafes =====")
        for c in cafes:
            print(f"Cafe ID: {c.cafe_id}, Name: {c.name}, Location: {c.location}, Max Seats: {c.max_seats}")

        # Reservation 5개 조회
        reservations = session.query(Reservation).limit(5).all()
        print("\n===== Reservations =====")
        for r in reservations:
            print(f"Reservation ID: {r.id}, Cafe ID: {r.cafe_id}, People: {r.people_count}, "
                  f"Status: {r.reservation_status}, Type: {r.meeting_type}, "
                  f"Attendance: {r.attendance_status}, Cancel: {r.cancel_reason}")
    finally:
        # 세션 닫기
        session.close()


if __name__ == "__main__":
    main()
