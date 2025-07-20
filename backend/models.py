from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class DataItem(Base):
    __tablename__ = "data_items"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    doc_type = Column(String) # "규칙", "사례", "용어", "PDF"
    content = Column(String)
    meta = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HistoryLog(Base):
    __tablename__ = "history_logs"
    id = Column(Integer, primary_key=True)
    action = Column(String)
    before = Column(JSON)
    after = Column(JSON)
    user = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)