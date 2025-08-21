from sqlalchemy import Column, Integer, String, Enum, Time, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base
from app.db import Base
import enum

Base = declarative_base()

class CafeReservationStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"

class SpaceType(str, enum.Enum):
    OPEN = "OPEN"
    QUIET = "QUIET"
    MEETING = "MEETING"
    LIMITED_TALK = "LIMITED_TALK"
    
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
    
class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# Cafe 모델
class Cafe(Base):
    __tablename__ = "cafe"

    id = Column("cafe_id", BigInteger, primary_key=True)
    name = Column(String(255))
    location = Column(String(255))
    max_seats = Column(BigInteger)
    business_info_id = Column(BigInteger, ForeignKey("business_info.id"))
    min_order = Column(String(255))
    space_type = Column(Enum(SpaceType))
    image_url = Column(String(255))
    able_start_time = Column(Time)
    able_end_time = Column(Time)
    reservation_status = Column(Enum(CafeReservationStatus))

    # 관계
    operating_hours = relationship("CafeOperatingHours", back_populates="cafe", uselist=False)
    images = relationship("CafeImage", back_populates="cafe")

class CafeOperatingHours(Base):
    __tablename__ = "cafe_operating_hours"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    cafe = relationship("Cafe", back_populates="operating_hours")

    mon_open = Column(Time)
    mon_close = Column(Time)
    mon_is_open = Column(Integer)

    tue_open = Column(Time)
    tue_close = Column(Time)
    tue_is_open = Column(Integer)
    
    wed_open = Column(Time)
    wed_close = Column(Time)
    wed_is_open = Column(Integer)
    
    thu_open = Column(Time)
    thu_close = Column(Time)
    thu_is_open = Column(Integer)
    
    fri_open = Column(Time)
    fri_close = Column(Time)
    fri_is_open = Column(Integer)
    
    sat_open = Column(Time)
    sat_close = Column(Time)
    sat_is_open = Column(Integer)
    
    sun_open = Column(Time)
    sun_close = Column(Time)
    sun_is_open = Column(Integer)
    
class CafeImage(Base):
    __tablename__ = "cafe_image"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column("imageUrl", String)
    cafe_id = Column(Integer, ForeignKey("cafe.cafe_id"))
    
    cafe = relationship("Cafe", back_populates="images")
    