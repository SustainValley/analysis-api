from sqlalchemy import Column, String, Integer, ForeignKey, Date, Time, Enum, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from .cafe import Cafe 
from app.db import Base
import enum

class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class AttendanceStatus(str, enum.Enum):
    BEFORE_USE = "BEFORE_USE"
    IN_USE = "IN_USE"
    COMPLETED = "COMPLETED"

class MeetingType(str, enum.Enum):
    PROJECT = "PROJECT"
    STUDY = "STUDY"
    MEETING = "MEETING"
    INTERVIEW = "INTERVIEW"
    NETWORKING = "NETWORKING"
    ETC = "ETC"

class CancelReason(str, enum.Enum):
    CLOSED_TIME = "CLOSED_TIME"
    OUT_OF_BUSINESS = "OUT_OF_BUSINESS"
    CROWDED = "CROWDED"
    EQUIPMENT_UNAVAILABLE = "EQUIPMENT_UNAVAILABLE"
    MAINTENANCE = "MAINTENANCE"
    PEAK_LIMIT = "PEAK_LIMIT"
    NO_SHOW = "NO_SHOW"
    
    SCHEDULE_CHANGE = "SCHEDULE_CHANGE"
    PERSONAL_REASON = "PERSONAL_REASON"
    TIME_MISTAKE = "TIME_MISTAKE"
    LOCATION_CHANGE = "LOCATION_CHANGE"
    LACK_OF_ATTENDEES = "LACK_OF_ATTENDEES"
    BUDGET_ISSUE = "BUDGET_ISSUE"
    DUPLICATE = "DUPLICATE"

class Reservation(Base):
    __tablename__ = "reservation"

    id = Column("reservations_id", BigInteger, primary_key=True)
    cafe_id = Column(BigInteger, ForeignKey("cafe.cafe_id"))
    user_id = Column(BigInteger, ForeignKey("user.user_id"))
    attendance_status = Column(Enum(AttendanceStatus))
    date = Column(String(10))  # MySQL DATE
    start_time = Column(Time)
    end_time = Column(Time)
    meeting_type = Column(Enum(MeetingType))
    people_count = Column(Integer, nullable=False)
    reservation_status = Column(Enum(ReservationStatus))
    cancel_reason = Column(Enum(CancelReason))

    # 관계
    cafe = relationship("Cafe") 
