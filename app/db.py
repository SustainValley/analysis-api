# app/db.py
# DB 연결

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# DB 연결 URL 형식: mysql+pymysql://username:password@host:port/database
DB_URL = "mysql+pymysql://root:3827@localhost:3306/hackathon_db"

# SQLAlchemy 엔진 생성
engine = create_engine(DB_URL, echo=True, future=True)

# 세션 생성기
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# ORM Base
Base = declarative_base()

# FastAPI 의존성용 세션
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()