import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일에서 환경 변수 불러오기
load_dotenv()

# 우선순위: 환경 변수(DB_URL) > 하드코딩(SQLite 기본값)
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL") or "sqlite:///./p_df_main.db"

# SQLite라면 connect_args 필수
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# SQLAlchemy 엔진 생성
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
