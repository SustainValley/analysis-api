# app/db.py
# DB 연결

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


load_dotenv()  # .env 파일 로드

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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